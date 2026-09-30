import requests
import xml.etree.ElementTree as ET

url = "https://login.salesforce.com/services/Soap/u/58.0"
headers = {
    "Content-Type": "text/xml; charset=UTF-8",
    "SOAPAction": "login"
}

body = """<?xml version="1.0" encoding="utf-8" ?>
<env:Envelope xmlns:xsd="http://www.w3.org/2001/XMLSchema"
              xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
              xmlns:env="http://schemas.xmlsoap.org/soap/envelope/">
  <env:Body>
    <n1:login xmlns:n1="urn:partner.soap.sforce.com">
      <n1:username>pendemajay7.64257f50286e@agentforce.com</n1:username>
      <n1:password>1234567Ajay</n1:password>
    </n1:login>
  </env:Body>
</env:Envelope>"""

res = requests.post(url, data=body, headers=headers)
print("Status code:", res.status_code)
print("Response text:", res.text[:500])
