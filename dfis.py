import os

def show_banner():
    banner = r"""
██████╗ ███████╗██╗███████╗
██╔══██╗██╔════╝██║██╔════╝
██║  ██║█████╗  ██║███████╗
██║  ██║██╔══╝  ██║╚════██║
██████╔╝██║     ██║███████║
╚═════╝ ╚═╝     ╚═╝╚══════╝

      DIGITAL FORENSIC INVESTIGATION SYSTEM

                  Version 1.1

     Live Forensics • Dump Analysis • SHA-256 Integrity

══════════════════════════════════════════════════════════════
"""
    print(banner)

import hashlib
from datetime import datetime
from datetime import datetime


# ------------------ PATH CONFIG ------------------

BASE_DIR = "DFIS_Case_" + datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
EVIDENCE_DIR = BASE_DIR + "/evidence/system"
ANALYSIS_DIR = BASE_DIR + "/analysis/system"
INTEGRITY_DIR = BASE_DIR + "/integrity"
REPORT_DIR = BASE_DIR + "/report"
NETWORK_DIR = BASE_DIR + "/network"
LOG_DIR = BASE_DIR + "/logs"
DUMP_DIR = BASE_DIR + "/dump_analysis"

def log_action(action):

    os.makedirs(LOG_DIR, exist_ok=True)

    log_file = LOG_DIR + "/investigation_log.txt"

    timestamp = datetime.now().strftime("%H:%M:%S")

    with open(log_file, "a") as log:
        log.write("[" + timestamp + "] " + action + "\n")

# ------------------ EVIDENCE ACQUISITION ------------------

def evidence_acquisition():

    log_action("Evidence Acquisition Started")

    os.makedirs(EVIDENCE_DIR, exist_ok=True)

    os.system("date > " + EVIDENCE_DIR + "/system_time.txt")
    os.system("uname -a > " + EVIDENCE_DIR + "/os_kernel_info.txt")
    os.system("cat /etc/os-release > " + EVIDENCE_DIR + "/os_release.txt")
    os.system("who > " + EVIDENCE_DIR + "/logged_in_users.txt")
    os.system("last > " + EVIDENCE_DIR + "/login_history.txt")
    os.system("ps aux > " + EVIDENCE_DIR + "/running_processes.txt")
    os.system("lsusb > " + EVIDENCE_DIR + "/usb_devices.txt")
    os.system("hostname > " + EVIDENCE_DIR + "/hostname.txt")
    os.system("df -h > " + EVIDENCE_DIR + "/disk_usage.txt")
    os.system("mount > " + EVIDENCE_DIR + "/mounted_devices.txt")
    os.system("free -h > " + EVIDENCE_DIR + "/memory_info.txt")
    os.system("cat /etc/passwd > " + EVIDENCE_DIR + "/user_accounts.txt")
    os.system("env > " + EVIDENCE_DIR + "/environment_variables.txt")
    
    log_action("Evidence Acquisition Completed")

    print("\n[+] Evidence acquisition completed.\n")


# ------------------ SYSTEM ANALYSIS ------------------

def system_analysis():

    log_action("System Analysis Completed")

    os.makedirs(ANALYSIS_DIR, exist_ok=True)

    os.system("systemctl list-units --type=service > " + ANALYSIS_DIR + "/running_services.txt")
    os.system("ss -tulnp > " + ANALYSIS_DIR + "/open_ports.txt")
    os.system("uptime > " + ANALYSIS_DIR + "/system_uptime.txt")
    os.system("ps aux --sort=-%cpu | head -n 15 > " + ANALYSIS_DIR + "/top_cpu_processes.txt")
    os.system("ps aux --sort=-%mem | head -n 15 > " + ANALYSIS_DIR + "/top_memory_processes.txt")
    os.system("ps -eo pid,lstart,cmd --sort=start_time | tail -n 15 > " + ANALYSIS_DIR + "/recent_processes.txt")

    log_action("Network Analysis Completed")

    print("\n[+] System analysis completed.\n")

