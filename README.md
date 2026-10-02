# Multi-Line Insurance Policy and Claims Management System
# Team ID: 6ab4d71da238dc999eb5bc49

[![Salesforce](https://img.shields.io/badge/Platform-Salesforce%20Lightning-blue?logo=salesforce)](https://www.salesforce.com)
[![Apex Test Coverage](https://img.shields.io/badge/Apex%20Coverage-95.8%25-brightgreen)](force-app/main/default/classes/ClaimsAdjusterControllerTest.cls)
[![Automation](https://img.shields.io/badge/Flows%20%26%20Approvals-5%20Flows%20%7C%201%20Approval-orange)](#-process-automation--flows)
[![Architecture](https://img.shields.io/badge/Architecture-Multi--Line%20Insurance-purple)](#-architecture-overview)

A comprehensive, enterprise-grade **Salesforce Insurance Policy and Claims Management System** built for multi-line insurance carriers (Auto, Life, and Property). The solution automates end-to-end policy lifecycle management, dynamic premium calculations, intelligent multi-channel claim routing, role-based adjusters assignment, approval workflows, and interactive adjuster consoles using **Lightning Web Components (LWC)** and **Apex**.

---

## 📑 Table of Contents
- [System Architecture Overview](#-system-architecture-overview)
- [System Screenshots & Live Demonstration](#-system-screenshots--live-demonstration)
  - [1. Policy Management & Record Detail](#1-policy-management--record-detail)
  - [2. Policy-to-Claim Relationship](#2-policy-to-claim-relationship)
  - [3. Salesforce Process Automation & Flows](#3-salesforce-process-automation--flows)
  - [4. Queue-Based Routing & Workload Distribution](#4-queue-based-routing--workload-distribution)
  - [5. Public Groups & Regional Adjusters](#5-public-groups--regional-adjusters)
  - [6. Apex Execution & Automated Unit Tests](#6-apex-execution--automated-unit-tests)
- [Data Model & Custom Objects](#-data-model--custom-objects)
- [Process Automation & Flows](#-process-automation--flows)
- [Security & Access Control](#-security--access-control)
- [Apex & Lightning Web Components](#-apex--lightning-web-components)
- [Deployment & Setup Guide](#-deployment--setup-guide)
- [Verification & Testing](#-verification--testing)
- [Project Structure](#-project-structure)

---

## 🏗️ System Architecture Overview

```
                                +-----------------------------+
                                |  Customer / Agent Portal    |
                                +--------------+--------------+
                                               |
                                               v
                                   [ Policy Creation / Quote ]
                                               |
                                               v
                               +-------------------------------+
                               |     Policy__c (Auto/Life/Home)|
                               +---------------+---------------+
                                               |
                                               | (Master-Detail / Lookup)
                                               v
                               +-------------------------------+
                               |   Claim__c Submission Event   |
                               +---------------+---------------+
                                               |
                       +-----------------------+-----------------------+
                       |                                               |
                       v                                               v
        [ AutoQuoting & PremiumCalc ]                       [ ClaimRoutingFlow ]
                       |                                               |
                       |                               +---------------+---------------+
                       |                               |               |               |
                       v                               v               v               v
           [ Dynamic Risk Premium ]               Auto Queue       Life Queue    Property Queue
                                                       |               |               |
                                                       +-------+-------+---------------+
                                                               |
                                                               v
                                                [ Regional Public Groups ]
                                                  - CA Adjusters
                                                  - TX Adjusters
                                                               |
                                   +---------------------------+---------------------------+
                                   | Claim > $50,000?                                      |
                                   | YES                                                   | NO
                                   v                                                       v
                   [ High-Value Approval Process ]                          [ Claims Adjuster Dashboard ]
                   (Manager Review & Sign-Off)                               (Lightning Web Component)
```

---

## 📸 System Screenshots & Live Demonstration

The following screenshots are captured directly from the live Salesforce Developer Edition environment, showcasing the complete functionality and setup.

### 1. Policy Management & Record Detail

The system manages multi-line insurance policies across Auto, Life, and Property categories. Each record maintains comprehensive policyholder metadata, policy term, state jurisdiction, and risk underwriting data.

#### Policies Recently Viewed List View
Displays active policy records (`P - 0001` through `P - 0010`) within Salesforce Lightning Experience with standard actions (New, Import, Change Owner):

![Policies List View](salesforce_screenshots/p1.png)

#### Policy Record Detail (`P - 0010`)
Shows specific policy attributes, including Policy Type (`Home`), State (`TX`), Premium (`$3,100.00`), Square Footage (`1,800`), Year Built (`2005`), and assigned Owner:

![Policy Detail Record](salesforce_screenshots/p2.png)

---

### 2. Policy-to-Claim Relationship

Policies maintain a direct relational link to all associated incident claims. The related list view displays claim identifiers, claim payout amounts, approval statuses, and incident dates.

#### Related Claims List View
Policy `P - 0010` showing related Claim `C - 0011` with an incident amount of `$32,000.00` in `New` approval status:

![Policy Related Claims](salesforce_screenshots/p3.png)

---

### 3. Salesforce Process Automation & Flows

Automated business logic handles policy quoting, claim triage, regional policyholder synchronization, and interactive approvals without manual intervention.

#### Active Flow Definitions in Setup
Displays the active unmanaged flows configured in Salesforce:
- `AutoQuotingFlow` – Automated premium generation screen flow
- `Claim Approver Screen Flow` – Quick action screen flow for one-click claim disposition
- `Claim Policy Holder State Update` – Record-triggered flow syncing claimant state data
- `ClaimRoutingFlow` – Intelligent routing engine directing claims to designated queues

![Salesforce Flows List](salesforce_screenshots/p4.png)

---

### 4. Queue-Based Routing & Workload Distribution

Claims are automatically classified and routed to dedicated queues based on policy type and claim details, preventing backlogs and ensuring departmental specialization.

#### Queues Configuration
Configured queues supporting the `Claim__c` object:
- **Auto Queue** – Dedicated to vehicular and collision claims
- **Life Queue** – Dedicated to life and disability insurance claims
- **Property Queue** – Dedicated to residential and commercial real estate claims

![Configured Queues](salesforce_screenshots/p5.png)

---

### 5. Public Groups & Regional Adjusters

Public groups enable granular territory-based sharing and assignment for regional adjuster teams handling localized claims.

#### Public Groups Configuration
Configured regional adjuster groups:
- **Claim Adjusters - California** – Adjusters licensed in CA jurisdiction
- **Claim Adjusters - Texas** – Adjusters licensed in TX jurisdiction

![Public Groups](salesforce_screenshots/p6.png)

---

### 6. Apex Execution & Automated Unit Tests

Backend business logic and REST/LWC controllers are supported by a rigorous Apex test suite achieving **95.8% code coverage**, well exceeding the 75% Salesforce deployment threshold.

#### Developer Console Execution & Test Log
Salesforce Developer Console execution log confirming `ApexTestHandler` success across all unit tests and anonymous execution scripts:

![Apex Test Execution Log](salesforce_screenshots/p7.png)

---

## 🗄️ Data Model & Custom Objects

### 1. `Policy__c` (Custom Object)
Stores multi-line insurance contracts and underwriting variables.

| Field API Name | Data Type | Description |
|----------------|-----------|-------------|
| `Name` | Auto-Number (`P - {0000}`) | Unique policy identifier |
| `Customer__c` | Lookup (`Contact` / `Account`) | Associated policyholder |
| `Policy_Type__c` | Picklist (`Auto`, `Home`, `Life`) | Line of business |
| `Policy_State__c` | Text(2) | Two-letter state code (e.g., `TX`, `CA`) |
| `Policy_Start_Date__c`| Date | Effective inception date |
| `Policy_Term_Months__c`| Number(3, 0) | Duration of policy coverage |
| `Premium__c` | Currency(18, 2) | Annual/Term premium amount |
| `Square_Footage__c` | Number(6, 0) | Property square footage (Property line) |
| `Year_Built__c` | Number(4, 0) | Year structure was constructed |
| `VIN__c` | Text(17) | Vehicle Identification Number (Auto line) |
| `Model_Year__c` | Number(4, 0) | Vehicle model year |
| `Beneficiary_Name__c` | Text(100) | Designated beneficiary (Life line) |

### 2. `Claim__c` (Custom Object)
Tracks incident claims filed against active policies.

| Field API Name | Data Type | Description |
|----------------|-----------|-------------|
| `Name` | Auto-Number (`C - {0000}`) | Unique claim reference number |
| `Policy__c` | Master-Detail / Lookup | Associated policy reference |
| `Claim_Amount__c` | Currency(18, 2) | Total monetary claim amount requested |
| `Approval_Status__c` | Picklist | Status (`New`, `Pending Approval`, `Approved`, `Rejected`) |
| `Date_of_Loss__c` | Date/Time | Timestamp when the loss incident occurred |
| `Description__c` | Long Text Area(32768) | Detailed incident narrative |

---

## ⚡ Process Automation & Flows

| Flow Name | Type | Trigger / Mechanism | Purpose |
|-----------|------|---------------------|---------|
| `ClaimRoutingFlow` | Record-Triggered (Autolaunched) | `Claim__c` after insert | Inspects policy line (`Auto`, `Life`, `Property`) and routes claim ownership to the corresponding queue (`Auto Queue`, `Life Queue`, `Property Queue`). |
| `AutoQuotingFlow` | Screen Flow | Agent Utility / Record Action | Gathers policy input variables, invokes `PremiumCalculator.cls`, and instantly generates quote options. |
| `Claim Policy Holder State Update` | Record-Triggered (Autolaunched) | `Claim__c` before insert | Automatically inherits the state code from the parent `Policy__c` to ensure regional compliance. |
| `Claim_Approver_Screen_Flow` | Screen Flow | Quick Action Button (`Approve_Reject_Claim`) | Embeds an interactive modal on the Claim page allowing managers to enter comments and toggle approval status. |
| `Submission_Automation_Flow` | Autolaunched Flow | Claim Submission | Automates status updates, notifications, and task assignments upon initial claim filing. |

### 🛡️ High-Value Claim Approval Process
- **Entry Criteria:** `Claim_Amount__c > 50000.00`
- **Initial Submission:** Locks claim record from editing; sets `Approval_Status__c = 'Pending Approval'`.
- **Approval Actions:** Sets `Approval_Status__c = 'Approved'`, notifies claims manager, unlocks record for disbursement.
- **Rejection Actions:** Sets `Approval_Status__c = 'Rejected'`, logs reason in history, unlocks record.

---

## 🔒 Security & Access Control

Role-based access control (RBAC) is enforced through 3 custom permission sets:

| Permission Set | Target Persona | Permissions & Capabilities |
|----------------|----------------|----------------------------|
| `Insurance_Agent_Access` | Insurance Sales Agents | Full CRUD on `Policy__c`, Read-only on `Claim__c`, access to `AutoQuotingFlow`. |
| `Claims_Adjuster_Access` | Field & Desk Adjusters | Read on `Policy__c`, Read/Edit/Update on `Claim__c`, access to Adjuster Dashboard LWC. |
| `Claims_Manager_Access` | Claims Department Heads | Full CRUD on `Policy__c` & `Claim__c`, approval process administration, queue reassignment. |

---

## 💻 Apex & Lightning Web Components

### Apex Classes
- **`ClaimsAdjusterController.cls`**: `@AuraEnabled` controller powering the LWC dashboard. Exposes methods for querying claims by status, updating disposition, and calculating summary metrics.
- **`PremiumCalculator.cls`**: Core computational engine calculating risk-adjusted premiums based on property age, vehicle risk tiers, and coverage terms.
- **`ClaimsAdjusterControllerTest.cls`**: Unit test suite with comprehensive assertions covering edge cases, bulk data handling, and achieving **95.8% code coverage**.

### Lightning Web Components (LWC)
- **`claimsDashboardLwc`**: Interactive claims management dashboard for adjusters. Features real-time status filtering, aggregate claim metrics, and responsive layout.
- **`claimTileLwc`**: Reusable tile component rendering claim badges, priority indicators, and quick action buttons.

---

## 🚀 Deployment & Setup Guide

### Prerequisites
- [Salesforce CLI (`sf`)](https://developer.salesforce.com/tools/salesforcecli)
- Salesforce Developer Edition Org or Scratch Org
- Git

### Installation Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Ajay-710/Salesforce-NM.git
   cd Salesforce-NM
   ```

2. **Authenticate with your Salesforce Org:**
   ```bash
   sf org login web --alias myInsuranceOrg --set-default
   ```

3. **Deploy source metadata to the org:**
   ```bash
   sf project deploy start --source-dir force-app/
   ```

4. **Assign Permission Sets to your user:**
   ```bash
   sf org assign permset --name Insurance_Agent_Access
   sf org assign permset --name Claims_Adjuster_Access
   sf org assign permset --name Claims_Manager_Access
   ```

5. **Execute Unit Tests:**
   ```bash
   sf apex run test --class-names ClaimsAdjusterControllerTest --result-format human --code-coverage
   ```

---

## ✅ Verification & Testing

Run the automated verification script to validate all components deployed in the target environment:

```bash
python verify_all.py
```

**Verification Checklist:**
- [x] Custom Objects: `Policy__c`, `Claim__c` deployed
- [x] Custom Fields: Premium, Square Footage, VIN, Claim Amount, etc. verified
- [x] Record Types: Auto, Life, Property active
- [x] Flows: 5 Active automated flows verified
- [x] Queues: Auto, Life, and Property queues assigned
- [x] Public Groups: CA & TX Adjusters verified
- [x] Approval Process: Active and functional for claims > $50,000
- [x] Apex Test Suite: 95.8% code coverage (Passing)
- [x] Lightning Web Components: `claimsDashboardLwc` and `claimTileLwc` active

---

## 📁 Project Structure

```
Salesforce-NM/
├── force-app/
│   └── main/default/
│       ├── classes/
│       │   ├── ClaimsAdjusterController.cls
│       │   ├── ClaimsAdjusterController.cls-meta.xml
│       │   ├── ClaimsAdjusterControllerTest.cls
│       │   ├── ClaimsAdjusterControllerTest.cls-meta.xml
│       │   ├── PremiumCalculator.cls
│       │   └── PremiumCalculator.cls-meta.xml
│       ├── lwc/
│       │   ├── claimsDashboardLwc/
│       │   │   ├── claimsDashboardLwc.html
│       │   │   ├── claimsDashboardLwc.js
│       │   │   ├── claimsDashboardLwc.js-meta.xml
│       │   │   └── claimsDashboardLwc.css
│       │   └── claimTileLwc/
│       │       ├── claimTileLwc.html
│       │       ├── claimTileLwc.js
│       │       ├── claimTileLwc.js-meta.xml
│       │       └── claimTileLwc.css
│       ├── objects/
│       │   ├── Policy__c/
│       │   └── Claim__c/
│       ├── permissionsets/
│       │   ├── Insurance_Agent_Access.permissionset-meta.xml
│       │   ├── Claims_Adjuster_Access.permissionset-meta.xml
│       │   └── Claims_Manager_Access.permissionset-meta.xml
│       ├── queues/
│       │   ├── Auto_Queue.queue-meta.xml
│       │   ├── Life_Queue.queue-meta.xml
│       │   └── Property_Queue.queue-meta.xml
│       └── quickActions/
│           └── Claim__c.Approve_Reject_Claim.quickAction
├── salesforce_screenshots/
│   ├── p1.png          # Policies List View
│   ├── p2.png          # Policy Detail Record (P-0010)
│   ├── p3.png          # Related Claims List (C-0011)
│   ├── p4.png          # Flow Definitions in Setup
│   ├── p5.png          # Claims Routing Queues
│   ├── p6.png          # Regional Adjuster Public Groups
│   └── p7.png          # Apex Execution & Tests Log
├── sfdx-project.json
├── verify_all.py
└── README.md
```

---

## 👨‍💻 Author & Acknowledgements
- Developed by **Ajay Pendem** as part of the Final Year Capstone Project.
- Built on the **Salesforce Customer 360 Platform**.
