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
<Flow xmlns="http://soap.sforce.com/2006/04/metadata" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <actionCalls>
        <name>Calculate_Premium_Action</name>
        <label>Calculate Premium Action</label>
        <locationX>176</locationX>
        <locationY>638</locationY>
        <actionName>PremiumCalculator</actionName>
        <actionType>apex</actionType>
        <connector>
            <targetReference>Update_Policy_With_Premium</targetReference>
        </connector>
        <flowTransactionModel>Automatic</flowTransactionModel>
        <inputParameters>
            <name>policyId</name>
            <value>
                <elementReference>varPolicyId</elementReference>
            </value>
        </inputParameters>
        <outputParameters>
            <assignToReference>varCalculatedPremium</assignToReference>
            <name>output</name>
        </outputParameters>
    </actionCalls>
    <apiVersion>60.0</apiVersion>
    <dynamicChoiceSets>
        <name>Policy_State_Choices</name>
        <dataType>Picklist</dataType>
        <picklistField>Policy_State__c</picklistField>
        <picklistObject>Policy__c</picklistObject>
    </dynamicChoiceSets>
    <environments>Default</environments>
    <interviewLabel>AutoQuotingFlow {!$Flow.CurrentDateTime}</interviewLabel>
    <label>AutoQuotingFlow</label>
    <processMetadataValues>
        <name>BuilderType</name>
        <value>
            <stringValue>LightningFlowBuilder</stringValue>
        </value>
    </processMetadataValues>
    <processType>Flow</processType>
    <recordCreates>
        <name>Create_Draft_Policy</name>
        <label>Create Draft Policy</label>
        <locationX>176</locationX>
        <locationY>518</locationY>
        <assignRecordIdToReference>varPolicyId</assignRecordIdToReference>
        <connector>
            <targetReference>Calculate_Premium_Action</targetReference>
        </connector>
        <inputAssignments>
            <field>Customer__c</field>
            <value>
                <elementReference>Customer_Lookup.recordId</elementReference>
            </value>
        </inputAssignments>
        <inputAssignments>
            <field>Model_Year__c</field>
            <value>
                <elementReference>Model_Year</elementReference>
            </value>
        </inputAssignments>
        <inputAssignments>
            <field>Policy_Start_Date__c</field>
            <value>
                <elementReference>Policy_Start_Date</elementReference>
            </value>
        </inputAssignments>
        <inputAssignments>
            <field>Policy_State__c</field>
            <value>
                <elementReference>Policy_State</elementReference>
            </value>
        </inputAssignments>
        <inputAssignments>
            <field>Policy_Type__c</field>
            <value>
                <stringValue>Auto</stringValue>
            </value>
        </inputAssignments>
        <inputAssignments>
            <field>RecordTypeId</field>
            <value>
                <elementReference>Get_Vehicle_RT_ID.Id</elementReference>
            </value>
        </inputAssignments>
        <inputAssignments>
            <field>VIN__c</field>
            <value>
                <elementReference>VIN</elementReference>
            </value>
        </inputAssignments>
        <object>Policy__c</object>
    </recordCreates>
    <recordLookups>
        <name>Get_Vehicle_RT_ID</name>
        <label>Get Vehicle RT ID</label>
        <locationX>176</locationX>
        <locationY>158</locationY>
        <assignNullValuesIfNoRecordsFound>false</assignNullValuesIfNoRecordsFound>
        <connector>
            <targetReference>New_Auto_Policy_Quote_Basic_Information</targetReference>
        </connector>
        <filterLogic>and</filterLogic>
        <filters>
            <field>SobjectType</field>
            <operator>EqualTo</operator>
            <value>
                <stringValue>Policy__c</stringValue>
            </value>
        </filters>
        <filters>
            <field>DeveloperName</field>
            <operator>EqualTo</operator>
            <value>
                <stringValue>Auto</stringValue>
            </value>
        </filters>
        <getFirstRecordOnly>true</getFirstRecordOnly>
        <object>RecordType</object>
        <storeOutputAutomatically>true</storeOutputAutomatically>
    </recordLookups>
    <recordUpdates>
        <name>Update_Policy_With_Premium</name>
        <label>Update Policy With Premium</label>
        <locationX>176</locationX>
        <locationY>758</locationY>
        <filterLogic>and</filterLogic>
        <filters>
            <field>Id</field>
            <operator>EqualTo</operator>
            <value>
                <elementReference>varPolicyId</elementReference>
            </value>
        </filters>
        <inputAssignments>
            <field>Premium__c</field>
            <value>
                <elementReference>varCalculatedPremium</elementReference>
            </value>
        </inputAssignments>
        <object>Policy__c</object>
    </recordUpdates>
    <screens>
        <name>New_Auto_Policy_Quote_Basic_Information</name>
        <label>New Auto Policy Quote - Basic Information</label>
        <locationX>176</locationX>
        <locationY>278</locationY>
        <allowBack>false</allowBack>
        <allowFinish>true</allowFinish>
        <allowPause>false</allowPause>
        <connector>
            <targetReference>Vehicle_Specific_Details</targetReference>
        </connector>
        <fields>
            <name>Screen_1_Policy_Basics</name>
            <fieldText>&lt;p&gt;&lt;b&gt;Auto Policy Quote - Basic Information&lt;/b&gt;&lt;/p&gt;</fieldText>
            <fieldType>DisplayText</fieldType>
        </fields>
        <fields>
            <name>Customer_Lookup</name>
            <extensionName>flowruntime:lookup</extensionName>
            <fieldType>ComponentInstance</fieldType>
            <inputParameters>
                <name>fieldApiName</name>
                <value>
                    <stringValue>Customer__c</stringValue>
                </value>
            </inputParameters>
            <inputParameters>
                <name>label</name>
                <value>
                    <stringValue>Policy Holder</stringValue>
                </value>
            </inputParameters>
            <inputParameters>
                <name>objectApiName</name>
                <value>
                    <stringValue>Policy__c</stringValue>
                </value>
            </inputParameters>
            <isRequired>true</isRequired>
            <storeOutputAutomatically>true</storeOutputAutomatically>
        </fields>
        <fields>
            <name>Policy_Start_Date</name>
            <dataType>Date</dataType>
            <fieldText>Policy Start Date</fieldText>
            <fieldType>InputField</fieldType>
            <isRequired>true</isRequired>
        </fields>
        <fields>
            <name>Policy_State</name>
            <choiceReferences>Policy_State_Choices</choiceReferences>
            <dataType>String</dataType>
            <fieldText>Policy State</fieldText>
            <fieldType>DropdownBox</fieldType>
            <isRequired>true</isRequired>
        </fields>
        <showFooter>true</showFooter>
        <showHeader>true</showHeader>
    </screens>
    <screens>
        <name>Vehicle_Specific_Details</name>
        <label>Vehicle-Specific Details</label>
        <locationX>176</locationX>
        <locationY>398</locationY>
        <allowBack>true</allowBack>
        <allowFinish>true</allowFinish>
        <allowPause>false</allowPause>
        <connector>
            <targetReference>Create_Draft_Policy</targetReference>
        </connector>
        <fields>
            <name>Screen_2_Vehicle_Details</name>
            <fieldText>&lt;p&gt;&lt;b&gt;Vehicle Details&lt;/b&gt;&lt;/p&gt;</fieldText>
            <fieldType>DisplayText</fieldType>
        </fields>
        <fields>
            <name>VIN</name>
            <dataType>String</dataType>
            <fieldText>VIN</fieldText>
            <fieldType>InputField</fieldType>
            <isRequired>true</isRequired>
        </fields>
        <fields>
            <name>Model_Year</name>
            <dataType>String</dataType>
            <fieldText>Model Year</fieldText>
            <fieldType>InputField</fieldType>
            <isRequired>false</isRequired>
        </fields>
        <showFooter>true</showFooter>
        <showHeader>true</showHeader>
    </screens>
    <start>
        <locationX>50</locationX>
        <locationY>0</locationY>
        <connector>
            <targetReference>Get_Vehicle_RT_ID</targetReference>
        </connector>
    </start>
    <status>Active</status>
    <variables>
        <name>varCalculatedPremium</name>
        <dataType>Currency</dataType>
        <isCollection>false</isCollection>
        <isInput>false</isInput>
        <isOutput>false</isOutput>
        <scale>2</scale>
    </variables>
    <variables>
        <name>varPolicyId</name>
        <dataType>String</dataType>
        <isCollection>false</isCollection>
        <isInput>false</isInput>
        <isOutput>false</isOutput>
    </variables>
</Flow>"""

package_xml = """<?xml version="1.0" encoding="UTF-8"?>
<Package xmlns="http://soap.sforce.com/2006/04/metadata">
    <types>
        <members>AutoQuotingFlow</members>
        <name>Flow</name>
    </types>
    <version>60.0</version>
</Package>"""

buf = io.BytesIO()
with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as z:
    z.writestr('package.xml', package_xml)
    z.writestr('flows/AutoQuotingFlow.flow', flow_xml)

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
            print("AutoQuotingFlow SUCCESS:", success)
            if success != 'true':
                failures = croot.findall('.//{http://soap.sforce.com/2006/04/metadata}componentFailures')
                for fail in failures:
                    comp = fail.find('{http://soap.sforce.com/2006/04/metadata}fileName').text
                    prob = fail.find('{http://soap.sforce.com/2006/04/metadata}problem').text
                    print(f"FAILED: {comp} -> {prob}")
            break
else:
    print("Error:", res.text)