# -----------------NETWORK ANALYSIS-----------------
def network_analysis():

    os.makedirs(NETWORK_DIR, exist_ok=True)

    os.system("ip a > " + NETWORK_DIR + "/network_interfaces.txt")
    os.system("ss -tunap > " + NETWORK_DIR + "/active_connections.txt")
    os.system("netstat -rn > " + NETWORK_DIR + "/routing_table.txt")
    os.system("ss -lntp > " + NETWORK_DIR + "/listening_ports.txt")
    os.system("ss -tunap | grep ESTAB > " + NETWORK_DIR + "/established_connections.txt")

    log_action("Network Analysis Completed")

    print("\n[+] Network analysis completed.\n")

# ------------------ HASH GENERATION ------------------

def generate_hashes():

    os.makedirs(INTEGRITY_DIR, exist_ok=True)

    hash_path = INTEGRITY_DIR + "/system_hashes.txt"

    with open(hash_path, "w") as hash_file:

        for folder in [EVIDENCE_DIR, ANALYSIS_DIR]:

            if os.path.exists(folder):

                for file in os.listdir(folder):

                    filepath = os.path.join(folder, file)

                    sha256 = hashlib.sha256()

                    with open(filepath, "rb") as f:

                        while True:

                            data = f.read(4096)

                            if not data:
                                break

                            sha256.update(data)

                    hash_file.write(file + " : " + sha256.hexdigest() + "\n")

    log_action("Evidence Integrity Verification Completed")

    print("\n[+] Evidence integrity verified using SHA-256.\n")

def verify_hashes():

    print("\nVerifying evidence integrity...\n")

    hash_file = INTEGRITY_DIR + "/system_hashes.txt"

    if not os.path.exists(hash_file):
        print("No hash file found. Run hash generation first.")
        return

    with open(hash_file) as f:

        for line in f:

            parts = line.strip().split(" : ")

            if len(parts) != 2:
                continue

            filename, stored_hash = parts

            filepath_evidence = os.path.join(EVIDENCE_DIR, filename)
            filepath_analysis = os.path.join(ANALYSIS_DIR, filename)

            filepath = None

            if os.path.exists(filepath_evidence):
                filepath = filepath_evidence
            elif os.path.exists(filepath_analysis):
                filepath = filepath_analysis

            if filepath:

                sha256 = hashlib.sha256()

                with open(filepath, "rb") as file:
                    while True:
                        data = file.read(4096)
                        if not data:
                            break
                        sha256.update(data)

                current_hash = sha256.hexdigest()

                if current_hash == stored_hash:
                    print(filename + " → VERIFIED")
                else:
                    print(filename + " → WARNING: FILE MODIFIED!")

    log_action("Evidence Integrity Verified")     




# ------------------ REPORT GENERATION ------------------

