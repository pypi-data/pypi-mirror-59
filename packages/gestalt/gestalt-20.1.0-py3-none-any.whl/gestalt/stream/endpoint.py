import asyncio
import enum
import inspect
import logging
import random
import socket

from ssl import SSLContext
from gestalt import serialization
from gestalt.stream.protocols.base import BaseStreamProtocol
from typing import Any, Dict, Optional, Sequence, Tuple, Type

logger = logging.getLogger(__name__)


# The percentage of jitter to apply to the reconnection backoff time
BACKOFF_JITTER = 0.05


class StreamEndpointModes(enum.Enum):
    Server = 0
    Client = 1


class StreamEndpoint:
    """
    A stream endpoint provides two-way communications with a another stream
    oriented interface. Depending on the protocol being used, an endpoint can
    operate on a simple stream of bytes or on higher level message objects.

    A stream endpoint operates in one of two modes; client or server.

    When operating in server mode a stream endpoint will bind to an interface
    and port to listen for connections from clients. Upon detecting new client
    connections the server will instantiate a new protocol instance to handle
    communications with the peer.

    When operating in client mode a stream endpoint will connecting to a
    server on the supplied interface and port. A client endpoint

    An endpoint uses callback functions to notify the endpoint user when
    specific events occur, such as starting, stopping, peer connection, peer
    disconnection) and receipt of messages.
    """

    # Concrete endpoint implementations must define the protocol object to
    # be instantiated to handle a connection with a peer. The protocol is
    # expected to inherit from the
    # :ref:`gestalt.stream.protocols.base.BaseStreamProtocol` interface.
    protocol_class: Optional[Type[BaseStreamProtocol]] = None

    is_server: bool = False

    def __init__(
        self,
        on_message=None,
        on_started=None,
        on_stopped=None,
        on_peer_available=None,
        on_peer_unavailable=None,
        content_type: str = serialization.CONTENT_TYPE_DATA,
        backoff_maximum: float = 10.0,
        loop=None,
        **kwargs,
    ) -> None:
        """ Initialise stream endpoint

        :param on_message: A callback function that will be called when a
          protocol extracts a message from the stream.

        :param on_started: A callback that will be called when the endpoint has
          been started. This callback simply notifies that the endpoint has been
          started and does not necessarily indicate that the endpoint is ready to
          send and receive messages. Use the `on_peer_available` method to know
          when the endpoint is ready to send or receive messages.

        :param on_stopped: A callback that will be called when the endpoint has
          been stopped.

        :param on_peer_available: A callback function that will be called when
          the protocol is connected with a transport. In this state the protocol
          can send or receive messages.

        :param on_peer_unavailable: A callback function that will be called when
          the protocol has lost the connection with its transport. In this state
          the protocol can not send or receive messages.

        :param content_type: A string argument that specifies the mime-type of
          message data. From this a serialization name will be resolved. This
          will be used to convert messages to and from wire format. Default
          value is :const:`serialization.CONTENT_TYPE_DATA` which is suitable
          for sending bytes data that has already been serialized before being
          passed to the endpoint.

        :param backoff_maximum: The maximum interval between reconnect attempts
          by an endpoint operating in client mode. Reconnect attempts backoff
          exponentially up to this maximum value. Default value is 10.0 seconds.
        """
        self.loop = loop or asyncio.get_event_loop()
        self._on_message_handler = on_message
        self._on_started_handler = on_started
        self._on_stopped_handler = on_stopped
        self._on_peer_available_handler = on_peer_available
        self._on_peer_unavailable_handler = on_peer_unavailable

        codec = serialization.registry.get_codec(content_type)
        self.content_type = codec.content_type
        self.serialization_name = serialization.registry.type_to_name[content_type]
        self.content_encoding = codec.content_encoding

        if self.protocol_class is None:
            raise Exception("protocol_class is not defined")

        if not issubclass(self.protocol_class, BaseStreamProtocol):
            raise Exception(
                f"Endpoint protocol class must be a subclass of BaseStreamProtocol, got {self.protocol_class}"
            )

        self._mode = (
            StreamEndpointModes.Server if self.is_server else StreamEndpointModes.Client
        )
        self._mode_str = self._mode.name
        self._peers = {}  # type: Dict[bytes, BaseStreamProtocol]
        self._addr = ""
        self._port = 0
        self._family = None  # type: Optional[int]
        self._ssl = None  # type: Optional[SSLContext]

        self._running = False

        # Client specific attributes
        self._reconnect = False
        self._backoff = 0.0
        self._backoff_maximum = backoff_maximum
        self._connect_task = None  # type: Optional[asyncio.Task]

        # Server specific attributes
        self._listener = None  # type: Optional[asyncio.AbstractServer]
        self._listener_addr = None  # type: Optional[Tuple[str, int]]

    @property
    def mode(self):
        """ Return the endpoint operating mode """
        return self._mode

    @property
    def running(self):
        """ Return the running state of the endpoint.

        A running endpoint simply indicates that the endpoint has been started.
        A running client endpoint may not actually be connected as it may be
        attempting reconnects, etc.
        """
        return self._running

    @property
    def bindings(self) -> Sequence[Tuple[str, int]]:
        """ Return a server endpoint's bound addresses. """
        return [self._listener_addr] if self._listener_addr else []

    @property
    def connections(self) -> Sequence[Tuple[str, int]]:
        """ Return a client endpoint's connect addresses """
        return [prot.raddr for _prot_id, prot in self._peers.items()]

    def register_message(self, type_identifier: int, obj: Any):
        """
        Register a message object with a unique message identifier.

        :param type_identifier: A message type identifier to use for the
          object.

        :param obj: The message object to associate with the identifier.
        """
        serializer = serialization.registry.get_serializer(self.serialization_name)
        serializer.registry.register_message(obj, type_identifier=type_identifier)

    async def start(
        self,
        addr: str = "",
        port: int = 0,
        family: int = socket.AF_INET,
        ssl: Optional[SSLContext] = None,
        reconnect: bool = True,
    ) -> None:
        """ Start endpoint.

        For a client endpoint this would initiate a connection attempt to
        the specified address. For a server endpoint this would attempt to
        bind the server socket to a port.

        :param addr: The address to connect or bind to. Defaults to an empty
          string which means all interfaces.

        :param port: The port to connect or bind to. Defaults to 0 which
          results in an ephemeral port being used.

        :param family: An optional address family integer from the socket module.
          Defaults to socket.AF_INET IPv4.

        :param ssl: an optional sslContext for use with TLS.

        :param reconnect: A boolean flag that determines whether a client
          endpoint should automatically attempt to reconnect if the connection
          is dropped. Only used for endpoints operating in client mode.
          Defaults to True.
        """
        if self.running:
            return

        logger.debug(f"Starting {self._mode_str}")

        self._addr = addr
        self._port = port
        self._family = family
        self._ssl = ssl
        self._reconnect = reconnect

        if self.is_server:
            await self._listen(addr=addr, port=port, family=family, ssl=ssl)
        else:
            self._connect_task = self.loop.create_task(
                self._connect(
                    addr=addr,
                    port=port,
                    family=family,
                    ssl=ssl,
                    reconnect=reconnect,
                    initial=True,
                )
            )

    async def stop(self):
        """ Stop endpoint.

        A client endpoint will disconnect and halt any further reconnection
        attempts. A server endpoint will unbind its listening socket to prevent
        any further connection and then disconnect any existing client
        connections.

        """
        logger.debug(f"Stopping {self._mode_str}")

        if self.is_server:
            # Close listener to prevent any more client connections
            if self._listener:
                self._listener.close()
                await self._listener.wait_closed()
            self._listener = None
        else:
            # Prevent automatic reconnects upon disconnect
            self._reconnect = False

            # Cancel any in-progress connection tasks
            if self._connect_task:
                self._connect_task.cancel()
            self._connect_task = None

        await self._disconnect_peers()

        self._addr = ""
        self._port = 0
        self._family = None
        self._ssl = None
        self._backoff = 0.0

        if self.running:
            self._running = False

            # Don't let poor user code break the library
            try:
                if self._on_stopped_handler:
                    self._on_stopped_handler(self)
            except Exception:
                logger.exception("Error in on_stopped callback method")

    def send(
        self, data: bytes, *, peer_id: bytes = None, type_identifier: int = 0, **kwargs
    ):
        """ Send a message to one or more peers.

        :param data: a bytes object containing the message payload.

        :param peer_id: The unique peer identity to send this message to. If
          no peer_id is specified then send to all peers. For a client
          endpoint, which typically has a single peer, this argument can
          conveniently be left unspecified.

        :param type_identifier: An optional parameter specifying the message
          type identifier. If supplied this integer value will be encoded
          into the message frame header.

        """
        if not self._peers:
            logger.error(f"No peers to send message to!")
            return

        _content_type, _content_encoding, data = serialization.dumps(
            data, self.serialization_name
        )

        if not isinstance(data, bytes):
            logger.error(f"data must be bytes - can't send message. data={data}")
            return

        peer_ids = [peer_id] if peer_id else list(self._peers)

        for _peer_id in peer_ids:
            prot = self._peers[_peer_id]
            prot.send(data, type_identifier=type_identifier, **kwargs)

    def _protocol_factory(self):
        """ Return a protocol instance to handle a new peer connection """
        return self.protocol_class(  # pylint: disable=not-callable
            on_message=self.on_message,
            on_peer_available=self.on_peer_available,
            on_peer_unavailable=self.on_peer_unavailable,
        )

    async def _listen(
        self, addr: str, port: int, family: int = socket.AF_INET, ssl: SSLContext = None
    ) -> None:
        """ Bind server to begin handling client connections.

        :param addr: The address to bind to. Defaults to an empty string which
          means all interfaces.

        :param host: The port to bind to. Defaults to 0 which results in an
          ephemeral port being used.

        :param family: An optional address family integer from the socket
          module. Defaults to 0.

        :param ssl: an optional sslContext for use with TLS.

        """
        logger.debug(f"Starting to listen on {addr}:{port}")

        try:
            self._listener = await self.loop.create_server(  # type: ignore
                self._protocol_factory, host=addr, port=port, family=family, ssl=ssl
            )

            assert self._listener is not None
            _laddr = self._listener.sockets[0].getsockname()  # type: ignore
            # Depending on the socket family, the address may be a 2-tuple for
            # IPv4 or a 4-tuple for IPv6. Currently the library is supporting
            # IPv4 only. # AF_INET6 returns a four-tuple (host, port, flowinfo,
            # scopeid) which needs to be converted to the expected 2-tuple.
            if len(_laddr) == 4:
                host, port, flowinfo, scopeid = _laddr
                _laddr = (host, port)
            self._listener_addr = _laddr
            logger.debug(f"Bound listener to {self._listener_addr}")

            self._running = True

            # Don't let poor user code break the library
            try:
                if self._on_started_handler:
                    self._on_started_handler(self)
            except Exception as exc:
                logger.exception("Error in on_started callback method")

        except Exception as exc:
            err_str = f"Unexpected error binding to {addr}:{port}: {exc}"
            logger.error(err_str)
            raise Exception(err_str) from None

    async def _connect(
        self,
        addr: str,
        port: int,
        family: int = socket.AF_INET,
        ssl: SSLContext = None,
        reconnect: bool = True,
        initial: bool = False,
    ) -> None:
        """ Connect the client to a server

        :param addr: The address to connect to.

        :param host: The port to connect to.

        :param family: An optional address family integer from the socket
          module. Defaults to socket.AF_INET IPv4.

        :param ssl: an optional sslContext for use with TLS.

        :param reconnect: A boolean flag that determines whether the
          connection should automatically attempt to reconnect. Default
          value is True.

        :param initial: When set to True the endpoint will bypass the normal
          connection backoff duration. Useful for the first connection
          attempt. Default value is False.
        """
        logger.debug(f"Starting to connect to {addr}:{port}")

        # Start from a clean state
        await self._disconnect_peers()

        if not initial:
            # A small amount of jitter is added to the connection backoff time, to
            # help improve performance in situations where thousands of clients
            # simultaneously disconnect from a service and attempt to reconnect.
            jitter = self._backoff * BACKOFF_JITTER
            min_backoff_value = max(0, self._backoff - jitter)
            max_backoff_value = self._backoff + jitter
            backoff_duration = random.uniform(min_backoff_value, max_backoff_value)
            if backoff_duration:
                logger.info(
                    f"Waiting {backoff_duration:.1f} seconds before connection attempt"
                )
                # Endpoint may be stopped while performing a reconnection
                # backoff wait. Handle this gracefully.
                try:
                    await asyncio.sleep(backoff_duration)
                except asyncio.CancelledError:
                    return

            # Determine the next backoff time up to a maximum. E.g. 1.0, 2.5, 4.74...
            self._backoff = min(
                self._backoff_maximum, self._backoff + (self._backoff / 2) + 1
            )

        _protocol = None
        try:
            _transport, _protocol = await self.loop.create_connection(  # type: ignore
                self._protocol_factory, host=addr, port=port, ssl=ssl, family=family
            )
            # Upon a successful connection the protocol will call the
            # on_peer_available method at which point the endpoint will
            # store a reference to the protocol along with the peer_id.
            # Hence, a reference to the protocol is not stored for now.

            # Reset some attributes upon successful connection
            self._backoff = 0
            self._connect_task = None

            self._running = True

            try:
                if self._on_started_handler:
                    self._on_started_handler(self)
            except Exception as exc:
                logger.exception("Error in on_started callback method")

        except (ConnectionRefusedError, OSError) as exc:
            # When connecting to "localhost", some systems try to connect to
            # both 127.0.0.1 and ::1 resulting in an OSError(Multiple errors
            # occurred) that wraps two ConnectionRefusedErrors
            logger.error(f"Connection to {addr}:{port} was refused")
        except Exception as exc:
            logger.error(f"Unexpected error connecting to {addr}:{port}", exc_info=exc)

        if _protocol is None and reconnect:
            self._connect_task = self.loop.create_task(
                self._connect(
                    addr=addr, port=port, family=family, ssl=ssl, reconnect=reconnect
                )
            )
        else:
            self._backoff = 0

    async def _disconnect_peers(self):
        """ Disconnect peers """
        for prot in list(self._peers.values()):
            prot.close()
            # Allow event loop to briefly iterate so that transport can close
            await asyncio.sleep(0)

    def on_peer_available(self, prot, peer_id: bytes):
        """ Called from a protocol instance when its transport is available.

        This means that the peer is ready for sending or receiving messages.

        :param prot: The protocol instance responsible for the peer.

        :param peer_id: The peer's unique identity.
        """
        self._peers[peer_id] = prot

        # Don't let poor user code break the library
        try:
            if self._on_peer_available_handler:
                self._on_peer_available_handler(self, peer_id)
        except Exception:
            logger.exception("Error in on_peer_available callback method")

    def on_peer_unavailable(self, prot, peer_id: bytes):
        """ Called from a protocol instance when its transport is no longer
        available. No further messages can be sent or received from the peer.

        :param prot: The protocol instance responsible for the peer.

        :param peer_id: The peer's unique identity.
        """
        # peer connection sequence may never have reached
        try:
            del self._peers[peer_id]
        except KeyError:
            pass

        # Don't let poor user code break the library
        try:
            if self._on_peer_unavailable_handler:
                self._on_peer_unavailable_handler(self, peer_id)
        except Exception:
            logger.exception("Error in on_peer_unavailable callback method")

        if not self.is_server:
            if self._reconnect:
                assert isinstance(self._family, int)  # satisfy mypy type checker
                self._connect_task = self.loop.create_task(
                    self._connect(
                        addr=self._addr,
                        port=self._port,
                        family=self._family,
                        ssl=self._ssl,
                        reconnect=self._reconnect,
                    )
                )

    def on_message(self, prot, peer_id: bytes, data: bytes, **kwargs) -> None:
        """ Called by a protocol when it receives a message from a peer.

        :param prot: The protocol instance the received the message.

        :param peer_id: The peer's unique identity which can be used to route
          messages back to the originator.

        :param data: The message payload.
        """
        if self._on_message_handler:

            type_identifier = kwargs.get("type_identifier")
            data = serialization.loads(
                data,
                content_type=self.content_type,
                content_encoding=self.content_encoding,
                type_identifier=type_identifier,
            )

            try:
                maybe_awaitable = self._on_message_handler(
                    self, data, peer_id=peer_id, **kwargs
                )
                if inspect.isawaitable(maybe_awaitable):
                    self.loop.create_task(maybe_awaitable)
            except Exception:
                logger.exception(f"Error in on_message callback method")
                return


class StreamServer(StreamEndpoint):
    """ An endpoint configured to operate as a server """

    is_server = True


class StreamClient(StreamEndpoint):
    """ An endpoint configured to operate as a client """
