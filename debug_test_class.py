import requests

with open("session_id.txt", "r") as f:
    sid = f.read().strip()

instance_url = "https://orgfarm-dd7f1a505a-dev-ed.develop.my.salesforce.com"
headers = {
    "Authorization": f"Bearer {sid}",
    "Content-Type": "application/json"
}

with open("force-app/main/default/classes/ClaimsAdjusterControllerTest.cls", "r") as f:
    code = f.read()

# Let's test compiling it via executeAnonymous to see line/column
res = requests.get(f"{instance_url}/services/data/v60.0/tooling/executeAnonymous/?anonymousBody={requests.utils.quote(code)}", headers=headers)
print("Exec Anon Test Class:", res.json())
