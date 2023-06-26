import nmap
import ipaddress
import subprocess
import os

# Check if the 'ip_list.txt' file exists
if not os.path.isfile('ip_list.txt'):
    print(" Error: 'ip_list.txt' file not found. \n Please ensure there is a .txt file named ip_list.txt in the same directory as the Python script")
    exit(1)

# Read the list of IP addresses from the text file
with open('ip_list.txt', 'r') as file:
    ip_list = file.readlines()

# Create an Nmap scanner object
scanner = nmap.PortScanner()

# Specify the destination directory for exported files
export_dir = 'F:\\test'
os.makedirs(export_dir, exist_ok=True)

# Iterate through each IP address
for ip_str in ip_list:
    ip_str = ip_str.strip()

    # Validate and convert the IP address string to an IPv4Address object
    try:
        ip = ipaddress.IPv4Address(ip_str)
    except ipaddress.AddressValueError as e:
        print(f"Invalid IP address: {ip_str} ({e})")
        continue

    # Perform the port scan
    print(f"Scanning IP: {ip_str}...")

    try:
        scanner.scan(str(ip), arguments='-p 1-1000')  # Adjust the port range as needed
    except nmap.PortScannerError as e:
        print(f"Error while scanning IP: {ip_str} ({e})")
        continue

    # Retrieve and print the open ports
    if scanner[ip_str].state() == 'up':
        print(f"Open ports for IP: {ip_str}")
        for protocol in scanner[ip_str].all_protocols():
            ports = scanner[ip_str][protocol].keys()
            for port in ports:
                print(f"Port: {port} ({protocol}) - {scanner[ip_str][protocol][port]['name']}")

    print("-" * 40)

    # Capture XML output by running the nmap command and redirecting the output to a file
    xml_output_file = os.path.join(export_dir, f"{ip_str}.xml")
    nmap_output_file = os.path.join(export_dir, f"{ip_str}.nmap")
    cmd = f"nmap -p 1-1000 -oX {xml_output_file} -oN {nmap_output_file} {ip_str}"
    process = subprocess.run(cmd, shell=True, capture_output=True, text=True)

    if process.returncode == 0:
        print(f"XML output captured in {xml_output_file}")
        print(f"Nmap output captured in {nmap_output_file}")
    else:
        print(f"Error while running Nmap: {process.stderr}")

    print("-" * 40)