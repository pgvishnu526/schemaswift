# SchemaSwift – Conversational Database Assistant using MCP and RAG

**A Telegram-based AI assistant that enables natural-language interaction with PostgreSQL using Model Context Protocol (MCP) and Retrieval-Augmented Generation (RAG).**

# Project Overview

SchemaSwift is a conversational database assistant that converts user messages into structured database operations or semantic explanation responses. Users interact through Telegram, providing a seamless and intuitive interface for database management.

The system routes requests using a **Groq-powered LLM intent router**. Based on the user's natural language input, the router dynamically decides whether to execute actions via the **MCP tool layer** (for structured CRUD operations) or retrieve contextual explanations through a **RAG pipeline** (for knowledge-based queries).

# Key Features

*   **Natural language database interaction** via Telegram
*   **LLM-driven intent routing** using Groq
*   **Model Context Protocol (MCP)** tool execution layer
*   **Retrieval-Augmented Generation (RAG)** using ChromaDB embeddings
*   **Role-Based Access Control (RBAC)**
*   **Email-based admin approval workflow**
*   **Activity monitoring** through a dedicated logs table
*   **Automatic embedding refresh** after database updates

# System Architecture

SchemaSwift employs a modular, layered architecture to ensure scalability, security, and separation of concerns:

1.  **Telegram Interface Layer**: Handles user interaction and message polling.
2.  **Intent Routing Layer (Groq LLM)**: Analyzes user input to determine the required action.
3.  **Access Control Layer**: Validates user permissions before executing privileged tools.
4.  **MCP Execution Layer**: Executes structured database operations via registered tools.
5.  **RAG Retrieval Layer**: Performs semantic search on database records for explanation-based queries.
6.  **Vector Database (ChromaDB)**: Stores and manages document embeddings for RAG.
7.  **Relational Database (PostgreSQL)**: The primary store for users, products, logs, and access requests.

### Pipeline Description:
**User** → **Intent Router** → **Decision** → **MCP Tool** (Structured Action) **OR** **RAG Engine** (Explanation) → **Database Response**

# Model Context Protocol (MCP)

SchemaSwift uses the Model Context Protocol (MCP) to separate user interaction logic from database execution logic. This standardized architecture allows the LLM to interact with the database through a set of well-defined, secure tools.

### Implemented MCP Tools:
*   `insert_product`: Adds a new product record.
*   `fetch_products`: Retrieves a list of all products.
*   `delete_product`: Removes a product from the database.
*   `register_user`: Handles new user registration.
*   `get_user_role`: Queries the current role of a user.
*   `request_access`: Submits a request for elevated privileges.
*   `fetch_activity_logs`: Retrieves system activity history.
*   `search_products`: Performs a search for products by name.
*   `check_product_exists`: Validates the existence of a specific product.
*   `list_pending_requests`: Lists access requests awaiting approval.

# Retrieval-Augmented Generation (RAG)

SchemaSwift leverages RAG to provide intelligent, context-aware answers to user queries that require an understanding of the database state beyond simple CRUD.

Database records from the `users`, `access_requests`, and `activity_logs` tables are converted into high-dimensional embeddings using HuggingFace models. These embeddings are stored in **ChromaDB**. When a user asks a semantic question, the system retrieves relevant context from the vector store to generate a natural language explanation.

**Example:**
*   **User query**: "Who are the current users?"
*   **System Action**: Retrieves context from the vector store and generates an explanation response listing the users and their roles based on the retrieved records.

# LLM-Based Intent Routing

The system utilizes the **Groq LLM** to detect user intent dynamically. Unlike traditional keyword-based bots, SchemaSwift understands the semantics of the request.

The LLM decides whether to:
1.  **Execute an MCP tool**: For structured tasks like "Add a product".
2.  **Trigger the RAG pipeline**: For descriptive tasks like "Summarize recent activity".
3.  **Return a help response**: For general inquiries or ambiguous commands.

No hardcoded keyword routing is used, allowing for high flexibility in user phrasing.

# Role-Based Access Control (RBAC)

Security is a core component of SchemaSwift. The system enforces strict access levels:
*   **Viewer Role**: Read-only access to products and logs.
*   **Admin Role**: Full database access, including modification and deletion.

**Workflow**:
1.  User requests admin access via the bot.
2.  An email notification is automatically sent to the administrator.
3.  The admin approves the request via a secure link.
4.  The user's role is updated automatically in the database.

# Email Approval Workflow

Access requests trigger automated email notifications to ensure that privilege escalation is audited and authorized.

The Admin receives an email with the following options:
*   **Approve Viewer**
*   **Approve Admin**
*   **Reject Request**

The system processes the admin's choice via a FastAPI-based approval server and updates the database state immediately.

# Multi-Agent Pipeline Design

The system is conceptualized as a collaboration between specialized agents:
*   **IntentAgent**: Analyzes the message and determines the high-level action.
*   **AccessAgent**: Validates the user's permissions for the determined action.
*   **ExecutionAgent**: Orchestrates the call to the appropriate MCP tool.
*   **RAGAgent**: Handles vector retrieval and explanation generation.

These agents collaborate sequentially to process user requests safely and accurately.

# Guardrails and Safety

