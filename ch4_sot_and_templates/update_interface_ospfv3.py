#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Python sample script for updating interface OSPFv3 configuration with RESTCONF.

------------

Copyright (c) 2025 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at

               https://developer.cisco.com/docs/licenses

All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
"""

import requests
import urllib3
import yaml
import jinja2

__author__ = "Juulia Santala"
__email__ = "jusantal@cisco.com"
__copyright__ = "Copyright (c) 2025 Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.1"

# Following line disables warnings of the unverified certificate. Do not use in production!
urllib3.disable_warnings()

def render_template(ospfv3:list, template_name:str):
    with open(template_name, encoding="utf-8") as my_template:
        template = jinja2.Template(my_template.read())
    configuration = template.render(ospfv3=ospfv3)
    print(f"Configuration to be sent: \n {configuration}")
    return configuration

def configure_interface(device_ip:str, username:str, password:str,
                        configuration:dict, interface_id: str,
                        port:int=443, verify:bool=False)->None:
    '''
    Function to configure interface on an IOS XE device using RESTCONF.
    '''
    print(f"Configuring interfaces GigabitEthernet {interface_id}...", end=" ")

    url = f"https://{device_ip}:{port}/restconf/data/Cisco-IOS-XE-native:native/interface/GigabitEthernet={interface_id}/ipv6/Cisco-IOS-XE-ospfv3:ospf"
    header = {"Content-Type": "application/yang-data+json"}
    payload = render_template(ospfv3=configuration, template_name="interface_ospfv3.j2")

    response = requests.patch(url, headers=header, auth=(username, password),
                              data=payload, verify=verify)

    if response.ok:
        print("Success!")
    else:
        print("Error!")
        print(response.text)


def read_configuration_template(config_file: str="ipv6_config.yaml"):
    with open(config_file, encoding="utf-8") as my_values:
        config = yaml.safe_load(my_values.read())
    return config["devices"]

def main():
    devices_config = read_configuration_template()

    devices = {
        "R1":"198.18.133.101",
        "R2":"198.18.7.2",
        "R3":"198.18.11.2",
        "R4":"198.18.12.2"
    }

    credentials = {
        "password": "C1sco12345",
        "username": "developer"
    }


    print("# Enabling OSPFv3 for interfaces")
    for device, config in devices_config.items():
        print(f"Device: {device} {devices[device]}")
        for interface in config["interfaces"]:
            if "ospfv3" in interface:
                print("\n#######\n")
                configure_interface(
                    device_ip=devices[device],
                    username=credentials["username"],
                    password=credentials["password"],
                    configuration=interface["ospfv3"],
                    interface_id=interface["number"]
                )

if __name__ == "__main__":
    main()