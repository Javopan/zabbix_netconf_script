# zabbix_netconf_script
A python script that will enable Zabbix to get netconf data from a unit.
This instructions are for a Linux installation of Zabbix.

The instructions were tested on Ubuntu 20.04

# install instructions  
1. Make sure you have Python 3.8+
   - On a terminal or in cli run `python3` and check the version on the output. `Python 3.8.10 (default, Mar 15 2022, 12:22:08)`
2. Install pip `apt install python3-pip`
3. Install ncclient on the linux Zabbix server. `pip install ncclient`. This also install paramiko and lxml. With this modules we will be able to open a connection to the netconf unit and poll the data.
4. Install zabbix according to the instructions from: [Zabbix](https://www.zabbix.com/download)
5. We need to enable an external check in Zabbix.  
   - To enable it, we need to modify the `zabbix_server.conf` file
   - look for the line with `#ExternalScripts=/usr/lib/zabbix/externalscripts` and uncomment it `ExternalScripts=/usr/lib/zabbix/externalscripts` and save it
6. We can save our custom scripts in `/usr/lib/zabbix/externalscripts`
7. 