SchemaSwift implements multiple layers of safety:
*   **Role-based permission enforcement**: Prevents unauthorized tool execution.
*   **Approval-based privilege escalation**: No self-promotion of roles.
*   **Structured JSON tool execution**: Prevents prompt injection from affecting database logic.
*   **Restricted action selection**: The LLM can only interact with the database through predefined MCP tools.

# Observability and Monitoring

The `activity_logs` table provides comprehensive monitoring and traceability:
*   **User actions**: Tracks who did what.
*   **Tool execution**: Logs which tools were called and their results.
*   **Access requests**: Records the history of permission changes.
*   **System events**: Captures errors and internal state changes.

# Database Schema

The PostgreSQL database consists of the following primary tables:
*   `users`: Stores Telegram user IDs, usernames, and assigned roles.
*   `products`: Stores product records including names and categories.
*   `access_requests`: Stores pending and historical approval requests.
*   `activity_logs`: Stores a detailed history of all system activities.

# Project Folder Structure

```text
schemaswift/
├── bot/                # Telegram bot interface and MCP client
├── llm/                # LLM prompts and routing logic
├── mcp_server/         # MCP server implementation and tools
├── rag/                # RAG pipeline and embedding logic
├── app/                # Core database schemas and services
├── approval_api/       # FastAPI server for email approvals
├── scripts/            # Utility scripts (init db, seeds)
├── run_bot.py          # Main entry point for the bot
├── run_mcp.py          # Entry point for the MCP server
└── requirements.txt    # Project dependencies
```

# Technologies Used

*   **Python**: Core programming language.
*   **Telegram Bot API**: User interaction interface.
*   **Groq LLM**: High-performance LLM for routing and RAG.
*   **Model Context Protocol (MCP)**: Tool execution framework.
*   **LangChain**: RAG and LLM orchestration.
*   **ChromaDB**: Vector database for embeddings.
*   **PostgreSQL**: Primary relational database.
*   **SQLAlchemy**: ORM for database interactions.
*   **FastAPI**: API server for the approval workflow.

# Installation Instructions

1.  **Clone the repository**:
    ```bash
    git clone [https://github.com/your-repo/schemaswift.git](https://github.com/pgvishnu526/schemaswift)
    cd schemaswift
    ```
2.  **Create a virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
4.  **Configure the .env file**: Create a `.env` file in the root directory 

5.  **Initialize the database**:
    ```bash
    python scripts/init_db.py
    ```
6.  **Seed the admin user**:
    ```bash
    python scripts/seed_admin.py
    ```

# Environment Variables (.env)

The following environment variables are required for the project to run:

```env
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
GROQ_API_KEY=your_groq_api_key
DATABASE_URL=postgresql://user:password@localhost/schemaswift
SMTP_EMAIL=your_smtp_email
SMTP_PASSWORD=your_smtp_password
ADMIN_EMAIL=admin@example.com
APP_BASE_URL=http://your-server-url

example :
you need some credentials and .env file should contains:
    
    DATABASE_URL= postgresql://postgres:pass_word@localhost:5432/project_db (your path)
    TELEGRAM_BOT_TOKEN= telegram_bot_api_key
    GROQ_API_KEY= groq_api key
    ADMIN_EMAIL= your_personal_mail(if need create new mail - you give approval from this mail only)
    SMTP_EMAIL= your_bot_mail (schemaswfit.bot@gmail.com - is mine gmail to send the request mail and you need to create app password from this mail id )
    SMTP_PASSWORD=#your_password (need app password not gmail password)
    SMTP_SERVER=smtp.gmail.com
    SMTP_PORT=465
    APP_BASE_URL=http://localhost:8000
```

# Running the Project

Follow these steps to start the SchemaSwift ecosystem:

1.  **Start the Approval API Server**:
    ```bash
    uvicorn approval_api.approval_server:app --port 8000
    ```
2.  **Start the MCP Server**:
    The MCP server is typically managed by the bot, but can be tested independently via:
    ```bash
    python run_mcp.py
    ```
3.  **Run the Telegram Bot**:
    ```bash
    python run_bot.py
    ```

# Example Usage

Once the bot is running, you can interact with it using commands such as:
*   "Add a new laptop to the database"
*   "Show me all the products we have"
*   "Delete the chair with ID 5"
*   "Who are the current users and what are their roles?"
*   "Show me the recent system activity"
*   "I need admin access to manage products"

# Concept Coverage Mapping

*   **MCP**: Implemented a tool-based execution architecture for secure database operations.
*   **RAG**: Integrated semantic retrieval from ChromaDB embeddings for knowledge-based queries.
*   **Multi-agent pipeline**: Modularized logic into specialized agents for routing, access, and execution.
*   **Guardrails**: Enforced RBAC and manual approval gates for critical operations.
*   **Observability**: Centralized logging in the `activity_logs` table for full system traceability.

# Future Enhancements

*   **Web Dashboard Interface**: A visual management console for admins.
*   **Voice Interaction Support**: Enabling voice commands via Telegram.
*   **Cloud Deployment**: Containerization with Docker and deployment to AWS/GCP.
*   **Advanced Analytics Monitoring**: Integrated dashboards for usage trends and system health.

# Conclusion

SchemaSwift demonstrates a sophisticated hybrid conversational database assistant architecture. By integrating MCP, RAG, LLM-based routing, and RBAC security, it provides a safe, intelligent, and highly accessible way to interact with relational data through natural language.
