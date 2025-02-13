import requests
import urllib3

urllib3.disable_warnings()

def enable_ipv6(device_ip, username, password, port=443, verify=False):

    print(f"Enabling IPv6 on device {device_ip}...", end=" ")

    url = f"https://{device_ip}:{port}/restconf/data/Cisco-IOS-XE-native:native/ipv6/"
    header = {"Content-Type": "application/yang-data+json"}
    payload = {
        "Cisco-IOS-XE-native:ipv6": {"unicast-routing": [None]}
    }

    response = requests.patch(url, headers=header, auth=(username, password),
                              json=payload, verify=verify)

    if response.status_code in (200, 204):
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
