#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2012-2015 clowwindy
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from ssshare.shadowsocks import shell, daemon, eventloop, tcprelay, udprelay, asyncdns


def main(dictionary=None, str_json=None, port=None):
    shell.check_python()

    # fix py2exe
    if str_json:
        config = shell.check_and_parse_config(
            shell.parse_json_in_str(shell.remove_comment(str_json)))
    elif dictionary:
        config = shell.check_and_parse_config(dictionary)
    else:
        raise Exception('No config specified')

    if port:
        config['local_port'] = int(port)

    if not config.get('dns_ipv6', False):
        asyncdns.IPV6_CONNECTION_SUPPORT = False

    daemon.daemon_exec(config)
    # logging.info("local start with protocol[%s] password [%s] method [%s] obfs [%s] obfs_param [%s]" %
    #         (config['protocol'], config['password'], config['method'], config['obfs'], config['obfs_param']))

    try:
        # logging.info("starting local at %s:%d" %
        #              (config['local_address'], config['local_port']))

        dns_resolver = asyncdns.DNSResolver()
        tcp_server = tcprelay.TCPRelay(config, dns_resolver, True)
        udp_server = udprelay.UDPRelay(config, dns_resolver, True)
        loop = eventloop.EventLoop()
        dns_resolver.add_to_loop(loop)
        tcp_server.add_to_loop(loop)
        udp_server.add_to_loop(loop)

        # daemon.set_user(config.get('user', None))
        return [loop, tcp_server, udp_server]
        loop.run()
    except OSError as e:
        print(e)
        raise OSError(e)
    except Exception as e:
        if 'tcp_server' in locals():
            tcp_server.close(next_tick=True)
        if 'udp_server' in locals():
            udp_server.close(next_tick=True)
        if 'loop' in locals():
            loop.stop()
        shell.print_exception(e)
        raise Exception(e)


if __name__ == '__main__':
    pass
    # main()