def generate_report():

    log_action("Report Generation Started")

    os.makedirs(REPORT_DIR, exist_ok=True)

    report_path = REPORT_DIR + "/forensic_report.txt"

    with open(report_path, "w") as report:

        report.write("========== DIGITAL FORENSIC INVESTIGATION REPORT ==========\n\n")

        report.write("Case Generated At:\n")
        report.write(str(datetime.now()) + "\n\n")

        report.write("------------------------------------------------------------\n")
        report.write("EVIDENCE FILES COLLECTED\n")
        report.write("------------------------------------------------------------\n")

        if os.path.exists(EVIDENCE_DIR):
            for file in os.listdir(EVIDENCE_DIR):
                report.write(file + "\n")

        report.write("\n------------------------------------------------------------\n")
        report.write("SYSTEM ANALYSIS RESULTS\n")
        report.write("------------------------------------------------------------\n")

        if os.path.exists(ANALYSIS_DIR):
            for file in os.listdir(ANALYSIS_DIR):
                report.write(file + "\n")

        report.write("\n------------------------------------------------------------\n")
        report.write("NETWORK ANALYSIS RESULTS\n")
        report.write("------------------------------------------------------------\n")

        if os.path.exists(NETWORK_DIR):
            for file in os.listdir(NETWORK_DIR):
                report.write(file + "\n")

        report.write("\n------------------------------------------------------------\n")
        report.write("EVIDENCE INTEGRITY (SHA256 HASHES)\n")
        report.write("------------------------------------------------------------\n")

        hash_file = INTEGRITY_DIR + "/system_hashes.txt"

        if os.path.exists(hash_file):
            with open(hash_file) as hashes:
                report.write(hashes.read())

        report.write("\n------------------------------------------------------------\n")
        report.write("INVESTIGATION ACTIVITY LOG\n")
        report.write("------------------------------------------------------------\n")

        log_file = LOG_DIR + "/investigation_log.txt"

        if os.path.exists(log_file):
            with open(log_file) as logs:
                report.write(logs.read())

    log_action("Report Generated")

    print("\n[+] Structured forensic report generated successfully.\n")


#-------------------DUMP MODULES------------------

def memory_dump_analysis():

    log_action("Memory Dump Analysis Started")

    os.makedirs(DUMP_DIR, exist_ok=True)

    dump_file = input("Enter memory dump file path: ")

    if not os.path.exists(dump_file):
        print("File not found.")
        return

    output_file = DUMP_DIR + "/memory_analysis.txt"

    print("\n[+] Scanning memory dump (filtered)...")

    os.system(f"strings {dump_file} | grep -Ei 'http|https|cmd|powershell|base64|password|login' > {output_file}")

    print("[+] Searching for suspicious patterns...")

    os.system(f'grep -Ei "http|https|cmd|powershell|base64" {output_file} > {DUMP_DIR}/suspicious_patterns.txt')

    print(f"\n[+] Memory analysis saved at: {output_file}")

    log_action("Memory Dump Analysis Completed")




def disk_dump_analysis():

    log_action("Disk Image Analysis Started")

    os.makedirs(DUMP_DIR, exist_ok=True)

    disk_file = input("Enter disk image file path: ")

    if not os.path.exists(disk_file):
        print("File not found.")
        return

    output_file = DUMP_DIR + "/disk_analysis.txt"

    print("\n[+] Listing files from disk image...")

    os.system(f"fls {disk_file} > {output_file}")

    print(f"[+] Disk analysis saved at: {output_file}")

    log_action("Disk Image Analysis Completed")




def network_dump_analysis():

    log_action("Network Capture Analysis Started")

    os.makedirs(DUMP_DIR, exist_ok=True)

    pcap_file = input("Enter pcap file path: ")

    if not os.path.exists(pcap_file):
        print("File not found.")
        return

    output_file = DUMP_DIR + "/network_analysis.txt"

    print("\n[+] Analyzing network capture...")

    os.system(f"tshark -r {pcap_file} > {output_file}")

    print(f"[+] Network analysis saved at: {output_file}")

    log_action("Network Capture Analysis Completed")



def log_analysis():

    log_action("Log File Analysis Started")

    os.makedirs(DUMP_DIR, exist_ok=True)

    log_file = input("Enter log file path: ")

    if not os.path.exists(log_file):
        print("File not found.")
        return

    output_file = DUMP_DIR + "/log_analysis.txt"

    print("\n[+] Searching for suspicious log entries...")

    os.system(f'grep -Ei "failed|error|unauthorized|denied" {log_file} > {output_file}')

    print(f"[+] Log analysis saved at: {output_file}")

    log_action("Log File Analysis Completed")




