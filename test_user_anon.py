import requests

with open("session_id.txt", "r") as f:
    sid = f.read().strip()

instance_url = "https://orgfarm-dd7f1a505a-dev-ed.develop.my.salesforce.com"
headers = {
    "Authorization": f"Bearer {sid}",
    "Content-Type": "application/json"
}

code = """
Profile p = [SELECT Id FROM Profile WHERE Name = 'Standard User' LIMIT 1];
User u = new User(
    FirstName = 'Test',
    LastName = 'User',
    Alias = 'tuser',
    Username = 'testuser' + DateTime.now().getTime() + '@example.com.test',
    Email = 'testuser123@example.com',
    TimeZoneSidKey = 'America/Los_Angeles',
    LocaleSidKey = 'en_US',
    EmailEncodingKey = 'UTF-8',
    LanguageLocaleKey = 'en_US',
    ProfileId = p.Id
);
insert u;
"""
res = requests.get(f"{instance_url}/services/data/v60.0/tooling/executeAnonymous/?anonymousBody={requests.utils.quote(code)}", headers=headers)
print("Exec user insert:", res.json())
