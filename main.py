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
    with open('know_devices.json', 'w') as f:
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
    result = subprocess.run(['nmap', '-sn', subnet], capture_output=True, text=True).stdout
    devices = {}
    current_ip = None
    for line in result.splitlines():
        if "Nmap scan report for" in line:
            current_ip = line.split()[-1]
        elif "MAC Address:" in line:
            mac = line.split()[2]
            devices[mac] = current_ip
    return devices
    
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

if __name__ == "__main__":
    main()