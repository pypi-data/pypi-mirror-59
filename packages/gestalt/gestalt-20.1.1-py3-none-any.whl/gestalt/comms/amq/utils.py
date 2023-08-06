import os
from gestalt.compression import compress, decompress
from gestalt.serialization import (
    dumps,
    loads,
    registry,
    CONTENT_TYPE_PROTOBUF,
    CONTENT_TYPE_AVRO,
)

from typing import Any, Optional, Tuple


def build_amqp_url(
    user: str = None,
    password: str = None,
    host: str = None,
    port: int = None,
    virtual_host: str = None,
    connection_attempts: int = None,
    heartbeat_interval: int = None,
) -> str:
    user = user if user else os.getenv("RABBITMQ_USER", "guest")
    password = password if password else os.getenv("RABBITMQ_PASS", "guest")
    host = host if host else os.getenv("RABBITMQ_HOST", "localhost")
    port = int(port if port else os.getenv("RABBITMQ_PORT", "5672"))
    virtual_host = virtual_host if virtual_host else "%2F"

    options = []
    if connection_attempts:
        options.append(f"connection_attempts={connection_attempts}")
    if heartbeat_interval:
        options.append(f"heartbeat_interval={heartbeat_interval}")

    options_str = ""
    if options:
        options_str = "?" + "&".join(options)

    amqp_url = f"amqp://{user}:{password}@{host}:{port}/{virtual_host}{options_str}"
    return amqp_url


def encode_payload(
    data: Any,
    *,
    content_type: str = None,
    compression: str = None,
    headers: dict = None,
    type_identifier: int = None,
) -> Tuple[bytes, str, str]:
    """ Prepare a message payload.

    :param data: The message data to encode.

    :param content_type: A string specifying the message content type. By
      default the value is None. This field determines the data
      serialization format.

    :param compression: An optional string specifying a compression method to
      use. If compression is defined then headers must also be supplied.

    :param headers: A dict of headers that will be associated with the
      message.

    :param type_identifier: An integer that uniquely identifies a
      registered message.

    :returns: A three-item tuple containing the serialized data as bytes
      a string specifying the content type (e.g., `application/json`) and
      a string specifying the content encoding, (e.g. `utf-8`).

    """
    # Some content-types require additional information to be passed to
    # help decode the message payload. This is achieved by adding
    # information to the message headers.

    # Google Protocol buffer decoders require awareness of the object type
    # being decoded (referred to as a symbol). The symbol name is added to
    # the headers so that it can be used on the receiving side.
    if content_type == CONTENT_TYPE_PROTOBUF:
        if type_identifier is None:
            raise Exception("No protobuf id specified!")
        headers["x-protobuf-id"] = type_identifier

    # Avro decoders require awareness of the schema that describes the object.
    # This information is added to the headers so that it can be used on the
    # receiving side.
    if content_type == CONTENT_TYPE_AVRO:
        if type_identifier is None:
            raise Exception("No Avro id specified!")
        headers["x-avro-id"] = type_identifier

    serialization_name = registry.type_to_name[content_type]

    try:
        content_type, content_encoding, payload = dumps(
            data, serialization_name, type_identifier=type_identifier
        )
    except Exception as exc:
        raise Exception(f"Error serializing payload to {content_type}: {exc}") from None

    if compression:
        try:
            headers["compression"], payload = compress(payload, compression)
        except Exception as exc:
            raise Exception(
                f"Error compressing payload using {compression}: {exc}"
            ) from None

    return payload, content_type, content_encoding


def decode_payload(
    data: bytes,
    compression: Optional[str] = None,
    content_type: str = None,
    content_encoding: str = None,
    type_identifier: int = None,
) -> Any:
    """ Decode a message payload

    :param data: The message payload data to decode.

    :param content_type: A string specifying the message content type. By
      default the value is None.

    :param compression: An optional string specifying a compression mime-type.

    :param type_identifier: An integer that uniquely identifies a
      registered message.
    """

    if compression:
        try:
            _mime_type, data = decompress(data, compression)
        except Exception as exc:
            raise Exception(
                f"Error decompressing payload using {compression}: {exc}"
            ) from None

    try:
        payload = loads(
            data, content_type, content_encoding, type_identifier=type_identifier
        )
    except Exception as exc:
        raise Exception(
            f"Error decoding payload with content-type={content_type}: {exc}"
        ) from None

    return payload


def decode_message(message: "aio_pika.IncomingMessage"):
    """ Decode a message payload """

    if content_type == CONTENT_TYPE_AVRO:
        type_identifier = message.headers.get("x-avro-id")
    elif content_type == CONTENT_TYPE_PROTOBUF:
        type_identifier = message.headers.get("x-protobuf-id")
    else:
        type_identifier = None
    type_identifier
    payload = decode_payload(
        message.body,
        message.headers.get("compression"),
        message.content_type,
        message.content_encoding,
        type_identifier=type_identifier,
    )
    return payload
