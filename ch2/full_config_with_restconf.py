#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Simple Python sample script for enabling IPv6 and interface configuration
on multiple devices with RESTCONF.
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

devices = [
    "198.18.7.2",
    "198.18.11.2",
    "198.18.12.2"
]

PASSWORD = "C1sco12345"
USERNAME = "developer"

payload = {
    "Cisco-IOS-XE-native:native": {
        "ipv6": {
            "unicast-routing": [None],
            "router": {
                "ospf": [{"id": 1}]
            }
        },
        "interface": {
            "GigabitEthernet": [
                {
                    "name": "4",
                    "ipv6": {
                        "enable":[None],
                        "Cisco-IOS-XE-ospfv3:ospf": {
                            "process": {
                                "id": "1",
                                "area": "0"
                            }
                        }
                    }
                 },
                 {
                    "name": "5",
                    "ipv6": {
                        "enable":[None],
                        "Cisco-IOS-XE-ospfv3:ospf": {
                            "process": {
                                "id": "1",
                                "area": "0"
                            }
                        }
                    }
                 },
                 {
                    "name": "6",
                    "ipv6": {
                        "enable":[None],
                        "Cisco-IOS-XE-ospfv3:ospf": {
                            "process": {
                                "id": "1",
                                "area": "0"
                            }
                        }
                    }
                 }
            ]
        }
    }
}

for host in devices:
    print(f"Configuring device {host}...", end=" ")
    url = f"https://{host}:443/restconf/data/Cisco-IOS-XE-native:native/"

    header = {"Content-Type": "application/yang-data+json"}

    response = requests.patch(url, headers=header,
                            auth=(USERNAME, PASSWORD),
                            json=payload, verify=False)

    if response.ok:
        print("Success!")
    else:
        print("Error!")
        print(response.text)
