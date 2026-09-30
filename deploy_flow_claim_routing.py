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
    <decisions>
        <name>Route_by_Policy_Type</name>
        <label>Route by Policy Type</label>
        <locationX>314</locationX>
        <locationY>431</locationY>
        <defaultConnector>
            <targetReference>Assign_to_Life_Queue</targetReference>
        </defaultConnector>
        <defaultConnectorLabel>Life Claim Route</defaultConnectorLabel>
        <rules>
            <name>Auto_Claim_Route</name>
            <conditionLogic>and</conditionLogic>
            <conditions>
                <leftValueReference>Get_Policy_RT.RecordType.Name</leftValueReference>
                <operator>EqualTo</operator>
                <rightValue>
                    <stringValue>Auto</stringValue>
                </rightValue>
            </conditions>
            <connector>
                <targetReference>Assign_to_Auto_Queue</targetReference>
            </connector>
            <label>Auto Claim Route</label>
        </rules>
        <rules>
            <name>Property_Claim_Route</name>
            <conditionLogic>and</conditionLogic>
            <conditions>
                <leftValueReference>Get_Policy_RT.RecordType.Name</leftValueReference>
                <operator>EqualTo</operator>
                <rightValue>
                    <stringValue>Property</stringValue>
                </rightValue>
            </conditions>
            <connector>
                <targetReference>Assign_to_Property_Queue</targetReference>
            </connector>
            <label>Property Claim Route</label>
        </rules>
    </decisions>
    <environments>Default</environments>
    <interviewLabel>ClaimRoutingFlow {!$Flow.CurrentDateTime}</interviewLabel>
    <label>ClaimRoutingFlow</label>
    <processMetadataValues>
        <name>BuilderType</name>
        <value>
            <stringValue>LightningFlowBuilder</stringValue>
        </value>
    </processMetadataValues>
    <processType>AutoLaunchedFlow</processType>
    <recordLookups>
        <name>Get_Policy_RT</name>
        <label>Get_Policy_RT</label>
        <locationX>314</locationX>
        <locationY>323</locationY>
        <assignNullValuesIfNoRecordsFound>false</assignNullValuesIfNoRecordsFound>
        <connector>
            <targetReference>Route_by_Policy_Type</targetReference>
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
    <recordUpdates>
        <name>Assign_to_Auto_Queue</name>
        <label>Assign to Auto Queue</label>
        <locationX>50</locationX>
        <locationY>539</locationY>
        <inputAssignments>
            <field>OwnerId</field>
            <value>
                <stringValue>00Gbm00000QJ58HEAT</stringValue>
            </value>
        </inputAssignments>
        <inputReference>$Record</inputReference>
    </recordUpdates>
    <recordUpdates>
        <name>Assign_to_Property_Queue</name>
        <label>Assign to Property Queue</label>
        <locationX>314</locationX>
        <locationY>539</locationY>
        <inputAssignments>
            <field>OwnerId</field>
            <value>
                <stringValue>00Gbm00000QJ59tEAD</stringValue>
            </value>
        </inputAssignments>
        <inputReference>$Record</inputReference>
    </recordUpdates>
    <recordUpdates>
        <name>Assign_to_Life_Queue</name>
        <label>Assign to Life Queue</label>
        <locationX>578</locationX>
        <locationY>539</locationY>
        <inputAssignments>
            <field>OwnerId</field>
            <value>
                <stringValue>00Gbm00000QJ5BVEA1</stringValue>
            </value>
        </inputAssignments>
        <inputReference>$Record</inputReference>
    </recordUpdates>
    <start>
        <locationX>188</locationX>
        <locationY>0</locationY>
        <connector>
            <targetReference>Get_Policy_RT</targetReference>
        </connector>
        <object>Claim__c</object>
        <recordTriggerType>Create</recordTriggerType>
        <triggerType>RecordAfterSave</triggerType>
    </start>
    <status>Active</status>
</Flow>"""

package_xml = """<?xml version="1.0" encoding="UTF-8"?>
<Package xmlns="http://soap.sforce.com/2006/04/metadata">
    <types>
        <members>ClaimRoutingFlow</members>
        <name>Flow</name>
    </types>
    <version>60.0</version>
</Package>"""

buf = io.BytesIO()
with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as z:
    z.writestr('package.xml', package_xml)
    z.writestr('flows/ClaimRoutingFlow.flow', flow_xml)

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
            print("ClaimRoutingFlow SUCCESS:", success)
            if success != 'true':
                failures = croot.findall('.//{http://soap.sforce.com/2006/04/metadata}componentFailures')
                for fail in failures:
                    comp = fail.find('{http://soap.sforce.com/2006/04/metadata}fileName').text
                    prob = fail.find('{http://soap.sforce.com/2006/04/metadata}problem').text
                    print(f"FAILED: {comp} -> {prob}")
            break
else:
    print("Error:", res.text)
