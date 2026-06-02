# CRM Donation System

A centralized, secure, and scalable Customer Relationship Management (CRM) platform for hospital fundraising operations. Built with Django and Django REST Framework.

## Features

### 1. Donor & Stakeholder Management
- Comprehensive donor profiles for individuals, corporates, CSR contributors, foundations, welfare/Zakat donors, event sponsors, HNIs, and vendors
- Contact information, donation history, engagement records, and communication logs
- Document management (MoUs, proposals, agreements, receipts)
- Account manager / relationship ownership assignment
- Donor segmentation and search

### 2. Fundraising & Campaign Management
- End-to-end campaign planning and execution
- Pledge tracking with outstanding balance computation
- Donation recording linked to campaigns and pledges
- Event management with participant tracking
- Pipeline visibility: campaign status, goal vs. raised amounts

### 3. Communication & Engagement Automation
- Email template library (acknowledgements, reminders, invitations, Zakat receipts)
- Per-donor communication logs (email, SMS, WhatsApp, call, meeting)
- Bulk communication targeting (segmented outreach)
- All interactions automatically logged per donor

### 4. Finance Integration & Financial Controls
- Automated, sequential receipt numbering (`RCP-YYYY-NNNNN`)
- General, Zakat, Sadaqah, Sponsorship, and CSR receipt types
- Payment tracking: Cash, Cheque, Bank Transfer, Online, POS
- Restricted and unrestricted fund allocation per payment
- Approval workflow for payments, receipts, and pledges
- Audit trail via Django admin logs

### 5. Reporting & Management Dashboards
- **Dashboard summary**: active donors, active campaigns, total raised, outstanding pledges
- **Campaign performance**: donation count and totals vs. goals per campaign
- **Donor retention**: retained, new, and lapsed donors; retention rate year-on-year
- **Financial reconciliation**: breakdowns by payment mode and status

### 6. Workflow Automation & Task Management
- Tasks with type, priority, status, assignee, due date, and donor linkage
- Reminders linked to tasks (pledge due, follow-up, meeting, recurring donor alerts, payment pending)

### 7. User Access & Security
- Django's built-in role-based authentication
- Session and Basic authentication for the REST API
- All endpoints require authentication by default
- Admin site with fine-grained model permissions per user/group

## Tech Stack

- **Backend**: Python 3.12 / Django 4.2+ / Django REST Framework
- **Database**: SQLite (development) — easily switchable to PostgreSQL
- **File storage**: Local filesystem (`media/`) — can be swapped for S3/Azure
- **API**: RESTful JSON API with filtering, search, ordering, and pagination

## Project Structure

```
crmdonation/
├── manage.py
├── requirements.txt
├── crmdonation/        # Project settings and root URL config
├── donors/             # Donor & stakeholder management
├── campaigns/          # Campaigns, pledges, donations, events
├── communications/     # Email templates, communication logs, bulk comms
├── finance/            # Receipts, payments, fund allocations, approvals
├── workflow/           # Tasks and reminders
└── reports/            # Dashboard and reporting API views
```

## API Endpoints

| Prefix | Resource |
|--------|----------|
| `/api/donors/` | Donor CRUD + search/filter |
| `/api/donor-documents/` | Donor document uploads |
| `/api/donor-engagements/` | Engagement / meeting logs |
| `/api/campaigns/` | Campaign management |
| `/api/pledges/` | Pledge tracking |
| `/api/donations/` | Donation records |
| `/api/events/` | Event management |
| `/api/event-participants/` | Event attendance |
| `/api/receipts/` | Receipt generation |
| `/api/payments/` | Payment tracking |
| `/api/fund-allocations/` | Restricted / unrestricted fund allocation |
| `/api/approvals/` | Approval workflows |
| `/api/email-templates/` | Email template library |
| `/api/communication-logs/` | Per-donor communication history |
| `/api/bulk-communications/` | Bulk outreach campaigns |
| `/api/tasks/` | Task management |
| `/api/reminders/` | Scheduled reminders |
| `/api/reports/dashboard/` | Dashboard summary |
| `/api/reports/campaign-performance/` | Campaign KPIs |
| `/api/reports/donor-retention/` | Year-on-year donor retention |
| `/api/reports/financial-reconciliation/` | Payment reconciliation |

## Setup & Installation

```bash
# 1. Clone the repository
git clone https://github.com/munafs4s/crmdonation.git
cd crmdonation

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Apply database migrations
python manage.py migrate

# 5. Create a superuser (admin)
python manage.py createsuperuser

# 6. Run the development server
python manage.py runserver
```

Then visit:
- **Admin panel**: http://127.0.0.1:8000/admin/
- **API root**: http://127.0.0.1:8000/api/
- **API auth**: http://127.0.0.1:8000/api-auth/

## Running Tests

```bash
python manage.py test --verbosity=2
```

All 39 tests should pass.
