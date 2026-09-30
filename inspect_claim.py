import requests

with open("session_id.txt", "r") as f:
    sid = f.read().strip()

instance_url = "https://orgfarm-dd7f1a505a-dev-ed.develop.my.salesforce.com"
headers = {
    "Authorization": f"Bearer {sid}",
    "Content-Type": "application/json"
}

res = requests.get(f"{instance_url}/services/data/v60.0/sobjects/Claim__c/describe", headers=headers)
data = res.json()
for f in data['fields']:
    if 'Policy' in f['name'] or f['type'] == 'reference':
        print(f"Field: {f['name']}, Type: {f['type']}, RelationshipName: {f.get('relationshipName')}, ReferenceTo: {f.get('referenceTo')}")
