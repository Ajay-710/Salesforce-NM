# Multi-Line Insurance Policy and Claims Management System

A comprehensive Salesforce-based Insurance Policy and Claims Management System built as a final year project. This system manages policies, automates claims processing, and provides intelligent routing for a multi-line insurance business.

## 🏗️ Architecture Overview

This project is built on the **Salesforce Platform** using:
- **Apex** (backend logic & test classes)
- **Lightning Web Components (LWC)** (UI components)
- **Salesforce Flows** (process automation)
- **Metadata API** (deployment)

## 🔑 Key Features

### Data Model
| Object | Record Types | Description |
|--------|-------------|-------------|
| `Policy__c` | Auto, Life, Property | Stores insurance policies |
| `Claim__c` | Accident, Life, Property | Tracks insurance claims |

### Automation
- **ClaimRoutingFlow** – Automatically routes claims to the correct queue (Auto, Life, Property)
- **Claim_Policy_Holder_State_Update** – Updates policyholder state on claim submission
- **Submission_Automation_Flow** – Triggers automation when a claim is submitted
- **Claim_Approver_Screen_Flow** – Screen flow for claim approvers to approve/reject
- **AutoQuotingFlow** – Auto-generates premium quotes using `PremiumCalculator`

### Security & Access Control
Three permission sets control role-based access:
- `Insurance_Agent_Access` – For insurance agents creating/managing policies
- `Claims_Manager_Access` – For managers overseeing claims
- `Claims_Adjuster_Access` – For adjusters processing individual claims

### Queues & Groups
- **Auto Queue**, **Life Queue**, **Property Queue** – For claim routing
- **Claim Adjusters – California**, **Claim Adjusters – Texas** – Regional adjuster groups

### Approval Process
- **High Value Claim Approval** – Triggers approval workflow for claims exceeding $50,000

## 🧩 Components

### Apex Classes
| Class | Purpose |
|-------|---------|
| `ClaimsAdjusterController.cls` | Backend controller for the Claims Dashboard LWC |
| `PremiumCalculator.cls` | Calculates premiums based on policy type and risk |
| `ClaimsAdjusterControllerTest.cls` | Test class with **95.8% code coverage** |

### Lightning Web Components
| Component | Description |
|-----------|-------------|
| `claimsDashboardLwc` | Main dashboard for claims adjusters |
| `claimTileLwc` | Individual claim tile card in the dashboard |

## 🚀 Deployment

### Prerequisites
- Salesforce Developer Org
- Salesforce CLI (SFDX)
- Python 3.x with `requests` library

### Setup Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/Ajay-710/Salesforce-NM.git
   cd Salesforce-NM
   ```

2. Authenticate with your Salesforce org:
   ```bash
   sf org login web --alias myorg
   ```

3. Deploy the source:
   ```bash
   sf project deploy start --source-dir force-app/
   ```

4. Run tests:
   ```bash
   sf apex run test --class-names ClaimsAdjusterControllerTest --result-format human
   ```

## ✅ Verification

All components can be verified by running:
```bash
python verify_all.py
```

**Expected Output:**
- ✅ 2 test successes, 0 failures
- ✅ 95.8% code coverage
- ✅ 5 Active Flows
- ✅ Active Approval Process
- ✅ 3 Permission Sets
- ✅ 5 Queues & Groups
- ✅ 2 LWC Components

## 📁 Project Structure

```
├── force-app/
│   └── main/default/
│       ├── classes/
│       │   ├── ClaimsAdjusterController.cls
│       │   ├── ClaimsAdjusterControllerTest.cls
│       │   └── PremiumCalculator.cls
│       └── lwc/
│           ├── claimsDashboardLwc/
│           └── claimTileLwc/
├── sfdx-project.json
└── verify_all.py
```

## 👨‍💻 Technologies Used
- Salesforce Apex
- Salesforce Lightning Web Components (LWC)
- Salesforce Flow Builder
- Salesforce Metadata API
- Python (deployment scripts)

## 📝 License
This project is developed as part of a final year academic project.
