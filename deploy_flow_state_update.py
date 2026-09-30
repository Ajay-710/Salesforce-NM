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

flow_xml = """<?xml version="1.0" encoding="UTF-8"?>
<Flow xmlns="http://soap.sforce.com/2006/04/metadata">
    <apiVersion>60.0</apiVersion>
    <assignments>
        <name>Assign_Policy_State</name>
        <label>Assign Policy State</label>
        <locationX>176</locationX>
        <locationY>395</locationY>
        <assignmentItems>
            <assignToReference>$Record.Policy_Account_Holder_State__c</assignToReference>
            <operator>Assign</operator>
            <value>
                <elementReference>get_policy_records.Policy_State__c</elementReference>
            </value>
        </assignmentItems>
    </assignments>
    <environments>Default</environments>
    <interviewLabel>Claim Policy Holder State Update {!$Flow.CurrentDateTime}</interviewLabel>
    <label>Claim Policy Holder State Update</label>
    <processMetadataValues>
        <name>BuilderType</name>
        <value>
            <stringValue>LightningFlowBuilder</stringValue>
        </value>
    </processMetadataValues>
    <processType>AutoLaunchedFlow</processType>
    <recordLookups>
        <name>get_policy_records</name>
        <label>get_policy_records</label>
        <locationX>176</locationX>
        <locationY>287</locationY>
        <assignNullValuesIfNoRecordsFound>false</assignNullValuesIfNoRecordsFound>
        <connector>
            <targetReference>Assign_Policy_State</targetReference>
        </connector>
        <filterLogic>and</filterLogic>
        <filters>
            <field>Id</field>
            <operator>EqualTo</operator>
            <value>
                <elementReference>$Record.Policy__c</elementReference>
            </value>
        </filters>
        <getFirstRecordOnly>true</getFirstRecordOnly>
        <object>Policy__c</object>
        <storeOutputAutomatically>true</storeOutputAutomatically>
    </recordLookups>
    <start>
        <locationX>50</locationX>
        <locationY>0</locationY>
        <connector>
            <targetReference>get_policy_records</targetReference>
        </connector>
        <object>Claim__c</object>
        <recordTriggerType>CreateAndUpdate</recordTriggerType>
        <triggerType>RecordBeforeSave</triggerType>
    </start>
    <status>Active</status>
</Flow>"""

package_xml = """<?xml version="1.0" encoding="UTF-8"?>
<Package xmlns="http://soap.sforce.com/2006/04/metadata">
    <types>
        <members>Claim_Policy_Holder_State_Update</members>
        <name>Flow</name>
    </types>
    <version>60.0</version>
</Package>"""

buf = io.BytesIO()
with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as z:
    z.writestr('package.xml', package_xml)
    z.writestr('flows/Claim_Policy_Holder_State_Update.flow', flow_xml)

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
            print("Claim Policy Holder State Update SUCCESS:", success)
            if success != 'true':
                failures = croot.findall('.//{http://soap.sforce.com/2006/04/metadata}componentFailures')
                for fail in failures:
                    comp = fail.find('{http://soap.sforce.com/2006/04/metadata}fileName').text
                    prob = fail.find('{http://soap.sforce.com/2006/04/metadata}problem').text
                    print(f"FAILED: {comp} -> {prob}")
            break
else:
    print("Error:", res.text)
