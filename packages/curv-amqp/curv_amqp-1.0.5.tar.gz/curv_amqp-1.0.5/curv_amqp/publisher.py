from typing import Optional
from copy import deepcopy
from time import time
from uuid import uuid4

from pika.spec import BasicProperties
from curv_amqp.channel import Channel


class Publisher(Channel):
    def publish(self,
                routing_key: str,
                body: bytes,
                exchange: str = '',
                properties: Optional[BasicProperties] = None,
                mandatory: bool = False):
        """Publish to the channel with the given exchange, routing key, and
        body.

        For more information on basic_publish and what the parameters do, see:

            http://www.rabbitmq.com/amqp-0-9-1-reference.html#basic.publish

        NOTE: mandatory may be enabled even without delivery
          confirmation, but in the absence of delivery confirmation the
          synchronous implementation has no way to know how long to wait for
          the Basic.Return.

        :param str routing_key: The routing key to bind on
        :param bytes body: The message body; empty string if no body
        :param str exchange: The exchange to publish to
        :param pika.spec.BasicProperties properties: message properties
        :param bool mandatory: The mandatory flag

        :raises UnroutableError: raised when a message published in
            publisher-acknowledgments mode (see
            `BlockingChannel.confirm_delivery`) is returned via `Basic.Return`
            followed by `Basic.Ack`.
        :raises NackError: raised when a message published in
            publisher-acknowledgements mode is Nack'ed by the broker. See
            `BlockingChannel.confirm_delivery`.
        """
        # NOTE: Defaults to persistent delivery mode, creates a timestamp,
        # and unique message id as a uuid4 hex
        if properties is not None:
            props = deepcopy(properties)
        else:
            props = BasicProperties()
        if props.delivery_mode is None:
            props.delivery_mode = 2
        if props.timestamp is None:
            props.timestamp = time()
        if props.message_id is None:
            props.message_id = uuid4().hex
        self.conditional_reconnect()
        self.queue_declare(queue=routing_key)
        self.blocking_channel.basic_publish(exchange=exchange,
                                            routing_key=routing_key,
                                            body=body,
                                            properties=props,
                                            mandatory=mandatory)
