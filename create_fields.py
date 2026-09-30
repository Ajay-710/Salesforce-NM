import requests
import xml.etree.ElementTree as ET

with open("session_id.txt", "r") as f:
    sid = f.read().strip()

url = "https://orgfarm-dd7f1a505a-dev-ed.develop.my.salesforce.com/services/Soap/m/60.0"
headers = {
    "Content-Type": "text/xml; charset=UTF-8",
    "SOAPAction": "createMetadata"
}

def create_metadata(metadata_xml_list):
    # createMetadata accepts up to 10 items per call
    for i in range(0, len(metadata_xml_list), 10):
        chunk = metadata_xml_list[i:i+10]
        chunk_str = "\n".join(chunk)
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
      {chunk_str}
    </createMetadata>
  </env:Body>
</env:Envelope>"""
        res = requests.post(url, data=body, headers=headers)
        if res.status_code == 200:
            root = ET.fromstring(res.text)
            results = root.findall('.//{http://soap.sforce.com/2006/04/metadata}result')
            for r in results:
                fname = r.find('{http://soap.sforce.com/2006/04/metadata}fullName')
                success = r.find('{http://soap.sforce.com/2006/04/metadata}success')
                fname_str = fname.text if fname is not None else "unknown"
                success_str = success.text if success is not None else "false"
                errors = r.findall('{http://soap.sforce.com/2006/04/metadata}errors')
                err_msg = ""
                for e in errors:
                    msg = e.find('{http://soap.sforce.com/2006/04/metadata}message')
                    if msg is not None: err_msg += " " + msg.text
                print(f"[{fname_str}] success={success_str} {err_msg}")
        else:
            print("HTTP Error:", res.status_code, res.text[:300])

policy_fields = [
    """<metadata xsi:type="CustomField">
      <fullName>Policy__c.Customer__c</fullName>
      <label>Customer</label>
      <type>Lookup</type>
      <referenceTo>Contact</referenceTo>
      <relationshipLabel>Policies</relationshipLabel>
      <relationshipName>Policies</relationshipName>
      <required>false</required>
    </metadata>""",
    """<metadata xsi:type="CustomField">
      <fullName>Policy__c.Model_Year__c</fullName>
      <label>Model Year</label>
      <type>Text</type>
      <length>5</length>
      <required>false</required>
    </metadata>""",
    """<metadata xsi:type="CustomField">
      <fullName>Policy__c.Policy_Term_Months__c</fullName>
      <label>Policy Term Months</label>
      <type>Number</type>
      <precision>18</precision>
      <scale>0</scale>
      <required>false</required>
    </metadata>""",
    """<metadata xsi:type="CustomField">
      <fullName>Policy__c.Premium__c</fullName>
      <label>Premium</label>
      <type>Currency</type>
      <precision>16</precision>
      <scale>2</scale>
      <required>false</required>
    </metadata>""",
    """<metadata xsi:type="CustomField">
      <fullName>Policy__c.Square_Footage__c</fullName>
      <label>Square Footage</label>
      <type>Number</type>
      <precision>18</precision>
      <scale>0</scale>
      <required>false</required>
    </metadata>""",
    """<metadata xsi:type="CustomField">
      <fullName>Policy__c.VIN__c</fullName>
      <label>VIN</label>
      <type>Text</type>
      <length>20</length>
      <required>false</required>
    </metadata>""",
    """<metadata xsi:type="CustomField">
      <fullName>Policy__c.Year_Built__c</fullName>
      <label>Year Built</label>
      <type>Text</type>
      <length>5</length>
      <required>false</required>
    </metadata>""",
    """<metadata xsi:type="CustomField">
      <fullName>Policy__c.Policy_State__c</fullName>
      <label>Policy State</label>
      <type>Picklist</type>
      <valueSet>
        <restricted>false</restricted>
        <valueSetDefinition>
          <sorted>false</sorted>
          <value>
            <fullName>CA</fullName>
            <default>false</default>
            <label>CA</label>
          </value>
          <value>
            <fullName>TX</fullName>
            <default>false</default>
            <label>TX</label>
          </value>
          <value>
            <fullName>NY</fullName>
            <default>false</default>
            <label>NY</label>
          </value>
          <value>
            <fullName>FL</fullName>
            <default>false</default>
            <label>FL</label>
          </value>
        </valueSetDefinition>
      </valueSet>
    </metadata>"""
]

print("--- Creating Policy__c Fields ---")
create_metadata(policy_fields)

claim_fields = [
    """<metadata xsi:type="CustomField">
      <fullName>Claim__c.Adjuster__c</fullName>
      <label>Adjuster</label>
      <type>Lookup</type>
      <referenceTo>User</referenceTo>
      <relationshipLabel>Claims</relationshipLabel>
      <relationshipName>Claims</relationshipName>
      <required>false</required>
    </metadata>""",
    """<metadata xsi:type="CustomField">
      <fullName>Claim__c.Approval_Status__c</fullName>
      <label>Approval Status</label>
      <type>Picklist</type>
      <valueSet>
        <restricted>true</restricted>
        <valueSetDefinition>
          <sorted>false</sorted>
          <value>
            <fullName>New</fullName>
            <default>true</default>
            <label>New</label>
          </value>
          <value>
            <fullName>Submitted for Approval</fullName>
            <default>false</default>
            <label>Submitted for Approval</label>
          </value>
          <value>
            <fullName>Approved</fullName>
            <default>false</default>
            <label>Approved</label>
          </value>
          <value>
            <fullName>Rejected</fullName>
            <default>false</default>
            <label>Rejected</label>
          </value>
        </valueSetDefinition>
      </valueSet>
    </metadata>""",
    """<metadata xsi:type="CustomField">
      <fullName>Claim__c.Claim_Amount__c</fullName>
      <label>Claim Amount</label>
      <type>Currency</type>
      <precision>16</precision>
      <scale>2</scale>
      <required>false</required>
    </metadata>""",
    """<metadata xsi:type="CustomField">
      <fullName>Claim__c.Date_of_Loss__c</fullName>
      <label>Date of Loss</label>
      <type>DateTime</type>
      <required>false</required>
    </metadata>""",
    """<metadata xsi:type="CustomField">
      <fullName>Claim__c.Description__c</fullName>
      <label>Description</label>
      <type>LongTextArea</type>
      <length>32768</length>
      <visibleLines>3</visibleLines>
      <required>false</required>
    </metadata>""",
    """<metadata xsi:type="CustomField">
      <fullName>Claim__c.Policy__c</fullName>
      <label>Policy</label>
      <type>Lookup</type>
      <referenceTo>Policy__c</referenceTo>
      <relationshipLabel>Claims</relationshipLabel>
      <relationshipName>Claims</relationshipName>
      <required>false</required>
    </metadata>""",
    """<metadata xsi:type="CustomField">
      <fullName>Claim__c.Policy_Account_Holder_State__c</fullName>
      <label>Policy Account Holder State</label>
      <type>Text</type>
      <length>50</length>
      <required>false</required>
    </metadata>"""
]

print("--- Creating Claim__c Fields ---")
create_metadata(claim_fields)
