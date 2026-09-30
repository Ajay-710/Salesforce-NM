import requests
import base64

with open("session_id.txt", "r") as f:
    sid = f.read().strip()

url = "https://orgfarm-dd7f1a505a-dev-ed.develop.my.salesforce.com/services/Soap/m/60.0"
headers = {
    "Content-Type": "text/xml; charset=UTF-8",
    "SOAPAction": "createMetadata"
}

with open("force-app/main/default/classes/ClaimsAdjusterControllerTest.cls", "r") as f:
    code = f.read()

b64_code = base64.b64encode(code.encode('utf-8')).decode('utf-8')

body = f"""<?xml version="1.0" encoding="utf-8" ?>
<env:Envelope xmlns:xsd="http://www.w3.org/2001/XMLSchema"
              xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
              xmlns:env="http://schemas.xmlsoap.org/soap/envelope/">
  <env:Header>
    <SessionHeader xmlns="http://soap.sforce.com/2006/04/metadata">
      <sessionId>{sid}</sessionId>
    </SessionHeader>
  </env:Header>
  <env:Body>
    <createMetadata xmlns="http://soap.sforce.com/2006/04/metadata">
      <metadata xsi:type="ApexClass">
        <fullName>ClaimsAdjusterControllerTest</fullName>
        <content>{b64_code}</content>
        <apiVersion>60.0</apiVersion>
        <status>Active</status>
      </metadata>
    </createMetadata>
  </env:Body>
</env:Envelope>"""

res = requests.post(url, data=body, headers=headers)
print("CreateMetadata ApexClass Test Status:", res.status_code)
print(res.text)
