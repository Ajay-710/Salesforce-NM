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

layout_xml = """<?xml version="1.0" encoding="UTF-8"?>
<Layout xmlns="http://soap.sforce.com/2006/04/metadata">
    <layoutSections>
        <customLabel>false</customLabel>
        <detailHeading>false</detailHeading>
        <editHeading>true</editHeading>
        <label>Information</label>
        <layoutColumns>
            <layoutItems>
                <behavior>Readonly</behavior>
                <field>Name</field>
            </layoutItems>
            <layoutItems>
                <behavior>Edit</behavior>
                <field>Customer__c</field>
            </layoutItems>
            <layoutItems>
                <behavior>Edit</behavior>
                <field>Policy_Type__c</field>
            </layoutItems>
            <layoutItems>
                <behavior>Edit</behavior>
                <field>Policy_State__c</field>
            </layoutItems>
            <layoutItems>
                <behavior>Edit</behavior>
                <field>Policy_Start_Date__c</field>
            </layoutItems>
            <layoutItems>
                <behavior>Edit</behavior>
                <field>Policy_Term_Months__c</field>
            </layoutItems>
            <layoutItems>
                <behavior>Edit</behavior>
                <field>Premium__c</field>
            </layoutItems>
        </layoutColumns>
        <layoutColumns>
            <layoutItems>
                <behavior>Edit</behavior>
                <field>OwnerId</field>
            </layoutItems>
            <layoutItems>
                <behavior>Edit</behavior>
                <field>RecordTypeId</field>
            </layoutItems>
            <layoutItems>
                <behavior>Edit</behavior>
                <field>VIN__c</field>
            </layoutItems>
            <layoutItems>
                <behavior>Edit</behavior>
                <field>Model_Year__c</field>
            </layoutItems>
            <layoutItems>
                <behavior>Edit</behavior>
                <field>Square_Footage__c</field>
            </layoutItems>
            <layoutItems>
                <behavior>Edit</behavior>
                <field>Year_Built__c</field>
            </layoutItems>
            <layoutItems>
                <behavior>Edit</behavior>
                <field>Beneficiary_Name__c</field>
            </layoutItems>
        </layoutColumns>
        <style>TwoColumnsTopToBottom</style>
    </layoutSections>
    <layoutSections>
        <customLabel>false</customLabel>
        <detailHeading>false</detailHeading>
        <editHeading>true</editHeading>
        <label>System Information</label>
        <layoutColumns>
            <layoutItems>
                <behavior>Readonly</behavior>
                <field>CreatedById</field>
            </layoutItems>
        </layoutColumns>
        <layoutColumns>
            <layoutItems>
                <behavior>Readonly</behavior>
                <field>LastModifiedById</field>
            </layoutItems>
        </layoutColumns>
        <style>TwoColumnsTopToBottom</style>
    </layoutSections>
    <layoutSections>
        <customLabel>false</customLabel>
        <detailHeading>false</detailHeading>
        <editHeading>true</editHeading>
        <label>Custom Links</label>
        <layoutColumns/>
        <layoutColumns/>
        <layoutColumns/>
        <style>CustomLinks</style>
    </layoutSections>
    <relatedLists>
        <fields>NAME</fields>
        <fields>Claim_Amount__c</fields>
        <fields>Approval_Status__c</fields>
        <fields>Date_of_Loss__c</fields>
        <relatedList>Claim__c.Policy__c</relatedList>
    </relatedLists>
</Layout>"""

package_xml = """<?xml version="1.0" encoding="UTF-8"?>
<Package xmlns="http://soap.sforce.com/2006/04/metadata">
    <types>
        <members>Policy__c-Policy Layout</members>
        <name>Layout</name>
    </types>
    <version>60.0</version>
</Package>"""

buf = io.BytesIO()
with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as z:
    z.writestr('package.xml', package_xml)
    z.writestr('layouts/Policy__c-Policy Layout.layout', layout_xml)

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
            print("Policy Layout SUCCESS:", success)
            break
else:
    print("Error:", res.text)
