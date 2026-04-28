# 🚀 SchemaSwift – Conversational Database Assistant using MCP and RAG

SchemaSwift is a **Telegram-based AI assistant** that enables natural-language interaction with a PostgreSQL database using **Model Context Protocol (MCP)** and **Retrieval-Augmented Generation (RAG)**.

It combines LLM reasoning, secure tool execution, semantic retrieval, and role-based access control into a hybrid conversational database system.
---

# 📑 Table of Contents

* [Project Overview](#-project-overview)
* [Key Features](#-key-features)
* [System Architecture](#-system-architecture)
* [Model Context Protocol (MCP)](#-model-context-protocol-mcp)
* [Retrieval-Augmented Generation (RAG)](#-retrieval-augmented-generation-rag)
* [LLM-Based Intent Routing](#-llm-based-intent-routing)
* [Role-Based Access Control (RBAC)](#-role-based-access-control-rbac)
* [Email Approval Workflow](#-email-approval-workflow)
* [Multi-Agent Pipeline Design](#-multi-agent-pipeline-design)
* [Guardrails and Safety](#-guardrails-and-safety)
* [Observability and Monitoring](#-observability-and-monitoring)
* [Database Schema](#-database-schema)
* [Project Structure](#-project-structure)
* [Technologies Used](#-technologies-used)
* [Installation](#-installation)
* [Environment Variables](#-environment-variables-env)
* [Running the Project](#-running-the-project)
* [Example Usage](#-example-usage)
* [Demo Resources](#-demo-resources)
* [Concept Coverage Mapping](#-concept-coverage-mapping)
* [Future Enhancements](#-future-enhancements)
* [Conclusion](#-conclusion)

---

# 📌 Project Overview

Traditional database interaction requires SQL knowledge. SchemaSwift removes this barrier by allowing users to interact with structured data using **natural language via Telegram**.

The Groq LLM automatically decides whether a request should:

* execute a structured MCP database tool
* retrieve semantic knowledge using RAG
* return guidance/help responses

This creates a hybrid conversational database assistant architecture.

---

# ✨ Key Features

* Natural-language database interaction via Telegram
* Groq-powered LLM intent routing
* Model Context Protocol (MCP) execution layer
* Retrieval-Augmented Generation (RAG) semantic explanations
* Role-Based Access Control (RBAC)
* Email-based admin approval workflow
* Activity logging for monitoring
* Automatic embedding refresh after database updates

---

# 🧠 System Architecture

SchemaSwift follows a modular layered architecture:

```
User
↓
Telegram Bot Interface
↓
LLM Intent Router (Groq)
↓
Decision Layer
├── MCP Tool Execution Path
└── RAG Retrieval Path
```

Architecture layers:

1. Telegram Interface Layer
2. Intent Routing Layer (Groq LLM)
3. Access Control Layer
4. MCP Execution Layer
5. RAG Retrieval Layer
6. ChromaDB Vector Store
7. PostgreSQL Database

📊 **Architecture Diagram**

<img width="1600" height="864" alt="image" src="https://github.com/user-attachments/assets/4bfbd993-6698-40c6-b3ea-cfa38d5fda80" />

---

# ⚙️ Model Context Protocol (MCP)

SchemaSwift uses MCP to safely execute database operations through registered tools instead of direct SQL queries.

Implemented MCP tools:

* insert_product
* fetch_products
* delete_product
* register_user
* get_user_role
* request_access
* fetch_activity_logs
* search_products
* check_product_exists
* list_pending_requests

This ensures secure and modular interaction between the LLM and database.

---

# 🔎 Retrieval-Augmented Generation (RAG)

SchemaSwift supports explanation-style answers using semantic retrieval.

Embeddings are generated from:

* users table
* access_requests table
* activity_logs table

Stored in:

```
ChromaDB Vector Store
```

Example:

User:

```
Who are the current users?
```

System retrieves embeddings and generates contextual explanation response.

---

# 🤖 LLM-Based Intent Routing

SchemaSwift uses Groq LLM to automatically determine whether a query requires:

* MCP tool execution
* RAG semantic retrieval
* help response

No keyword-based routing is used.

---

# 🔐 Role-Based Access Control (RBAC)

Two permission levels exist:

| Role   | Permissions          |
| ------ | -------------------- |
| Viewer | Read-only access     |
| Admin  | Full database access |

Workflow:

1. User requests elevated access
2. Email notification sent to admin
3. Admin approves via secure link
4. Role updated automatically

---

# 📧 Email Approval Workflow

Access requests trigger automated email notifications.

Admin receives options:

* Approve Viewer
* Approve Admin
* Reject Request

Approval updates database immediately via FastAPI approval service.

---

# 🧩 Multi-Agent Pipeline Design

SchemaSwift operates as a modular agent pipeline:

| Agent          | Responsibility                 |
| -------------- | ------------------------------ |
| IntentAgent    | Detect user intent             |
| AccessAgent    | Validate permissions           |
| ExecutionAgent | Execute MCP tools              |
| RAGAgent       | Generate explanation responses |

---

# 🛡 Guardrails and Safety

Security mechanisms include:

* Role-based permission enforcement
* Approval-based privilege escalation
* Structured JSON tool invocation
* Restricted MCP tool execution

These safeguards prevent unauthorized database operations.

---

# 📊 Observability and Monitoring

The `activity_logs` table records:

* user actions
* tool execution
* access requests
* system events

Provides full execution traceability.

---

# 🗄 Database Schema

| Table           | Purpose                         |
| --------------- | ------------------------------- |
| users           | Stores Telegram users and roles |
| products        | Stores product records          |
| access_requests | Stores approval workflow        |
| activity_logs   | Stores execution history        |

---

# 📁 Project Structure

```
schemaswift/
├── bot/
├── llm/
├── mcp_server/
├── rag/
├── app/
├── approval_api/
├── scripts/
├── run_bot.py
├── run_mcp.py
└── requirements.txt
```

---

# 🧰 Technologies Used

* Python
* Telegram Bot API
* Groq LLM
* Model Context Protocol (MCP)
* LangChain
* ChromaDB
* PostgreSQL
* SQLAlchemy
* FastAPI

---

# ⚡ Installation

Clone repository:

```
git clone https://github.com/pgvishnu526/schemaswift.git
cd schemaswift
```

Create environment:

```
python -m venv venv
venv\Scripts\activate
```

Install dependencies:

```
pip install -r requirements.txt
```

Initialize database:

```
python scripts/init_db.py
```

Seed admin user:

```
python scripts/seed_admin.py
```

---

# 🔑 Environment Variables (.env)

Create `.env` file:

```
DATABASE_URL=postgresql://user:password@localhost:5432/project_db
TELEGRAM_BOT_TOKEN=your_bot_token
GROQ_API_KEY=your_groq_api_key
ADMIN_EMAIL=admin_mail (your mail where you give the approval)
SMTP_EMAIL=bot_mail( bot_mail you need to add this one to by giving another one new mail)
SMTP_PASSWORD=app_password ( need to create the app password from the bot_mail id and does not give gmail password)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=465
APP_BASE_URL=http://localhost:8000
```

---

# ▶ Running the Project

Start approval API:

```
uvicorn approval_api.approval_server:app --port 8000
```

Start MCP server (optional):

```
python run_mcp.py
```

Run Telegram bot:

```
python run_bot.py
```

---

# 💬 Example Usage

Try:

```
Add laptop
Show products
Delete chair
Who are current users?
Show recent activity
I need admin access
```

---

# 📂 Demo Resources

📊 Presentation Slides:

[View PPT](https://docs.google.com/presentation/d/1HwCPUvfgNd__-AxuWLrmZPh27ZWcG6dz/edit?usp=sharing&ouid=102861785575667136980&rtpof=true&sd=true)

🎥 Execution Demo:

[Watch Demo Video](https://drive.google.com/file/d/1fWxQ5FB120KzrtM5qyPV_GcEP274j_3q/view?usp=sharing)

---

# 📚 Concept Coverage Mapping

| Concept              | Implementation                     |
| -------------------- | ---------------------------------- |
| MCP                  | Tool-based execution architecture  |
| RAG                  | Semantic retrieval from embeddings |
| Multi-agent pipeline | Modular routing architecture       |
| Guardrails           | RBAC + approval workflow           |
| Observability        | activity_logs monitoring           |

---

# 🔮 Future Enhancements

* Web dashboard interface
* Voice interaction support
* Cloud deployment (Docker + AWS)
* Analytics monitoring dashboard

---

# 📌 Conclusion

SchemaSwift demonstrates a hybrid conversational database assistant combining:

* MCP structured execution
* RAG semantic reasoning
* Groq LLM routing
* RBAC security workflow

to enable safe and intelligent natural-language interaction with relational databases.
