import requests

with open("session_id.txt", "r") as f:
    sid = f.read().strip()

instance_url = "https://orgfarm-dd7f1a505a-dev-ed.develop.my.salesforce.com"
headers = {
    "Authorization": f"Bearer {sid}",
    "Content-Type": "application/json"
}

# Update test user to Senior Adjuster
u1_id = "005bm00000YXyppAAD"
r1 = requests.patch(f"{instance_url}/services/data/v60.0/sobjects/User/{u1_id}", headers=headers, json={
    "FirstName": "Senior",
    "LastName": "Adjuster",
    "Alias": "sadjust"
})
print("Update Senior Adjuster:", r1.status_code)

# Check if Department Manager exists or create
q = requests.get(f"{instance_url}/services/data/v60.0/query/?q=SELECT+Id+FROM+User+WHERE+LastName=\'Manager\'", headers=headers)
if q.json()['totalSize'] > 0:
    u2_id = q.json()['records'][0]['Id']
    print("Department Manager already exists:", u2_id)
else:
    # Get Standard User or Salesforce Platform profile
    p_res = requests.get(f"{instance_url}/services/data/v60.0/query/?q=SELECT+Id+FROM+Profile+WHERE+Name=\'Standard User\'", headers=headers)
    p_id = p_res.json()['records'][0]['Id']
    u2_data = {
        "FirstName": "Department",
        "LastName": "Manager",
        "Alias": "dmanager",
        "Username": "deptmanager_ajay123@orgfarm.com",
        "Email": "deptmanager@example.com",
        "TimeZoneSidKey": "America/Los_Angeles",
        "LocaleSidKey": "en_US",
        "EmailEncodingKey": "UTF-8",
        "LanguageLocaleKey": "en_US",
        "ProfileId": p_id
    }
    r2 = requests.post(f"{instance_url}/services/data/v60.0/sobjects/User", headers=headers, json=u2_data)
    print("Create Department Manager:", r2.status_code, r2.text)
    u2_id = r2.json().get('id')

print("Senior Adjuster User ID:", u1_id)
print("Department Manager User ID:", u2_id)
