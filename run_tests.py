import requests

with open("session_id.txt", "r") as f:
    sid = f.read().strip()

instance_url = "https://orgfarm-dd7f1a505a-dev-ed.develop.my.salesforce.com"
headers = {
    "Authorization": f"Bearer {sid}",
    "Content-Type": "application/json"
}

payload = {
    "tests": [
        {
            "classId": "01pbm00000VtUziAAF"
        }
    ]
}

res = requests.post(f"{instance_url}/services/data/v60.0/tooling/runTestsSynchronous", headers=headers, json=payload)
print("RunTests Status:", res.status_code)
data = res.json()
print("Successes:", len(data.get('successes', [])))
print("Failures:", len(data.get('failures', [])))
for s in data.get('successes', []):
    print("Test passed:", s['methodName'], s['time'])
for f in data.get('failures', []):
    print("Test failed:", f['methodName'], f['message'], f['stackTrace'])

# Coverage
cov_records = data.get('codeCoverage', [])
for cov in cov_records:
    name = cov.get('name')
    num_locations = cov.get('numLocations')
    num_locations_not_covered = cov.get('numLocationsNotCovered')
    pct = ((num_locations - num_locations_not_covered) / num_locations) * 100 if num_locations > 0 else 0
    print(f"Coverage for {name}: {pct:.1f}% ({num_locations - num_locations_not_covered}/{num_locations} lines)")
