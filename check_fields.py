import requests

with open("session_id.txt", "r") as f:
    sid = f.read().strip()

instance_url = "https://orgfarm-dd7f1a505a-dev-ed.develop.my.salesforce.com"
headers = {
    "Authorization": f"Bearer {sid}",
    "Content-Type": "application/json"
}

# Test SOQL
res = requests.get(f"{instance_url}/services/data/v60.0/query/?q=SELECT+Id,Name,DeveloperName+FROM+RecordType+LIMIT+1", headers=headers)
print("Query RecordType:", res.status_code, res.text)

# Also test User fields:
res2 = requests.get(f"{instance_url}/services/data/v60.0/sobjects/User/describe", headers=headers)
if res2.status_code == 200:
    fields = [f['name'] for f in res2.json()['fields']]
    print("User fields containing Alias or similar:", [f for f in fields if 'Alias' in f or 'Name' in f or 'User' in f])
