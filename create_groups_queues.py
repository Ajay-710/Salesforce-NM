import requests

with open("session_id.txt", "r") as f:
    sid = f.read().strip()

instance_url = "https://orgfarm-dd7f1a505a-dev-ed.develop.my.salesforce.com"
headers = {
    "Authorization": f"Bearer {sid}",
    "Content-Type": "application/json"
}

# 1. Public Groups
groups = [
    {"Name": "Claim Adjusters- California", "DeveloperName": "Claim_Adjusters_California", "Type": "Regular"},
    {"Name": "Claim Adjusters- Texas", "DeveloperName": "Claim_Adjusters_Texas", "Type": "Regular"}
]

for g in groups:
    res = requests.post(f"{instance_url}/services/data/v60.0/sobjects/Group", headers=headers, json=g)
    print(f"Group {g['Name']}:", res.status_code, res.text)

# 2. Queues
queues = [
    {"Name": "Auto Queue", "DeveloperName": "Auto_Queue", "Type": "Queue"},
    {"Name": "Property Queue", "DeveloperName": "Property_Queue", "Type": "Queue"},
    {"Name": "Life Queue", "DeveloperName": "Life_Queue", "Type": "Queue"}
]

queue_ids = {}
for q in queues:
    res = requests.post(f"{instance_url}/services/data/v60.0/sobjects/Group", headers=headers, json=q)
    print(f"Queue {q['Name']}:", res.status_code, res.text)
    if res.status_code == 201:
        queue_ids[q['Name']] = res.json()['id']
    else:
        # Query existing
        q_res = requests.get(f"{instance_url}/services/data/v60.0/query/?q=SELECT+Id+FROM+Group+WHERE+DeveloperName=\'{q['DeveloperName']}\'", headers=headers)
        queue_ids[q['Name']] = q_res.json()['records'][0]['Id']

# 3. Associate Queues with Claim__c via QueueSobject
for q_name, q_id in queue_ids.items():
    qs = {
        "QueueId": q_id,
        "SobjectType": "Claim__c"
    }
    res = requests.post(f"{instance_url}/services/data/v60.0/sobjects/QueueSobject", headers=headers, json=qs)
    print(f"QueueSobject {q_name}:", res.status_code, res.text)

print("Queue IDs map:", queue_ids)
with open("queue_ids.json", "w") as f:
    import json
    json.dump(queue_ids, f)
