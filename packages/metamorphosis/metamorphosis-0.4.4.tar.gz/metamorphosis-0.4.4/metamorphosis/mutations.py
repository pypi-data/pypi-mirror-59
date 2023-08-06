from uuid import uuid4
import time

import graphene as g
import msgpack
import werkzeug.exceptions

from metamorphosis.events import load_objecttype, dump_objecttype
import re

def class_case_to_snake_case(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


class MutationTimings(g.Enum):
    synchronous = 1
    asynchronous = 2


class EventMutation(g.Mutation):
    """
    A mutation that drops an event onto a Kafka topic.

    Subclass this method and write it like a typical Mutation, but instead of defining the `mutate` method, define
    the `mutate_event` method to return an object of the class you've defined or some other ObjectType that can serve
    as an event on the Kafka stream.

    If you define this method, you should have one consumer that saves its return value to the redis store. This is
    accomplished by setting a flag on the `msvc.event_consumer decorator`. Its return event will be treated as the
    result for this mutation. See the example for info on how that's done.

    Attributes:
        - microservice (Microservice): The microservice instance this event belongs to. Required.
        - polling_delta (float): The length of time to sleep between polling to look for results in the redis store.
            Default 0.1s
        - publish_topic (str): The Kafka topic the event will post to
    """
    microservice = None
    polling_delta = 0.1
    publish_topic = None
    allowed_timings = (MutationTimings.asynchronous,)
    default_timing = MutationTimings.asynchronous
    consequent_objecttypes = None
    mutation_event_type = None
    sync_timeout = 60

    @classmethod
    def __init_subclass__(cls, **kwargs):
        if cls.mutation_event_type is None:
            raise KeyError(f"{cls.__name__}.mutation_event_type must be defined as the BaseEventMixin ObjectType "
                           f"that the mutation yields.")

        cls.microservice.logger.info("Registering mutation %s (%s)", cls.__name__, class_case_to_snake_case(cls.__name__))
        if cls.publish_topic is None:
            cls.publish_topic = cls.microservice.name

        cls.microservice.mutations[class_case_to_snake_case(cls.__name__)] = cls

        if MutationTimings.synchronous in cls.allowed_timings:
            if not cls.consequent_objecttypes:
                raise KeyError(f"{cls.__name__}.consequent_objecttypes must be defined for synchronous calls. this is"
                               f"the return type of the consumer function.")

        if cls.consequent_objecttypes:
            ts = []
            if MutationTimings.asynchronous in cls.allowed_timings:
                ts = (cls.mutation_event_type,)

            if len(cls.consequent_objecttypes) > 1:
                class Meta:
                    types = tuple(ts.extend(cls.consequent_objecttypes))
                MutationResponseData = type(f'{cls.__name__}MutationResponse', (g.Union,), {"Meta": Meta})
                cls.data = g.Field(MutationResponseData)
            else:
                cls.data = g.Field(cls.consequent_objecttypes[0])
        else:
            cls.data = g.Field(cls.mutation_event_type)

        return super().__init_subclass__(**kwargs)

    @classmethod
    def mutate(cls, root, info, **kwargs):
        """
        The mutation itself. Do not override this method. Instead override mutate_event.
        """
        # this probably doesn't need to create a producer every single time. I don't know. Not overthinking it.

        # create the producer and attach it to the current event loop.  Need to figure out broker address config loc.
        producer = cls.microservice.producer

        # this is the CreateForm mutation's ObjectType. Not sure if that's what I really *want* but the return type on
        # this is the form object itself. Not sure what the pattern should be here.
        evt = cls.mutate_event(root=root, info=info, **kwargs)
        evt.id = str(uuid4())

        # serialize the event and send it over Kafka to the 'forms' topic.  Probably should set this topic in the
        # microservice instance.
        producer.send(cls.publish_topic, msgpack.packb(dump_objecttype(evt)))
        producer.flush()

        if (
                MutationTimings.synchronous in cls.allowed_timings and
                ((hasattr(evt, 'timing') and evt.timing == MutationTimings.synchronous) or
                 (not hasattr(evt, 'timing') and cls.default_timing == MutationTimings.synchronous) or
                 len(cls.allowed_timings) == 1
                )
        ):
            cls.microservice.logger.debug('%s', dump_objecttype(evt))
            cls.microservice.logger.debug('Message sent to %s, waiting on reply to be ready', cls.publish_topic)

            # here we poll every tenth of a second to see if a result is ready for us. We should probably time out, too
            # after a configurable amount of time
            slept = 0
            while not cls.microservice.recent_results.exists(evt.id) and slept < cls.sync_timeout:
                time.sleep(cls.polling_delta)
                slept += cls.polling_delta
            if slept > cls.sync_timeout:
                raise werkzeug.exceptions.RequestTimeout(evt.id)

            rsp_evt = load_objecttype(msgpack.unpackb(cls.microservice.recent_results.get(evt.id), raw=False))

            # the result in this case is the form itself.  we look for a registered exception event and if there is
            # one, raise it.
            cls.microservice.raise_for_evt(rsp_evt)

            return cls(data=rsp_evt)
        else:
            return cls(data=evt)

    @classmethod
    def mutate_event(cls, root, info, **kwargs):
        """
        Override this method. Return an event object, probably an instance of the class you defined.

        This is where you want to do authorization and validation of the input. If it all validates okay, then
        return an event object (Either the class you define this method or another event of (ObjectType, BaseEventMixin)

        Args:
            root: Passed from graphene
            info: Passed from graphene, the current context.
            **kwargs: This will be the args from the Arguments class you define as part of the mutation.

        Returns:
            A populated (ObjectType, BaseEventMixin) object.
        """
        raise NotImplementedError("Must implement this method instead of `mutate`")

