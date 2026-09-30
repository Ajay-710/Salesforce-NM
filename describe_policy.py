import requests

with open("session_id.txt", "r") as f:
    sid = f.read().strip()

instance_url = "https://orgfarm-dd7f1a505a-dev-ed.develop.my.salesforce.com"
headers = {
    "Authorization": f"Bearer {sid}",
    "Content-Type": "application/json"
}

res = requests.get(f"{instance_url}/services/data/v60.0/sobjects/Policy__c/describe", headers=headers)
if res.status_code == 200:
    data = res.json()
    fields = [f['name'] for f in data['fields']]
    print("Policy__c fields:", fields)
    record_types = [rt['name'] for rt in data.get('recordTypeInfos', [])]
    print("Policy__c Record Types:", record_types)
else:
    print("Error describing Policy__c:", res.text)
