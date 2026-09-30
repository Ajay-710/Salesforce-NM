import requests

with open("session_id.txt", "r") as f:
    sid = f.read().strip()

instance_url = "https://orgfarm-dd7f1a505a-dev-ed.develop.my.salesforce.com"
headers = {
    "Authorization": f"Bearer {sid}",
    "Content-Type": "application/json"
}

q = "SELECT Id, Name, Claim_Amount__c, Approval_Status__c, Date_of_Loss__c, Policy__r.Name, Policy__r.RecordType.Name, Policy__r.Customer__r.FirstName, Policy__r.Customer__r.LastName FROM Claim__c LIMIT 1"
res = requests.get(f"{instance_url}/services/data/v60.0/query/?q={requests.utils.quote(q)}", headers=headers)
print("Query result:", res.status_code, res.text)
