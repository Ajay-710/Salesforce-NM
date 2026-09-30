import requests

with open("session_id.txt", "r") as f:
    sid = f.read().strip()

instance_url = "https://orgfarm-dd7f1a505a-dev-ed.develop.my.salesforce.com"
headers = {
    "Authorization": f"Bearer {sid}",
    "Content-Type": "application/json"
}

# 1. Check Test Results and Coverage
print("=== 1. Apex Test Run & Code Coverage ===")
res_test = requests.post(f"{instance_url}/services/data/v60.0/tooling/runTestsSynchronous", headers=headers, json={
    "tests": [{"classId": "01pbm00000VtUziAAF"}]
})
td = res_test.json()
print("Test Successes:", len(td.get('successes', [])))
print("Test Failures:", len(td.get('failures', [])))
for cov in td.get('codeCoverage', []):
    num = cov.get('numLocations', 0)
    not_cov = cov.get('numLocationsNotCovered', 0)
    pct = ((num - not_cov) / num) * 100 if num > 0 else 0
    print(f"Coverage for {cov.get('name')}: {pct:.1f}% ({num - not_cov}/{num} lines)")

# 2. Check Flows Status
print("\n=== 2. Deployed Flows ===")
flows = requests.get(f"{instance_url}/services/data/v60.0/tooling/query/?q=SELECT+Definition.DeveloperName,VersionNumber,Status+FROM+Flow+WHERE+Status=\'Active\'", headers=headers).json()
for r in flows.get('records', []):
    name = r.get('Definition', {}).get('DeveloperName')
    if name in ['AutoQuotingFlow', 'ClaimRoutingFlow', 'Claim_Policy_Holder_State_Update', 'Submission_Automation_Flow', 'Claim_Approver_Screen_Flow']:
        print(f"Flow: {name} (Version {r.get('VersionNumber')}) -> Status: {r.get('Status')}")

# 3. Check Custom Objects & Fields
print("\n=== 3. Custom Objects, Fields & Record Types ===")
for obj in ['Policy__c', 'Claim__c']:
    desc = requests.get(f"{instance_url}/services/data/v60.0/sobjects/{obj}/describe", headers=headers).json()
    rts = [rt['name'] for rt in desc.get('recordTypeInfos', []) if rt['name'] != 'Master']
    print(f"{obj}: {len(desc.get('fields', []))} fields, Record Types: {rts}")

# 4. Check Approval Process
print("\n=== 4. Approval Process ===")
ap_res = requests.get(f"{instance_url}/services/data/v60.0/query/?q=SELECT+Id,Name,State,TableEnumOrId+FROM+ProcessDefinition+WHERE+TableEnumOrId=\'Claim__c\'", headers=headers)
if ap_res.status_code == 200:
    for r in ap_res.json().get('records', []):
        print(f"Approval Process: {r.get('Name')} -> State: {r.get('State')}")

# 5. Check Sharing Rules
print("\n=== 5. Sharing Rules ===")
sr_res = requests.get(f"{instance_url}/services/data/v60.0/tooling/query/?q=SELECT+Id,DeveloperName+FROM+SharingCriteriaRule", headers=headers)
if sr_res.status_code == 200:
    for r in sr_res.json().get('records', []):
        print(f"Sharing Rule: {r.get('DeveloperName')}")

# 6. Check Permission Sets
print("\n=== 6. Permission Sets ===")
ps = requests.get(f"{instance_url}/services/data/v60.0/query/?q=SELECT+Id,Name,Label+FROM+PermissionSet+WHERE+Name+IN+(\'Insurance_Agent_Access\',\'Claims_Manager_Access\',\'Claims_Adjuster_Access\')", headers=headers).json()
for r in ps.get('records', []):
    print(f"Permission Set: {r.get('Label')} ({r.get('Name')})")

# 7. Check Queues & Public Groups
print("\n=== 7. Queues & Public Groups ===")
g_res = requests.get(f"{instance_url}/services/data/v60.0/query/?q=SELECT+Id,Name,Type+FROM+Group+WHERE+Name+IN+(\'Auto Queue\',\'Property Queue\',\'Life Queue\',\'Claim Adjusters- California\',\'Claim Adjusters- Texas\')", headers=headers).json()
for r in g_res.get('records', []):
    print(f"{r.get('Type')}: {r.get('Name')}")

# 8. Check LWCs
print("\n=== 8. Lightning Web Components ===")
lwc = requests.get(f"{instance_url}/services/data/v60.0/tooling/query/?q=SELECT+Id,DeveloperName+FROM+LightningComponentBundle+WHERE+DeveloperName+IN+(\'claimsDashboardLwc\',\'claimTileLwc\')", headers=headers).json()
for r in lwc.get('records', []):
    print(f"LWC: {r.get('DeveloperName')}")
