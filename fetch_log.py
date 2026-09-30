import requests

with open("session_id.txt", "r") as f:
    sid = f.read().strip()

instance_url = "https://orgfarm-dd7f1a505a-dev-ed.develop.my.salesforce.com"
headers = {
    "Authorization": f"Bearer {sid}",
    "Content-Type": "application/json"
}

# Query recent ApexLog
res = requests.get(f"{instance_url}/services/data/v60.0/tooling/query/?q=SELECT+Id,Status,Operation,DurationMilliseconds+FROM+ApexLog+ORDER+BY+StartTime+DESC+LIMIT+5", headers=headers)
logs = res.json().get('records', [])
print("Recent logs:", [(l['Id'], l['Status'], l['Operation']) for l in logs])

if logs:
    log_id = logs[0]['Id']
    log_body = requests.get(f"{instance_url}/services/data/v60.0/tooling/sobjects/ApexLog/{log_id}/Body", headers=headers)
    # Search for USER_DEBUG or EXCEPTION in log
    for line in log_body.text.split('\n'):
        if 'USER_DEBUG' in line or 'EXCEPTION' in line or 'FATAL' in line:
            print(line)
