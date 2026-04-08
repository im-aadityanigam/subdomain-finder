import requests
import threading
import tkinter as tk
from tkinter import scrolledtext

def update_output(text):
    output.after(0, lambda: output.insert(tk.END, text))

def clear_output():
    output.after(0, lambda: output.delete(1.0, tk.END))

def find_subdomains():
    domain = entry.get().strip()

    if not domain:
        clear_output()
        update_output("Please enter a domain\n")
        return

    clear_output()
    update_output(f"[+] Finding subdomains for: {domain}\n\n")
    update_output("[*] Please wait...\n\n")

    url = f"https://crt.sh/?q=%25.{domain}&output=json"

    try:
        response = requests.get(url, timeout=30)

        if response.status_code != 200:
            update_output("[-] Failed to fetch data\n")
            return

        data = response.json()
        subdomains = set()

        for entry_data in data:
            name = entry_data.get("name_value")
            if name:
                for sub in name.split("\n"):
                    subdomains.add(sub.strip())

        if not subdomains:
            update_output("[-] No subdomains found or blocked\n")
            return

        for sub in sorted(subdomains):
            update_output(sub + "\n")

        update_output(f"\n[+] Total: {len(subdomains)} subdomains found\n")

    except requests.exceptions.Timeout:
        update_output("[-] Request timed out. Try again.\n")

    except Exception as e:
        update_output(f"Error: {e}\n")

def start_scan():
    thread = threading.Thread(target=find_subdomains)
    thread.daemon = True
    thread.start()

# GUI
root = tk.Tk()
root.title("Subdomain Finder")
root.geometry("700x500")
root.configure(bg="#1e1e1e")

title = tk.Label(root, text="Subdomain Finder", font=("Arial", 18, "bold"), fg="white", bg="#1e1e1e")
title.pack(pady=10)

entry = tk.Entry(root, width=50, font=("Arial", 12))
entry.pack(pady=10)

btn = tk.Button(root, text="Find Subdomains", command=start_scan, bg="#007acc", fg="white", font=("Arial", 12))
btn.pack(pady=5)

output = scrolledtext.ScrolledText(root, width=80, height=20, bg="#2d2d2d", fg="white")
output.pack(pady=10)

root.mainloop()