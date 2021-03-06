#!/usr/bin/python3 -u
import sys

from ncclient import manager, transport
from ncclient import NCClientError
from lxml import etree
# To send commands to unit we need to send xml elements to the unit via the channel.dispatch
# the element needs to be in xml format so we need to use lxml to generate it. In the examples on the web
# they use the to_ele but we are going to generate it with the lxml library to keep overhead to the minimum.
# example:
# To hash a password we need to generate a xml as follows:
# <crypt-password xmlns="http://siklu.com/yang/tg/user-management" xmlns:rb-tg-um="http://siklu.com/yang/tg/user-management">
#   <password>admin</password>
# </crypt-password>
# once we have it we just need to send the connection object.channel.dispatch

class SikluNetconf():

    def __init__(self, ip_, user_='admin', password_='admin', port_=22, timeout_=5, device_params_={'name': 'nexus'},
                 hostkey_verify_=False):

        self.ip = ip_
        self.username = user_
        self.password = password_
        self.port = port_
        self.timeout = timeout_
        self.device_params = device_params_
        self.host_key = hostkey_verify_
        self.channel = None
        self.log_message = ''

    def set_connection_timeout(self, time_out_):
        self.timeout = time_out_

    def get_connection_timeout(self):
        return self.timeout

    def set_channel_timeout(self, timeout_):
        if self.channel:
            self.channel.timeout = timeout_

    def get_command(self, command_):
        """
                This fuction will send the commands to the radio via NetCONF.
                :param command_:
                Command will be the command to check, working on execution
                :return:
                tree output
                """
        try:
            if self.channel:
                answer = self.channel.get(command_)
                return answer
            return None
        except NCClientError as e:
            return None

    def connect(self):
        """
        Creates a connection with the given parameters via a Netconf Shell.
        By default it will auto add keys
        :return: True if connection successfully connected, False if not
        """
        try:
            self.channel = manager.connect(host=self.ip,
                                           port=self.port,
                                           username=self.username,
                                           password=self.password,
                                           device_params=self.device_params,
                                           hostkey_verify=self.host_key,
                                           timeout=self.timeout)
            return True
        except transport.SSHError as e:
            print(f'Could not connect. Please check the device is enabled.\nActual python error: {e}')
            return False
        except transport.AuthenticationError as e:
            print(f'Could not connect. Bad user/pass combination. Please review.\nActual python error: {e}')
            return False
        except transport.TransportError as e:
            print(f'Connection suddenly broke\nActual python error: {e}')
            return False
        except NCClientError as e:
            print(f'Something went wrong...oops\nActual python error: {e}')
            return False

    def close(self):
        self.channel.close_session()


if __name__ == '__main__':
    ip = sys.argv[1]
    namespace = sys.argv[2]
    path = sys.argv[3]

    n366 = SikluNetconf(ip, 'admin', 'admin')
    if n366.connect():
        n366.set_channel_timeout(3)
        n366_active = n366.get_command(
            f'<filter xmlns:n366="{namespace}" select="{path}" type="xpath"/>')
        data = bytes(n366_active.data_xml, 'utf-8')
        root = etree.fromstring(data)
        answer = root.xpath('.//text()')
        if len(root.xpath('.//text()')) > 0:
            print(answer[-1])
        n366.close()
