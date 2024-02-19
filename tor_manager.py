# start_tor.py
from stem import process
from termcolor import colored
def start_tor():
    print(colored("[!] Initializing TOR Services...", "yellow"))
    try:
        tor_process = process.launch_tor_with_config(
            config={
                'SocksPort': '9050',
                'ControlPort': '9051',
            },
            take_ownership=True,
        )
        print(colored("[\u2713] Tor service started successfully.", "green"))
        return tor_process
    except Exception as e:
        print(f"Error starting Tor service: {e}")
        return None

def stop_tor(tor_process):
    if tor_process:
        tor_process.kill()