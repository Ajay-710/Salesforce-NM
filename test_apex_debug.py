import requests

with open("session_id.txt", "r") as f:
    sid = f.read().strip()

instance_url = "https://orgfarm-dd7f1a505a-dev-ed.develop.my.salesforce.com"
headers = {
    "Authorization": f"Bearer {sid}",
    "Content-Type": "application/json"
}

# Test 1: Query with Policy__r.RecordType.Name
q1 = "SELECT Id, Policy__r.RecordType.Name FROM Claim__c LIMIT 1"
res1 = requests.get(f"{instance_url}/services/data/v60.0/query/?q={q1}", headers=headers)
print("Query RecordType.Name:", res1.status_code, res1.text)

# Test 2: Execute anonymous Apex to test User creation
apex_code = """
Profile p = [SELECT Id FROM Profile WHERE Name = 'Standard User' LIMIT 1];
System.debug('Profile: ' + p.Id);
"""
res2 = requests.get(f"{instance_url}/services/data/v60.0/tooling/executeAnonymous/?anonymousBody={requests.utils.quote(apex_code)}", headers=headers)
print("Exec Anon Profile:", res2.status_code, res2.text)
