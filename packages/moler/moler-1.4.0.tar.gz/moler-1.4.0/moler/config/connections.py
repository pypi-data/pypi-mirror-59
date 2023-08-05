# -*- coding: utf-8 -*-
"""
Connections related configuration
"""

__author__ = 'Grzegorz Latuszek, Michal Ernst'
__copyright__ = 'Copyright (C) 2018, Nokia'
__email__ = 'grzegorz.latuszek@nokia.com, michal.ernst@nokia.com'

import sys
import platform
from moler.exceptions import MolerException


default_variant = {}
named_connections = {}


def set_default_variant(io_type, variant):
    """Set variant to use as default when requesting 'io_type' connection"""
    default_variant[io_type] = variant


def define_connection(name, io_type, **constructor_kwargs):
    """
    Assign name to connection specification.

    You should provide name that is meaningful in context of your application.
    Let's say you have 3 servers hosting HTTP under 10.20.30.41 .. 43
    Then you may name/define your connections like::

        www_svr1  io_type=tcp, host=10.20.30.41, port=80
        www_svr2  io_type=tcp, host=10.20.30.42, port=80
        www_svr3  io_type=tcp, host=10.20.30.43, port=80

    Thanks to such naming you could establish connection to server like::

        svr1_conn = get_connection(name="www_svr_1")
        svr1_conn.open()
    """
    named_connections[name] = (io_type, constructor_kwargs)


def clear():
    """Cleanup configuration related to connections"""
    default_variant.clear()
    named_connections.clear()


def set_defaults():
    """Set defaults for connections configuration"""
    set_default_variant(io_type="terminal", variant="threaded")


def _running_python_3_5_or_above():
    return (sys.version_info[0] >= 3) and (sys.version_info[1] >= 5)


supported_systems = ['Linux', "FreeBSD", "Darwin", "SunOS"]


def _running_on_supported_unix():
    return platform.system() in supported_systems


def register_builtin_connections(connection_factory, moler_conn_class):
    _register_builtin_connections(connection_factory, moler_conn_class)
    if _running_python_3_5_or_above():
        _register_python3_builtin_connections(connection_factory, moler_conn_class)

    if _running_on_supported_unix():
        _register_builtin_unix_connections(connection_factory, moler_conn_class)
        if _running_python_3_5_or_above():
            _register_builtin_py3_unix_connections(connection_factory, moler_conn_class)
    else:
        # who has added this? On Windows - just terminal connection is absent
        #
        # err_msg = "Unsupported system {} detected! Supported systems: {}".format(platform.system(), supported_systems)
        # raise MolerException(err_msg)
        pass


def mlr_conn_no_encoding(moler_conn_class, name):
    return moler_conn_class(name=name)


def mlr_conn_utf8(moler_conn_class, name):
    return moler_conn_class(encoder=lambda data: data.encode("utf-8"),
                            decoder=lambda data: data.decode("utf-8"),
                            name=name)


def _register_builtin_connections(connection_factory, moler_conn_class):
    from moler.io.raw.memory import ThreadedFifoBuffer
    from moler.io.raw.tcp import ThreadedTcp

    def mem_thd_conn(name=None, echo=True, **kwargs):  # kwargs to pass  logger_name
        mlr_conn = mlr_conn_utf8(moler_conn_class, name=name)
        io_conn = ThreadedFifoBuffer(moler_connection=mlr_conn,
                                     echo=echo, name=name, *kwargs)
        return io_conn

    def tcp_thd_conn(port, host='localhost', name=None, **kwargs):  # kwargs to pass  receive_buffer_size and logger
        mlr_conn = mlr_conn_utf8(moler_conn_class, name=name)
        io_conn = ThreadedTcp(moler_connection=mlr_conn,
                              port=port, host=host, **kwargs)  # TODO: add name
        return io_conn

    # TODO: unify passing logger to io_conn (logger/logger_name - see above comments)
    connection_factory.register_construction(io_type="memory",
                                             variant="threaded",
                                             constructor=mem_thd_conn)
    connection_factory.register_construction(io_type="tcp",
                                             variant="threaded",
                                             constructor=tcp_thd_conn)


def _register_python3_builtin_connections(connection_factory, moler_conn_class):
    from moler.io.asyncio.tcp import AsyncioTcp, AsyncioInThreadTcp

    def tcp_asyncio_conn(port, host='localhost', name=None, **kwargs):  # kwargs to pass  receive_buffer_size and logger
        mlr_conn = mlr_conn_utf8(moler_conn_class, name=name)
        io_conn = AsyncioTcp(moler_connection=mlr_conn,
                             port=port, host=host, **kwargs)  # TODO: add name
        return io_conn

    def tcp_asyncio_in_thrd_conn(port, host='localhost', name=None, **kwargs):  # kwargs to pass  receive_buffer_size and logger
        mlr_conn = mlr_conn_utf8(moler_conn_class, name=name)
        io_conn = AsyncioInThreadTcp(moler_connection=mlr_conn,
                                     port=port, host=host, **kwargs)  # TODO: add name
        return io_conn

    # TODO: unify passing logger to io_conn (logger/logger_name - see above comments)
    connection_factory.register_construction(io_type="tcp",
                                             variant="asyncio",
                                             constructor=tcp_asyncio_conn)
    connection_factory.register_construction(io_type="tcp",
                                             variant="asyncio-in-thread",
                                             constructor=tcp_asyncio_in_thrd_conn)


def _register_builtin_unix_connections(connection_factory, moler_conn_class):
    from moler.io.raw.terminal import ThreadedTerminal

    def terminal_thd_conn(name=None):
        # ThreadedTerminal works on unicode so moler_connection must do no encoding
        mlr_conn = mlr_conn_no_encoding(moler_conn_class, name=name)
        io_conn = ThreadedTerminal(moler_connection=mlr_conn)  # TODO: add name, logger
        return io_conn

    # TODO: unify passing logger to io_conn (logger/logger_name)
    connection_factory.register_construction(io_type="terminal",
                                             variant="threaded",
                                             constructor=terminal_thd_conn)


def _register_builtin_py3_unix_connections(connection_factory, moler_conn_class):
    from moler.io.asyncio.terminal import AsyncioTerminal, AsyncioInThreadTerminal

    def terminal_asyncio_conn(name=None):
        mlr_conn = mlr_conn_utf8(moler_conn_class, name=name)
        io_conn = AsyncioTerminal(moler_connection=mlr_conn)  # TODO: add name, logger
        return io_conn

    def terminal_asyncio_in_thrd_conn(name=None):
        mlr_conn = mlr_conn_utf8(moler_conn_class, name=name)
        io_conn = AsyncioInThreadTerminal(moler_connection=mlr_conn)  # TODO: add name, logger
        return io_conn

    # TODO: unify passing logger to io_conn (logger/logger_name)
    connection_factory.register_construction(io_type="terminal",
                                             variant="asyncio",
                                             constructor=terminal_asyncio_conn)
    connection_factory.register_construction(io_type="terminal",
                                             variant="asyncio-in-thread",
                                             constructor=terminal_asyncio_in_thrd_conn)
