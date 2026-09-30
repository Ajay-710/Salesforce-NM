import requests

with open("session_id.txt", "r") as f:
    sid = f.read().strip()

instance_url = "https://orgfarm-dd7f1a505a-dev-ed.develop.my.salesforce.com"
headers = {
    "Authorization": f"Bearer {sid}",
    "Content-Type": "application/json"
}

code = """
User u = [SELECT Id FROM User WHERE Alias = 'tuser' LIMIT 1];
System.runAs(u) {
    List<ClaimsAdjusterController.ClaimWrapper> results = ClaimsAdjusterController.getAssignedClaims();
    System.debug('RESULT_SIZE: ' + results.size());
    List<Claim__c> cList = [SELECT Id, OwnerId, Name FROM Claim__c];
    System.debug('ALL_CLAIMS: ' + cList);
    List<Claim__c> uList = [SELECT Id, OwnerId, Name FROM Claim__c WHERE OwnerId = :u.Id];
    System.debug('USER_CLAIMS: ' + uList);
}
"""

res = requests.get(f"{instance_url}/services/data/v60.0/tooling/executeAnonymous/?anonymousBody={requests.utils.quote(code)}", headers=headers)
print("Anon result:", res.json())
