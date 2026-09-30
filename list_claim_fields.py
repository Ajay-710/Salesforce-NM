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
print("All fields on Claim__c:", [f['name'] for f in data['fields']])
