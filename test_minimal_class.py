import requests

with open("session_id.txt", "r") as f:
    sid = f.read().strip()

instance_url = "https://orgfarm-dd7f1a505a-dev-ed.develop.my.salesforce.com"
headers = {
    "Authorization": f"Bearer {sid}",
    "Content-Type": "application/json"
}

body1 = """@isTest
private class ClaimsAdjusterControllerTest {
    @isTest
    static void testMe() {
        System.assert(true);
    }
}"""

res = requests.post(f"{instance_url}/services/data/v60.0/tooling/sobjects/ApexClass", headers=headers, json={"Name": "ClaimsAdjusterControllerTest", "Body": body1})
print("Create minimal test class:", res.status_code, res.text)
