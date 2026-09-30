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

record_types = [
    """<metadata xsi:type="RecordType">
      <fullName>Policy__c.Property</fullName>
      <label>Property</label>
      <active>true</active>
      <description>Property Policy Record Type</description>
    </metadata>""",
    """<metadata xsi:type="RecordType">
      <fullName>Policy__c.Life</fullName>
      <label>Life</label>
      <active>true</active>
      <description>Life Policy Record Type</description>
    </metadata>""",
    """<metadata xsi:type="RecordType">
      <fullName>Claim__c.Accident</fullName>
      <label>Accident</label>
      <active>true</active>
      <description>Accident Claim Record Type</description>
    </metadata>""",
    """<metadata xsi:type="RecordType">
      <fullName>Claim__c.Property</fullName>
      <label>Property</label>
      <active>true</active>
      <description>Property Claim Record Type</description>
    </metadata>""",
    """<metadata xsi:type="RecordType">
      <fullName>Claim__c.Life</fullName>
      <label>Life</label>
      <active>true</active>
      <description>Life Claim Record Type</description>
    </metadata>"""
]

print("--- Creating Record Types ---")
create_metadata(record_types)

validation_rules = [
    """<metadata xsi:type="ValidationRule">
      <fullName>Policy__c.VIN_Must_Be_17_Characters</fullName>
      <active>true</active>
      <errorConditionFormula>AND( RecordType.DeveloperName = &quot;Auto&quot;, LEN( VIN__c )&lt;&gt; 17)</errorConditionFormula>
      <errorDisplayField>VIN__c</errorDisplayField>
      <errorMessage>The Vehicle Identification Number (VIN) must be exactly 17 characters long for Auto Policies.</errorMessage>
    </metadata>"""
]

print("--- Creating Validation Rule ---")
create_metadata(validation_rules)

field_sets = [
    """<metadata xsi:type="FieldSet">
      <fullName>Policy__c.Vehicle</fullName>
      <label>Vehicle</label>
      <description>In the policy object</description>
      <displayedFields>
        <field>VIN__c</field>
        <isFieldManaged>false</isFieldManaged>
        <isRequired>false</isRequired>
      </displayedFields>
      <displayedFields>
        <field>Model_Year__c</field>
        <isFieldManaged>false</isFieldManaged>
        <isRequired>false</isRequired>
      </displayedFields>
    </metadata>""",
    """<metadata xsi:type="FieldSet">
      <fullName>Policy__c.Property</fullName>
      <label>Property</label>
      <description>In the policy object</description>
      <displayedFields>
        <field>Square_Footage__c</field>
        <isFieldManaged>false</isFieldManaged>
        <isRequired>false</isRequired>
      </displayedFields>
      <displayedFields>
        <field>Year_Built__c</field>
        <isFieldManaged>false</isFieldManaged>
        <isRequired>false</isRequired>
      </displayedFields>
    </metadata>""",
    """<metadata xsi:type="FieldSet">
      <fullName>Policy__c.Life</fullName>
      <label>Life</label>
      <description>In the policy object</description>
      <displayedFields>
        <field>Beneficiary_Name__c</field>
        <isFieldManaged>false</isFieldManaged>
        <isRequired>false</isRequired>
      </displayedFields>
      <displayedFields>
        <field>Policy_Term_Months__c</field>
        <isFieldManaged>false</isFieldManaged>
        <isRequired>false</isRequired>
      </displayedFields>
    </metadata>"""
]

print("--- Creating Field Sets ---")
create_metadata(field_sets)
