import requests
import time

with open("session_id.txt", "r") as f:
    sid = f.read().strip()

instance_url = "https://orgfarm-dd7f1a505a-dev-ed.develop.my.salesforce.com"
headers = {
    "Authorization": f"Bearer {sid}",
    "Content-Type": "application/json"
}

with open("force-app/main/default/classes/ClaimsAdjusterControllerTest.cls", "r") as f:
    full_code = f.read()

# Update via Tooling API MetadataContainer
mc_name = f"Container_{int(time.time())}"
mc_res = requests.post(f"{instance_url}/services/data/v60.0/tooling/sobjects/MetadataContainer", headers=headers, json={"Name": mc_name})
mc_id = mc_res.json().get('id')

class_id = "01pbm00000VtUziAAF"
acm_data = {
    "MetadataContainerId": mc_id,
    "ContentEntityId": class_id,
    "Body": full_code
}
acm_res = requests.post(f"{instance_url}/services/data/v60.0/tooling/sobjects/ApexClassMember", headers=headers, json=acm_data)

car_data = {
    "MetadataContainerId": mc_id,
    "IsCheckOnly": False
}
car_res = requests.post(f"{instance_url}/services/data/v60.0/tooling/sobjects/ContainerAsyncRequest", headers=headers, json=car_data)
car_id = car_res.json().get('id')

for _ in range(10):
    time.sleep(1)
    status_res = requests.get(f"{instance_url}/services/data/v60.0/tooling/sobjects/ContainerAsyncRequest/{car_id}", headers=headers)
    s = status_res.json()
    print("Async Status:", s.get('State'), s.get('ErrorMsg'))
    if s.get('State') in ['Completed', 'Failed', 'Error']:
        break
