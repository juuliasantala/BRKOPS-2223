import requests
import urllib3

urllib3.disable_warnings()

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
for HOST in devices:
    print(f"Configuring device {HOST}...", end=" ")
    url = f"https://{HOST}:443/restconf/data/Cisco-IOS-XE-native:native/"

    header = {"Content-Type": "application/yang-data+json"}

    response = requests.patch(url, headers=header,
                            auth=(USERNAME, PASSWORD),
                            json=payload, verify=False)

    if response.status_code in (200, 204):
        print("Success!")
    else:
        print("Error!")
        print(response.text)