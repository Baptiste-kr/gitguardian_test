# -*- coding: utf-8 -*-
"""
Creation : 30/05/2021
Name : answer.py
Author : Baptiste Krattinger
"""

# Import
import os
import json
os.system('cls')

# Import Gitguardian Wrapper
from pygitguardian import GGClient

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

#### GET EVERY INCIDENTS
RESPONSE = CLIENT.get('https://api.gitguardian.com/v1/incidents/secrets')
INCIDENTS = RESPONSE.json()
assert RESPONSE.status_code == 200, "Invalid get request" + str(RESPONSE.status_code)
print(f"{str(len(INCIDENTS))} incident(s) reported\n")


#### ASSIGN
USER = {
    "email": "bk_gg_test@yopmail.com",
    "member_id": 1234
}
for incidents in INCIDENTS:
    incident_id = str(incidents["id"])
    response = CLIENT.post(
        f"https://api.gitguardian.com/v1/incidents/secrets/{incident_id}/assign",
        data=USER
    )
    if response.status_code != 200:
        print("Invalid assign post request " + str(response.status_code))
    else:
        print(f"Incidents {str(incident_id)} assigned to {USER['email']}")


#### UNASSIGN
for incidents in INCIDENTS:
    incident_id = str(incidents["id"])
    response = CLIENT.post(
        f"https://api.gitguardian.com/v1/incidents/secrets/{incident_id}/unassign"
    )
    if response.status_code != 200:
        print("Invalid unassign post request " + str(response.status_code))
    else:
        print(f"Incidents {str(incident_id)} unassigned")

#### RESOLVE
SECRET = {
    "secret_revoked": True
}
for incidents in INCIDENTS:
    incident_id = str(incidents["id"])
    response = CLIENT.post(
        f"https://api.gitguardian.com/v1/incidents/secrets/{incident_id}/resolve",
        data=SECRET
    )
    if response.status_code != 200:
        print("Invalid resolve post request " + str(response.status_code))
    else:
        print(f"Incidents {str(incident_id)} resolved")

#### COMMENT
COMMENT = {
    "comment": "BK test for QA"
}
for incidents in INCIDENTS:
    incident_id = str(incidents["id"])
    response = CLIENT.post(
        f"https://api.gitguardian.com/v1/incidents/secrets/{incident_id}/notes",
        data=COMMENT
    )
    if response.status_code != 201:
        print("Invalid notes post request " + str(response.status_code))
    else:
        print(f"Incidents {str(incident_id)} commented : {str(COMMENT['comment'])}")

#### REOPEN
for incidents in INCIDENTS:
    incident_id = str(incidents["id"])
    response = CLIENT.post(
        f"https://api.gitguardian.com/v1/incidents/secrets/{incident_id}/reopen"
    )
    if response.status_code != 200:
        print("Invalid unassign post request " + str(response.status_code))
    else:
        print(f"Incidents {str(incident_id)} reopened")
