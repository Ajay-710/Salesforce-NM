import requests

with open("session_id.txt", "r") as f:
    sid = f.read().strip()

url = "https://orgfarm-dd7f1a505a-dev-ed.develop.my.salesforce.com/services/Soap/m/60.0"
headers = {
    "Content-Type": "text/xml; charset=UTF-8",
    "SOAPAction": "createMetadata"
}

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
      <metadata xsi:type="CustomObject">
        <fullName>Claim__c</fullName>
        <label>Claim</label>
        <pluralLabel>Claim</pluralLabel>
        <nameField>
          <type>AutoNumber</type>
          <label>Claim Number</label>
          <displayFormat>C - {{0000}}</displayFormat>
          <startingNumber>1</startingNumber>
        </nameField>
        <deploymentStatus>Deployed</deploymentStatus>
        <sharingModel>ReadWrite</sharingModel>
        <enableReports>true</enableReports>
        <enableActivities>true</enableActivities>
        <enableHistory>true</enableHistory>
        <enableSearch>true</enableSearch>
      </metadata>
    </createMetadata>
  </env:Body>
</env:Envelope>"""

res = requests.post(url, data=body, headers=headers)
print("CreateMetadata Status:", res.status_code)
print("CreateMetadata Response:", res.text)
