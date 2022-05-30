# -*- coding: utf-8 -*-
"""
Creation : 30/05/2021
Name : answer.py
Author : Baptiste Krattinger
"""

# Import
import os
import glob
os.system('cls')

# Import Gitguardian Wrapper
from pygitguardian import GGClient

# =============================================================
# CLIENT BADLY INNITIALYZED
# =============================================================

# Import API Key and init client
CLIENT = GGClient(api_key="FOOBAR")
# Check the health of the API and the API key used.
HEALTH = CLIENT.health_check()
assert HEALTH.status_code == 401, "Invalid API key : " +  str(HEALTH)
print(f"Client not initialyzed : \n{str(HEALTH)}\n")

# =============================================================
# CLIENT CORRECTLY INNITIALYZED
# =============================================================

# Import API Key and init client
API_KEY = os.getenv("GITGUARDIAN_API_KEY", "")
CLIENT = GGClient(api_key=API_KEY)
# Check the health of the API and the API key used.
HEALTH = CLIENT.health_check()
assert HEALTH.status_code == 200, "Invalid API key : " +  str(HEALTH)
print(f"Client initialyzed and healthy : \n{str(HEALTH)}\n")

# =============================================================
# FIRST USE CASE : REPOSITORY OF TLS CERTIFICATE
# =============================================================

# Get file to scan
ROOT = "C:\\Users\\bkrattinger\\Documents\\EBM_Test\\certs\\"
TO_SCAN = []
print("Starting reading repository ...")
for name in glob.glob(ROOT + "**\\*", recursive=True):
    if os.path.isfile(name) and not name.endswith(".pyc"):
        with open(name) as fn:
            try:
                TO_SCAN.append({"document": fn.read(), "filename": os.path.basename(name)})
                # print(name)
            except UnicodeDecodeError: # for binary file, here .der certificate
                pass
print("Repository processed\n")

# Scan file by file
TO_PROCESS = []
for i in range(0, len(TO_SCAN), 10):
    print(f"Starting scan {str(i + 1)}/{str(len(TO_SCAN))}")
    scan = CLIENT.multi_content_scan(TO_SCAN[i : i + 10])
    TO_PROCESS.extend(scan.scan_results)
print("All scans end\n")

# Process every results
for i, scan_result in enumerate(TO_PROCESS):
    if scan_result.has_secrets:
        # display issues
        print(f"{TO_SCAN[i]['filename']}: {scan_result.policy_break_count} break/s found")
        for policy_break in scan_result.policy_breaks:
            print(f"\t{policy_break.break_type}:")
            for match in policy_break.matches:
                print(f"\t\t{match.match_type}") #:{match.match}")
