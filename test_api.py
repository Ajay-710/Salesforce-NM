import requests

with open("session_id.txt", "r") as f:
    sid = f.read().strip()

instance_url = "https://orgfarm-dd7f1a505a-dev-ed.develop.my.salesforce.com"
headers = {
    "Authorization": f"Bearer {sid}",
    "Content-Type": "application/json"
}

res = requests.get(f"{instance_url}/services/data/v60.0/sobjects/", headers=headers)
print("SObjects Status Code:", res.status_code)
if res.status_code == 200:
    data = res.json()
    custom_objs = [s['name'] for s in data['sobjects'] if s['custom']]
    print("Custom Objects found in org:", custom_objs)
else:
    print("Error:", res.text[:300])
