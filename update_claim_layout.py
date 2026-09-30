import requests

with open("session_id.txt", "r") as f:
    sid = f.read().strip()

instance_url = "https://orgfarm-dd7f1a505a-dev-ed.develop.my.salesforce.com"
headers = {
    "Authorization": f"Bearer {sid}",
    "Content-Type": "application/json"
}

layout_id = "00hbm00000bbsufAAA"
get_res = requests.get(f"{instance_url}/services/data/v60.0/tooling/sobjects/Layout/{layout_id}", headers=headers)
layout_data = get_res.json()
metadata = layout_data['Metadata']

metadata['platformActionList'] = {
    "actionListContext": "Record",
    "platformActionListItems": [
        {"actionName": "Edit", "actionType": "StandardButton", "sortOrder": 0},
        {"actionName": "Delete", "actionType": "StandardButton", "sortOrder": 1},
        {"actionName": "Clone", "actionType": "StandardButton", "sortOrder": 2},
        {"actionName": "Claim__c.Approve_Reject_Claim", "actionType": "QuickAction", "sortOrder": 3},
        {"actionName": "Submit", "actionType": "StandardButton", "sortOrder": 4}
    ]
}

# Also ensure custom fields are on layout sections if needed
# Let's inspect layoutSections to ensure Claim_Amount__c, Approval_Status__c, Policy__c, Adjuster__c are on layout
# They are typically added, but let's check
patch_payload = {
    "Metadata": metadata
}

patch_res = requests.patch(f"{instance_url}/services/data/v60.0/tooling/sobjects/Layout/{layout_id}", headers=headers, json=patch_payload)
print("Patch Layout Status:", patch_res.status_code, patch_res.text)
