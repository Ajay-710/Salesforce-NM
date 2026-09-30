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
    <actionCalls>
        <name>Approve_Claim</name>
        <label>Approve Claim</label>
        <locationX>50</locationX>
        <locationY>518</locationY>
        <actionName>submit</actionName>
        <actionType>submit</actionType>
        <flowTransactionModel>CurrentTransaction</flowTransactionModel>
        <inputParameters>
            <name>objectId</name>
            <value>
                <elementReference>recordId</elementReference>
            </value>
        </inputParameters>
        <inputParameters>
            <name>comment</name>
            <value>
                <elementReference>Approver_Comments</elementReference>
            </value>
        </inputParameters>
    </actionCalls>
    <actionCalls>
        <name>Reject_Claim</name>
        <label>Reject Claim</label>
        <locationX>314</locationX>
        <locationY>518</locationY>
        <actionName>submit</actionName>
        <actionType>submit</actionType>
        <flowTransactionModel>CurrentTransaction</flowTransactionModel>
        <inputParameters>
            <name>objectId</name>
            <value>
                <elementReference>recordId</elementReference>
            </value>
        </inputParameters>
        <inputParameters>
            <name>comment</name>
            <value>
                <elementReference>Approver_Comments</elementReference>
            </value>
        </inputParameters>
    </actionCalls>
    <apiVersion>60.0</apiVersion>
    <choices>
        <name>Choice_Approve</name>
        <choiceText>Approve</choiceText>
        <dataType>String</dataType>
        <value>
            <stringValue>Approve</stringValue>
        </value>
    </choices>
    <choices>
        <name>Choice_Reject</name>
        <choiceText>Reject</choiceText>
        <dataType>String</dataType>
        <value>
            <stringValue>Reject</stringValue>
        </value>
    </choices>
    <decisions>
        <name>Check_Decision</name>
        <label>Check Decision</label>
        <locationX>182</locationX>
        <locationY>398</locationY>
        <defaultConnector>
            <targetReference>Reject_Claim</targetReference>
        </defaultConnector>
        <defaultConnectorLabel>Decision Rejected</defaultConnectorLabel>
        <rules>
            <name>Decision_Approved</name>
            <conditionLogic>and</conditionLogic>
            <conditions>
                <leftValueReference>Approval_Decision</leftValueReference>
                <operator>EqualTo</operator>
                <rightValue>
                    <elementReference>Choice_Approve</elementReference>
                </rightValue>
            </conditions>
            <connector>
                <targetReference>Approve_Claim</targetReference>
            </connector>
            <label>Decision Approved</label>
        </rules>
    </decisions>
    <environments>Default</environments>
    <interviewLabel>Claim Approver Screen Flow {!$Flow.CurrentDateTime}</interviewLabel>
    <label>Claim Approver Screen Flow</label>
    <processMetadataValues>
        <name>BuilderType</name>
        <value>
            <stringValue>LightningFlowBuilder</stringValue>
        </value>
    </processMetadataValues>
    <processType>Flow</processType>
    <recordLookups>
        <name>Get_Claim_Details</name>
        <label>Get Claim Details</label>
        <locationX>182</locationX>
        <locationY>158</locationY>
        <assignNullValuesIfNoRecordsFound>false</assignNullValuesIfNoRecordsFound>
        <connector>
            <targetReference>Claim_Review_Screen</targetReference>
        </connector>
        <filterLogic>and</filterLogic>
        <filters>
            <field>Id</field>
            <operator>EqualTo</operator>
            <value>
                <elementReference>recordId</elementReference>
            </value>
        </filters>
        <getFirstRecordOnly>true</getFirstRecordOnly>
        <object>Claim__c</object>
        <storeOutputAutomatically>true</storeOutputAutomatically>
    </recordLookups>
    <screens>
        <name>Claim_Review_Screen</name>
        <label>Claim Review Screen</label>
        <locationX>182</locationX>
        <locationY>278</locationY>
        <allowBack>true</allowBack>
        <allowFinish>true</allowFinish>
        <allowPause>false</allowPause>
        <connector>
            <targetReference>Check_Decision</targetReference>
        </connector>
        <fields>
            <name>Claim_Details_Display</name>
            <fieldText>&lt;p&gt;&lt;b&gt;Claim ID:&lt;/b&gt; {!Get_Claim_Details.Name}&lt;/p&gt;&lt;p&gt;&lt;b&gt;Amount:&lt;/b&gt; {!Get_Claim_Details.Claim_Amount__c}&lt;/p&gt;&lt;p&gt;&lt;b&gt;Policy Type:&lt;/b&gt; {!Get_Claim_Details.Policy__r.RecordType.Name}&lt;/p&gt;</fieldText>
            <fieldType>DisplayText</fieldType>
        </fields>
        <fields>
            <name>Approval_Decision</name>
            <choiceReferences>Choice_Approve</choiceReferences>
            <choiceReferences>Choice_Reject</choiceReferences>
            <dataType>String</dataType>
            <fieldText>Approval Decision</fieldText>
            <fieldType>RadioButtons</fieldType>
            <isRequired>true</isRequired>
        </fields>
        <fields>
            <name>Approver_Comments</name>
            <fieldText>Approver Comments</fieldText>
            <fieldType>LargeTextArea</fieldType>
            <isRequired>false</isRequired>
        </fields>
        <showFooter>true</showFooter>
        <showHeader>true</showHeader>
    </screens>
    <start>
        <locationX>56</locationX>
        <locationY>0</locationY>
        <connector>
            <targetReference>Get_Claim_Details</targetReference>
        </connector>
    </start>
    <status>Active</status>
    <variables>
        <name>recordId</name>
        <dataType>String</dataType>
        <isCollection>false</isCollection>
        <isInput>true</isInput>
        <isOutput>false</isOutput>
    </variables>
</Flow>"""

quick_action_xml = """<?xml version="1.0" encoding="UTF-8"?>
<QuickAction xmlns="http://soap.sforce.com/2006/04/metadata">
    <flowDefinition>Claim_Approver_Screen_Flow</flowDefinition>
    <label>Approve/Reject Claim</label>
    <optionsCreateFeedItem>false</optionsCreateFeedItem>
    <type>Flow</type>
</QuickAction>"""

package_xml = """<?xml version="1.0" encoding="UTF-8"?>
<Package xmlns="http://soap.sforce.com/2006/04/metadata">
    <types>
        <members>Claim_Approver_Screen_Flow</members>
        <name>Flow</name>
    </types>
    <types>
        <members>Claim__c.Approve_Reject_Claim</members>
        <name>QuickAction</name>
    </types>
    <version>60.0</version>
</Package>"""

buf = io.BytesIO()
with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as z:
    z.writestr('package.xml', package_xml)
    z.writestr('flows/Claim_Approver_Screen_Flow.flow', flow_xml)
    z.writestr('quickActions/Claim__c.Approve_Reject_Claim.quickAction', quick_action_xml)

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
            print("Claim Approver Screen Flow & QuickAction SUCCESS:", success)
            if success != 'true':
                failures = croot.findall('.//{http://soap.sforce.com/2006/04/metadata}componentFailures')
                for fail in failures:
                    comp = fail.find('{http://soap.sforce.com/2006/04/metadata}fileName').text
                    prob = fail.find('{http://soap.sforce.com/2006/04/metadata}problem').text
                    print(f"FAILED: {comp} -> {prob}")
            break
else:
    print("Error:", res.text)
