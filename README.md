# Nifty 100 Financial Intelligence System

An enterprise-grade, full-stack financial intelligence platform I designed and engineered to track, analyze, and visualize 12 years of historical financial data for Nifty 100 companies. This system integrates an asynchronous Machine Learning pipeline, a high-performance secure REST API, and an interactive suite of analytical Power BI dashboards to convert raw corporate filings into institutional-grade investment insights.

---

## 🏗️ System Architecture & Data Flow

I engineered this platform using a split-stream decoupled architecture to isolate resource-heavy computing from the web server and ensure production stability:

[ Raw Financial Data / DB Rows ]
│
▼
┌───────────────────┐
│  Neon Postgres    │◀─── [ Power BI Dashboard Interface ]
└───────────────────┘             (Stream A: Visual Analytics)
▲
│ (Secure SSL Connection)
▼
┌───────────────────┐
│  Django REST API  │◀─── [ Swagger UI / Live REST Endpoints ]
└───────────────────┘             (Stream C: Production API)
▲
│ (Broker / Result Backend Transport)
▼
┌───────────────────┐
│   Upstash Redis   │
└───────────────────┘
▲
│ (Asynchronous Task Queue)
▼
┌───────────────────┐
│   Celery Worker   │◀─── [ Machine Learning Scoring Engine ]
└───────────────────┘             (Stream B: Heavy Computing Pipeline)


1. **Stream A (Visual Analytics Interface):** I established direct, native database connections from Power BI Desktop to my cloud data warehouse over encrypted channels, mapping out corporate structures into dynamic data models (`fact_balance_sheet`, `fact_cash_flow`, `fact_profit_loss`, `dim_company`).
2. **Stream B (Asynchronous Computing Pipeline):** To handle heavy ML scoring algorithms without slowing down my web layer, I set up a dedicated Celery worker background process using Upstash Redis as an ultra-low latency serverless cloud message broker.
3. **Stream C (Production API Management):** I built a robust Django REST API to cleanly serve database records to down-stream consumers, fully self-documented using OpenAPI standards.

---

## 🛠️ Tech Stack & Infrastructure

- **Frontend & Analytics:** Power BI Desktop, DAX (Data Analysis Expressions)
- **Backend Framework:** Django 6.0, Django REST Framework (DRF)
- **Asynchronous Task Queue:** Celery 5.6
- **Message Broker:** Upstash Redis (Serverless Cloud Redis)
- **Primary Data Warehouse:** Neon PostgreSQL (Serverless Cloud Database)
- **WSGI Production Server:** Gunicorn
- **Static File Manager:** WhiteNoise
- **API Documentation:** OpenAPI 3.0 via `drf-spectacular`
- **Cloud Hosting Platform:** Render (Web Service & Background Worker)

---

## 📊 Interactive Dashboards Built (Stream A)

I designed and built five tailored analytics pages for deep financial research:
1. **Health Overview Dashboard:** Provides high-level market tracking across different sectors using customized DAX metrics.
2. **Profitability Deep Dive:** Tracks operational efficiency trends and margin expansions over a 12-year window.
3. **Leverage (Debt) Analysis:** Evaluates credit risk metrics by tracking Total Borrowings alongside dynamic Debt-to-Equity and Interest Coverage quadrants to instantly reveal high-risk companies.
4. **Cash Flow Analysis:** Compares net operating cash engines against absolute Free Cash Flow generation over time.
5. **Company Deep Dive ("The Tear Sheet"):** A single-company master dashboard equipped with single-select slicer logic allowing users to pull up a full 12-year interactive financial report card for any specific company instantly.

---

## 🚀 Live Deployment & API Endpoints

I have fully deployed the backend system to production on **Render** connected with a serverless **Neon Postgres** database.

- **My Live API Endpoint:** https://nifty100-financial-intelligence-6y2s.onrender.com
- **My Interactive OpenAPI/Swagger Documentation:** https://nifty100-financial-intelligence-6y2s.onrender.com/api/docs/

### Key Endpoints:
- `GET /api/companies/` - Fetches metadata and financial profiles for listed Nifty 100 enterprises.
- `GET /api/schema/` - Generates the raw structural OpenAPI 3 YAML/JSON schema.

---

## 💻 Local Installation & Setup

If you want to run this project locally, follow these steps:

### Prerequisites
- Python 3.10+
- Git
- Credentials for a PostgreSQL and Redis instance (local or cloud)

### 1. Clone the Repository

bash
git clone [https://github.com/sayanacharjee16-del/nifty100-financial-intelligence.git](https://github.com/sayanacharjee16-del/nifty100-financial-intelligence.git)
cd "Building Nifty 100 Financial System"

### 2. Configure Virtual Environment & Install Dependencies

`Bash
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
pip install -r requirements.txt`

### 3. Set Up Environment Variables
Create a .env file in the root project directory (next to manage.py):

`Code snippet
SECRET_KEY=your_django_secret_key
DEBUG=True
NEON_DB_URL=your_postgresql_connection_string
UPSTASH_REDIS_URL=your_redis_connection_string`

### 4. Apply Database Migrations & Run Web Server

`Bash
python manage.py migrate
python manage.py runserver`

The interactive local documentation will now be available at http://127.0.0.1:8000/api/docs/

### 5. Start the Celery Worker (In a separate terminal)

`Bash
celery -A b100_intelligence worker -l info --pool=solo`

### 👤 Author
## Sayan Acharjee

## Data Analyst / Full-Stack Data Engineer

## Bangalore, India

