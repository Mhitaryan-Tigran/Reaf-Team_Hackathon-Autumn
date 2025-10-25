from scapy.all import IP, ICMP, sr1
from scapy.layers.inet import UDP
import socket

def manual_traceroute(destination, max_hops=30):
    print(f"Manual traceroute to {destination}...")
    reply_list = []

    try:
        destination_ip = socket.gethostbyname(destination)
        print(f"Destination IP: {destination_ip}")
    except socket.gaierror:
        print(f"Could not resolve hostname: {destination}")
        return

    try:
        for ttl in range(1, max_hops + 1):
            packet = IP(dst=destination_ip, ttl=ttl) / UDP(dport=33434)        

            reply = sr1(packet, verbose=0, timeout=2)

            if reply is None:
                print(f"{ttl:2d}  * * *")
            elif reply.type == 3:  
                print(f"{ttl:2d}  {reply.src} (Reached Destination)")
                break
            else:
                print(f"{ttl:2d}  {reply.src}")
                reply_list.append(reply.src)

    finally:
            print(reply_list)

if __name__ == '__main__':
    manual_traceroute("donstu.ru")
