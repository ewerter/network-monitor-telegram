import json, subprocess, time, os, requests
from datetime import datetime

def load_config():
    with open('config.json') as f:
        return json.load(f)

def load_know_devices():
    try:
        with open('know_devices.json') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_know_devices(know_devices):
    with open('known_devices.json', 'w') as f:
        json.dump(know_devices, f, indent=4)

def log_device(ip, mac):
    with open("logs/scan_log.csv", "a") as f:
        f.write(f"{datetime.now()},{ip},{mac}\n")

def send_telegram_message(message):
    config = load_config()
    url = f"https://api.telegram.org/bot{config['telegram_token']}/sendMessage"
    payload = {
        'chat_id': config['telegram_chat_id'],
        'text': message
    }
    requests.post(url, data=payload)

def scan_network(subnet):
    print(f"[INFO] Running nmap scan on {subnet}...")
    result = subprocess.run(
        ["sudo", "nmap", "-sn", subnet], capture_output=True, text=True
    ).stdout
    print("[DEBUG] nmap output:")
    print(result)

    devices = {}
    current_ip = None
    for line in result.splitlines():
        if "Nmap scan report for" in line:
            current_ip = line.split()[-1]
        elif "MAC Address:" in line and current_ip:
            mac = line.split()[2]
            devices[mac] = current_ip
    return devices

"""    
def main():
    config = load_config()
    know = load_know_devices()
    scanned = scan_network(config['subnet'])
    new_devices ={}
    for mac, ip in scanned.items():
        if mac not in know:
            new_devices[mac] = ip
            send_telegram_message(f"New device detected: {ip} ({mac})")
            log_device(ip, mac)

        if new_devices:
            know.update(new_devices)
            save_know_devices(know)
"""
def main():
    config = load_config()
    print("[INFO] Loaded config.")

    known = load_know_devices()
    print(f"[INFO] Known devices loaded: {len(known)}")

    scanned = scan_network(config["subnet"])
    print(f"[INFO] Devices found in scan: {len(scanned)}")

    if not scanned:
        print("[WARNING] No devices found. Try running nmap with sudo or check your subnet.")
        return

    new_devices = {}

    for mac, ip in scanned.items():
        print(f"[DEBUG] Scanned device: {ip} ({mac})")
        if mac not in known:
            print(f"[NEW DEVICE] {ip} ({mac})")
            new_devices[mac] = ip
            send_telegram_message(f"New device detected: {ip} ({mac})")
            log_device(ip, mac)

    if new_devices:
        print("[INFO] Saving new devices...")
        known.update(new_devices)
        save_know_devices(known)
    else:
        print("[INFO] No new devices found.")

if __name__ == "__main__":
    main()