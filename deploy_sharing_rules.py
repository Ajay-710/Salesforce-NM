import io
import zipfile
import base64
import requests
import xml.etree.ElementTree as ET
import time

with open("session_id.txt", "r") as f:
    sid = f.read().strip()

url = "https://orgfarm-dd7f1a505a-dev-ed.develop.my.salesforce.com/services/Soap/m/60.0"
headers = {
    "Content-Type": "text/xml; charset=UTF-8",
    "SOAPAction": "deploy"
}

sharing_rules_xml = """<?xml version="1.0" encoding="UTF-8"?>
<SharingRules xmlns="http://soap.sforce.com/2006/04/metadata">
    <sharingCriteriaRules>
        <fullName>Share_Records_based_on_Policy_State_CA</fullName>
        <accessLevel>Edit</accessLevel>
        <label>Share Records based on Policy State CA</label>
        <sharedTo>
            <group>Claim_Adjusters_California</group>
        </sharedTo>
        <criteriaItems>
            <field>Policy_Account_Holder_State__c</field>
            <operation>equals</operation>
            <value>CA</value>
        </criteriaItems>
    </sharingCriteriaRules>
    <sharingCriteriaRules>
        <fullName>Share_Records_based_on_Policy_State_TX</fullName>
        <accessLevel>Edit</accessLevel>
        <label>Share Records based on Policy State TX</label>
        <sharedTo>
            <group>Claim_Adjusters_Texas</group>
        </sharedTo>
        <criteriaItems>
            <field>Policy_Account_Holder_State__c</field>
            <operation>equals</operation>
            <value>TX</value>
        </criteriaItems>
    </sharingCriteriaRules>
</SharingRules>"""

package_xml = """<?xml version="1.0" encoding="UTF-8"?>
<Package xmlns="http://soap.sforce.com/2006/04/metadata">
    <types>
        <members>Claim__c</members>
        <name>SharingRules</name>
    </types>
    <version>60.0</version>
</Package>"""

buf = io.BytesIO()
with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as z:
    z.writestr('package.xml', package_xml)
    z.writestr('sharingRules/Claim__c.sharingRules', sharing_rules_xml)

zip_bytes = buf.getvalue()
b64_zip = base64.b64encode(zip_bytes).decode('utf-8')

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
    <deploy xmlns="http://soap.sforce.com/2006/04/metadata">
      <ZipFile>{b64_zip}</ZipFile>
      <DeployOptions>
        <checkOnly>false</checkOnly>
        <rollbackOnError>true</rollbackOnError>
        <singlePackage>true</singlePackage>
      </DeployOptions>
    </deploy>
  </env:Body>
</env:Envelope>"""

res = requests.post(url, data=body, headers=headers)
root = ET.fromstring(res.text)
async_id_elem = root.find('.//{http://soap.sforce.com/2006/04/metadata}id')
if async_id_elem is not None:
    deploy_id = async_id_elem.text
    print("Deploy ID:", deploy_id)
    check_headers = {"Content-Type": "text/xml; charset=UTF-8", "SOAPAction": "checkDeployStatus"}
    for _ in range(15):
        time.sleep(2)
        check_body = f"""<?xml version="1.0" encoding="utf-8" ?>
<env:Envelope xmlns:xsd="http://www.w3.org/2001/XMLSchema"
              xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
              xmlns:env="http://schemas.xmlsoap.org/soap/envelope/">
  <env:Header>
    <SessionHeader xmlns="http://soap.sforce.com/2006/04/metadata">
      <sessionId>{sid}</sessionId>
    </SessionHeader>
  </env:Header>
  <env:Body>
    <checkDeployStatus xmlns="http://soap.sforce.com/2006/04/metadata">
      <asyncProcessId>{deploy_id}</asyncProcessId>
      <includeDetails>true</includeDetails>
    </checkDeployStatus>
  </env:Body>
</env:Envelope>"""
        cres = requests.post(url, data=check_body, headers=check_headers)
        croot = ET.fromstring(cres.text)
        done = croot.find('.//{http://soap.sforce.com/2006/04/metadata}done').text
        status = croot.find('.//{http://soap.sforce.com/2006/04/metadata}status').text
        print(f"Deploy status: {status}, done: {done}")
        if done == 'true':
            success = croot.find('.//{http://soap.sforce.com/2006/04/metadata}success').text
            print("Sharing Rules Deploy SUCCESS:", success)
            if success != 'true':
                failures = croot.findall('.//{http://soap.sforce.com/2006/04/metadata}componentFailures')
                for fail in failures:
                    comp = fail.find('{http://soap.sforce.com/2006/04/metadata}fileName').text
                    prob = fail.find('{http://soap.sforce.com/2006/04/metadata}problem').text
                    print(f"FAILED: {comp} -> {prob}")
            break
else:
    print("Error:", res.text)
