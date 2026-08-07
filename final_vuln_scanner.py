import nmap
import tkinter as tk
from tkinter import messagebox

# -------- SCAN FUNCTION --------
def scan_target():
    target = entry.get()
    
    if target == "":
        messagebox.showerror("Error", "Please enter target IP")
        return
    
    scanner = nmap.PortScanner()
    
    output.delete(1.0, tk.END)
    output.insert(tk.END, "Scanning...\n\n")
    
    scanner.scan(target, '1-1024', arguments='-sV')
    
    risk_score = 0
    open_ports = []

    for host in scanner.all_hosts():
        output.insert(tk.END, f"Host: {host}\n")
        
        for proto in scanner[host].all_protocols():
            ports = scanner[host][proto].keys()
            
            for port in ports:
                state = scanner[host][proto][port]['state']
                service = scanner[host][proto][port].get('name', '')
                
                output.insert(tk.END, f"Port {port} ({service}) → {state}\n")
                
                if state == "open":
                    open_ports.append(port)
                    
                    if port == 21:
                        risk_score += 5
                    elif port == 22:
                        risk_score += 3
                    elif port == 80:
                        risk_score += 4

    # Risk Level
    if risk_score >= 8:
        level = "HIGH"
    elif risk_score >= 4:
        level = "MEDIUM"
    else:
        level = "LOW"

    output.insert(tk.END, "\n--- REPORT ---\n")
    output.insert(tk.END, f"Open Ports: {open_ports}\n")
    output.insert(tk.END, f"Risk Score: {risk_score}\n")
    output.insert(tk.END, f"Risk Level: {level}\n")

    # Save report
    with open("final_report.txt", "w") as f:
        f.write(f"Target: {target}\n")
        f.write(f"Open Ports: {open_ports}\n")
        f.write(f"Risk Score: {risk_score}\n")
        f.write(f"Risk Level: {level}\n")

    output.insert(tk.END, "\nReport saved as final_report.txt\n")

# -------- GUI --------
root = tk.Tk()
root.title("Vulnerability Scanner")

tk.Label(root, text="Enter Target IP:").pack()

entry = tk.Entry(root, width=30)
entry.pack()

tk.Button(root, text="Start Scan", command=scan_target).pack()

output = tk.Text(root, height=20, width=60)
output.pack()

root.mainloop()