def suspicious_file_analysis():

    log_action("Suspicious File Analysis Started")

    os.makedirs(DUMP_DIR, exist_ok=True)

    file_path = input("Enter file path to analyze: ")

    if not os.path.exists(file_path):
        print("File not found.")
        return

    output_file = DUMP_DIR + "/suspicious_file_report.txt"

    with open(output_file, "w") as report:

        report.write("===== SUSPICIOUS FILE ANALYSIS =====\n\n")

        # File type
        report.write("[File Type]\n")
        os.system(f"file {file_path} >> {output_file}")

        report.write("\n[Extracted Strings]\n")
        os.system(f"strings {file_path} | head -n 50 >> {output_file}")

        report.write("\n[Suspicious Patterns]\n")
        os.system(f'grep -Ei "http|https|cmd|powershell|base64|malware|hack" {file_path} >> {output_file}')

    print(f"\n[+] Analysis saved at: {output_file}")

    log_action("Suspicious File Analysis Completed")




def generate_dump_report():

    log_action("Dump Report Generation Started")

    os.makedirs(DUMP_DIR, exist_ok=True)

    report_path = DUMP_DIR + "/dump_report.txt"

    with open(report_path, "w") as report:

        report.write("========== DUMP FORENSIC REPORT ==========\n\n")

        report.write("Case Generated At:\n")
        report.write(str(datetime.now()) + "\n\n")

        # Memory Analysis
        memory_file = DUMP_DIR + "/memory_analysis.txt"
        if os.path.exists(memory_file):
            report.write("----- MEMORY ANALYSIS -----\n")
            with open(memory_file) as f:
                report.write(f.read() + "\n\n")

        # Suspicious File Analysis
        suspicious_file = DUMP_DIR + "/suspicious_file_report.txt"
        if os.path.exists(suspicious_file):
            report.write("----- SUSPICIOUS FILE ANALYSIS -----\n")
            with open(suspicious_file) as f:
                report.write(f.read() + "\n\n")

        report.write("=========================================\n")

    print(f"\n[+] Dump report generated at: {report_path}")

    log_action("Dump Report Generated")



# ------------------ MENU ------------------
def main_menu():

    show_banner()
    
    print("1. Live Forensics")
    print("2. Dump Investigation")
    print("3. Exit")

    choice = input("Enter choice: ")

    if choice == "1":
        live_menu()

    elif choice == "2":
        dump_menu()

    elif choice == "3":
        exit()

    else:
        print("Invalid choice\n")

def live_menu():

  while True:

    print("\n ---LIVE FORENSICS---")
    print("1. Evidence Acquisition")
    print("2. System Analysis")
    print("3. Network Analysis")
    print("4. Generate Evidence Hashes")
    print("5. Verify Evidence Integrity")
    print("6. Generate Report")
    print("7. Back")

    choice = input("Enter choice: ")

    if choice == "1":
        evidence_acquisition()

    elif choice == "2":
        system_analysis()

    elif choice == "3":
         network_analysis()

    elif choice == "4":
        generate_hashes()

    elif choice == "5":
         verify_hashes()

    elif choice == "6":
        generate_report()

    elif choice == "7":
        break

    else:
        print("Invalid choice\n")

def dump_menu():

  while True:

    print("\n--- DUMP INVESTIGATION ---")
    print("1. Memory Dump Analysis")
    print("2. Disk Image Analysis")
    print("3. Network Capture Analysis")
    print("4. Log File Analysis")
    print("5. Suspicious File Analysis")
    print("6. Generate Dump Report")
    print("7. Back")

    choice = input("Enter choice: ")

    if choice == "1":
        memory_dump_analysis()

    elif choice == "2":
        disk_dump_analysis()

    elif choice == "3":
        network_dump_analysis()

    elif choice == "4":
        log_analysis()

    elif choice == "5":
        suspicious_file_analysis()

    elif choice == "6":
        generate_dump_report()

    elif choice =="7":
        break

    else:
        print("Invalid choice\n")


# ------------------ PROGRAM LOOP ------------------

while True:
    main_menu()
