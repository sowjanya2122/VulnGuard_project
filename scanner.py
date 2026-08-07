import nmap

# INPUT
target = input("Enter Target IP: ")

# INIT SCANNER 
scanner = nmap.PortScanner()

print("\nScanning target... Please wait...\n")

scanner.scan(target, '1-5000')

# RISK SCORE
risk_score = 0

# VULNERABILITY CHECK
def check_vulnerability(port):
    if port == 21:
        return "⚠ FTP - Anonymous login possible", 5
    elif port == 22:
        return "⚠ SSH - Brute-force risk", 3
    elif port == 80:
        return "⚠ HTTP - Possible XSS/SQL Injection", 4
    elif port == 443:
        return "⚠ HTTPS - Check SSL/TLS issues", 2
    else:
        return "No major vulnerability", 0

# ATTACK SIMULATION
def simulate_attack(port):
    print("\n--- Simulating Attack ---")
    
    if port == 21:
        print("Simulating FTP anonymous login...")
        print("Username: anonymous → Access Granted (Simulation)")
    
    elif port == 22:
        print("Simulating SSH brute-force...")
        passwords = ["1234", "admin", "password"]
        for p in passwords:
            print(f"Trying password: {p}")
    
    elif port == 80:
        print("Simulating SQL Injection...")
        print("Payload: ' OR '1'='1")
    
    elif port == 443:
        print("Simulating SSL vulnerability check...")
    
    else:
        print("No simulation available")

# MAIN LOGIC
open_ports = []

for host in scanner.all_hosts():
    print(f"Host: {host}")
    
    for proto in scanner[host].all_protocols():
        ports = scanner[host][proto].keys()
        
        for port in ports:
            state = scanner[host][proto][port]['state']
            print(f"Port {port} → {state}")
            
            if state == "open":
                open_ports.append(port)
                
                vuln, score = check_vulnerability(port)
                print(f"   {vuln}")
                
                risk_score += score

# SIMULATION OPTION
simulate = input("\nDo you want to simulate attacks? (yes/no): ")

if simulate.lower() == "yes":
    for port in open_ports:
        simulate_attack(port)

# FINAL REPORT
print("\n--- FINAL REPORT ---")
print(f"Target: {target}")
print(f"Open Ports: {open_ports}")
print(f"Risk Score: {risk_score}")

# SAVE REPORT
with open("report.txt", "w") as f:
    f.write("Vulnerability Assessment Report\n")
    f.write(f"Target: {target}\n")
    f.write(f"Open Ports: {open_ports}\n")
    f.write(f"Risk Score: {risk_score}\n")

print("\nReport saved as report.txt")
