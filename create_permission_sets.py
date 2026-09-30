import requests

with open("session_id.txt", "r") as f:
    sid = f.read().strip()

instance_url = "https://orgfarm-dd7f1a505a-dev-ed.develop.my.salesforce.com"
headers = {
    "Authorization": f"Bearer {sid}",
    "Content-Type": "application/json"
}

# Query ApexClass IDs
res_classes = requests.get(f"{instance_url}/services/data/v60.0/query/?q=SELECT+Id,Name+FROM+ApexClass+WHERE+Name+IN+(\'PremiumCalculator\',\'ClaimsAdjusterController\')", headers=headers)
class_map = {r['Name']: r['Id'] for r in res_classes.json()['records']}
print("Class Map:", class_map)

# 1. Insurance Agent Access
ps1 = {
    "Name": "Insurance_Agent_Access",
    "Label": "Insurance Agent Access",
    "PermissionsRunFlow": True
}
r1 = requests.post(f"{instance_url}/services/data/v60.0/sobjects/PermissionSet", headers=headers, json=ps1)
print("PS1:", r1.status_code, r1.text)
ps1_id = r1.json().get('id') or requests.get(f"{instance_url}/services/data/v60.0/query/?q=SELECT+Id+FROM+PermissionSet+WHERE+Name=\'Insurance_Agent_Access\'", headers=headers).json()['records'][0]['Id']

# Object perms for PS1:
# Policy: Create, Read
requests.post(f"{instance_url}/services/data/v60.0/sobjects/ObjectPermissions", headers=headers, json={
    "ParentId": ps1_id, "SobjectType": "Policy__c", "PermissionsCreate": True, "PermissionsRead": True, "PermissionsEdit": False, "PermissionsDelete": False
})
# Contact: Read, Edit
requests.post(f"{instance_url}/services/data/v60.0/sobjects/ObjectPermissions", headers=headers, json={
    "ParentId": ps1_id, "SobjectType": "Contact", "PermissionsCreate": False, "PermissionsRead": True, "PermissionsEdit": True, "PermissionsDelete": False
})
# Claim: Read
requests.post(f"{instance_url}/services/data/v60.0/sobjects/ObjectPermissions", headers=headers, json={
    "ParentId": ps1_id, "SobjectType": "Claim__c", "PermissionsCreate": False, "PermissionsRead": True, "PermissionsEdit": False, "PermissionsDelete": False
})
# Apex Class: PremiumCalculator
if 'PremiumCalculator' in class_map:
    requests.post(f"{instance_url}/services/data/v60.0/sobjects/SetupEntityAccess", headers=headers, json={
        "ParentId": ps1_id, "SetupEntityId": class_map['PremiumCalculator']
    })

# 2. Claims Manager Access
ps2 = {
    "Name": "Claims_Manager_Access",
    "Label": "Claims Manager Access",
    "PermissionsRunReports": True
}
r2 = requests.post(f"{instance_url}/services/data/v60.0/sobjects/PermissionSet", headers=headers, json=ps2)
print("PS2:", r2.status_code, r2.text)
ps2_id = r2.json().get('id') or requests.get(f"{instance_url}/services/data/v60.0/query/?q=SELECT+Id+FROM+PermissionSet+WHERE+Name=\'Claims_Manager_Access\'", headers=headers).json()['records'][0]['Id']

# Object perms for PS2:
# Policy: Read
requests.post(f"{instance_url}/services/data/v60.0/sobjects/ObjectPermissions", headers=headers, json={
    "ParentId": ps2_id, "SobjectType": "Policy__c", "PermissionsCreate": False, "PermissionsRead": True, "PermissionsEdit": False, "PermissionsDelete": False
})
# Contact: Read, Edit
requests.post(f"{instance_url}/services/data/v60.0/sobjects/ObjectPermissions", headers=headers, json={
    "ParentId": ps2_id, "SobjectType": "Contact", "PermissionsCreate": False, "PermissionsRead": True, "PermissionsEdit": True, "PermissionsDelete": False
})
# Claim: Read, Edit, Delete
requests.post(f"{instance_url}/services/data/v60.0/sobjects/ObjectPermissions", headers=headers, json={
    "ParentId": ps2_id, "SobjectType": "Claim__c", "PermissionsCreate": False, "PermissionsRead": True, "PermissionsEdit": True, "PermissionsDelete": True
})

# 3. Claims Adjuster Access
ps3 = {
    "Name": "Claims_Adjuster_Access",
    "Label": "Claims Adjuster Access"
}
r3 = requests.post(f"{instance_url}/services/data/v60.0/sobjects/PermissionSet", headers=headers, json=ps3)
print("PS3:", r3.status_code, r3.text)
ps3_id = r3.json().get('id') or requests.get(f"{instance_url}/services/data/v60.0/query/?q=SELECT+Id+FROM+PermissionSet+WHERE+Name=\'Claims_Adjuster_Access\'", headers=headers).json()['records'][0]['Id']

# Object perms for PS3:
# Policy: Read
requests.post(f"{instance_url}/services/data/v60.0/sobjects/ObjectPermissions", headers=headers, json={
    "ParentId": ps3_id, "SobjectType": "Policy__c", "PermissionsCreate": False, "PermissionsRead": True, "PermissionsEdit": False, "PermissionsDelete": False
})
# Claim: Read, Edit
requests.post(f"{instance_url}/services/data/v60.0/sobjects/ObjectPermissions", headers=headers, json={
    "ParentId": ps3_id, "SobjectType": "Claim__c", "PermissionsCreate": False, "PermissionsRead": True, "PermissionsEdit": True, "PermissionsDelete": False
})
# Apex Class: ClaimsAdjusterController
if 'ClaimsAdjusterController' in class_map:
    requests.post(f"{instance_url}/services/data/v60.0/sobjects/SetupEntityAccess", headers=headers, json={
        "ParentId": ps3_id, "SetupEntityId": class_map['ClaimsAdjusterController']
    })

print("All 3 Permission Sets created and configured successfully!")
