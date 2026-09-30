import requests

with open("session_id.txt", "r") as f:
    sid = f.read().strip()

instance_url = "https://orgfarm-dd7f1a505a-dev-ed.develop.my.salesforce.com"
headers = {
    "Authorization": f"Bearer {sid}",
    "Content-Type": "application/json"
}

# 1. Create a Permission Set: "Insurance_Full_Access"
ps_data = {
    "Name": "Insurance_Full_Access",
    "Label": "Insurance Full Access",
    "PermissionsModifyAllData": False
}
res_ps = requests.post(f"{instance_url}/services/data/v60.0/sobjects/PermissionSet", headers=headers, json=ps_data)
print("Create PermissionSet:", res_ps.status_code, res_ps.text)
if res_ps.status_code == 201:
    ps_id = res_ps.json()['id']
else:
    # Query it
    q = requests.get(f"{instance_url}/services/data/v60.0/query/?q=SELECT+Id+FROM+PermissionSet+WHERE+Name=\'Insurance_Full_Access\'", headers=headers)
    ps_id = q.json()['records'][0]['Id']

print("PermissionSet ID:", ps_id)

# 2. Grant ObjectPermissions for Policy__c and Claim__c
for obj in ['Policy__c', 'Claim__c']:
    obj_perm = {
        "ParentId": ps_id,
        "SobjectType": obj,
        "PermissionsCreate": True,
        "PermissionsRead": True,
        "PermissionsEdit": True,
        "PermissionsDelete": True,
        "PermissionsViewAllRecords": True,
        "PermissionsModifyAllRecords": True
    }
    r = requests.post(f"{instance_url}/services/data/v60.0/sobjects/ObjectPermissions", headers=headers, json=obj_perm)
    print(f"ObjectPermissions {obj}:", r.status_code, r.text)

# 3. Grant FieldPermissions
fields_to_grant = [
    'Policy__c.Beneficiary_Name__c',
    'Policy__c.Customer__c',
    'Policy__c.Model_Year__c',
    'Policy__c.Policy_Start_Date__c',
    'Policy__c.Policy_Term_Months__c',
    'Policy__c.Premium__c',
    'Policy__c.Square_Footage__c',
    'Policy__c.VIN__c',
    'Policy__c.Year_Built__c',
    'Policy__c.Policy_State__c',
    'Claim__c.Adjuster__c',
    'Claim__c.Approval_Status__c',
    'Claim__c.Claim_Amount__c',
    'Claim__c.Date_of_Loss__c',
    'Claim__c.Description__c',
    'Claim__c.Policy__c',
    'Claim__c.Policy_Account_Holder_State__c'
]

for f in fields_to_grant:
    fp = {
        "ParentId": ps_id,
        "SobjectType": f.split('.')[0],
        "Field": f,
        "PermissionsRead": True,
        "PermissionsEdit": True
    }
    r = requests.post(f"{instance_url}/services/data/v60.0/sobjects/FieldPermissions", headers=headers, json=fp)
    print(f"FieldPermission {f}:", r.status_code, r.text)

# 4. Assign Permission Set to current user
user_res = requests.get(f"{instance_url}/services/data/v60.0/query/?q=SELECT+Id+FROM+User+WHERE+Username=\'pendemajay7.64257f50286e@agentforce.com\'", headers=headers)
user_id = user_res.json()['records'][0]['Id']

psa = {
    "PermissionSetId": ps_id,
    "AssigneeId": user_id
}
r_psa = requests.post(f"{instance_url}/services/data/v60.0/sobjects/PermissionSetAssignment", headers=headers, json=psa)
print("PermissionSetAssignment:", r_psa.status_code, r_psa.text)
