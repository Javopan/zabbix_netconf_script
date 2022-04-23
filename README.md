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
7. Use wget to save the file on the externalscripts folder  
  `wget -P /usr/lib/zabbix/externalscripts/ https://raw.githubusercontent.com/Javopan/zabbix_netconf_script/main/netconf_driver_zabbix.py`
8. Change the owner of the file to zabbix and group zabbix:  
  `chown zabbix:zabbix /usr/lib/zabbix/externalscripts/netconf_driver_zabbix.py`
9. Change the permissions to execute the file:  
  `chmod 700 /usr/lib/zabbix/externalscripts/netconf_driver_zabbix.py`
10. Restart the Zabbix services:  
  `service zabbiz-agent restart`  
  `service zabbiz-server restart`  
  We are now ready to add a host and add an external check.
11. Log in into your Zabbix instance and add a new host from
12. Configuration -> Hosts and on the upper right of the window click on Create Host
13. Fill in the data and add it to a desired group and add a description  
  In this case  
  Host name `TG`  
  Visible name `TG-Unit-0001`  
  Groups `Siklu MH TG`  
  Add an interface with the IP of the radio to monitor. The type is not important. (For this test it was agent)  
  Description `A unit to be monitored by netconf`  
  Enabled `checked`  
  ![add host](addhost.jpg "Add a host")  
14. Click Add
15. The new Host shall be in the hosts website  
  ![hosts website](hosts.jpg "Hosts website")  
16. Click on the new host that you want to configure in this case `TG-Unit-0001`
  ![host clicked](unit.jpg "Host clicked")  
17. In the upper gray ribbon click Items  
![items clicked](items.jpg "Items clicked")  
18. On the upper right corner click `Create item`
![create item](create_item.jpg "Create item")  
19. Fill in the relevan data. In this case we are using a Zabbix macro `{HOST.NAME} - system name` to give it a meaningful name of what we will poll.
20. Select from the Type list `External check`
21. 
  
