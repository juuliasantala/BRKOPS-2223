#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Python sample script for enabling IPv6 on multiple devices with RESTCONF.
------------

Copyright (c) 2024 Cisco and/or its affiliates.
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

requests.urllib3.disable_warnings()

def enable_ipv6(device_ip, username, password, port=443, verify=False):
    """
    Function to enable IPv6 on a network device
    """

    print(f"Enabling IPv6 on device {device_ip}...", end=" ")

    url = f"https://{device_ip}:{port}/restconf/data/Cisco-IOS-XE-native:native/ipv6/"
    header = {"Content-Type": "application/yang-data+json"}
    payload = {
        "Cisco-IOS-XE-native:ipv6": {
            "unicast-routing": [None],
            "router": {
                "ospf": [{"id": 1}]
            }
        }
    }

    response = requests.patch(url, headers=header, auth=(username, password),
                              json=payload, verify=verify)

    if response.ok:
        print("Success!")
    else:
        print("Error!")
        print(response.text)

if __name__ == "__main__":

    devices = [
        "198.18.133.101",
        "198.18.7.2",
        "198.18.11.2",
        "198.18.12.2"
    ]

    credentials = {
        "password": "C1sco12345",
        "username": "developer"
    }

    for device in devices:
        enable_ipv6(device, credentials["username"], credentials["password"])
