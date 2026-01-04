# AI Hospital Receptionist System

An intelligent, secure, and deterministic chatbot for hospital patient intake. Built with React, FastAPI, LangGraph, and Supabase.

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Vercel-000000?style=for-the-badge&logo=vercel&logoColor=white)](https://ai-receptionist-system.vercel.app)

## Features

-   **Deterministic Triage**: Automatically routes patients to **General**, **Emergency**, or **Mental Health** wards based on symptoms.
-   **Strict Data Collection**: Enforces collection of Name, Age, and Query to ensure complete records.
-   **Secure Persistence**: Stores patient data in **Supabase (PostgreSQL)** using Row Level Security (RLS) bypass via Service Role.
-   **Webhook Integration**: Triggers external workflows (e.g., Relay.app, Zapier) upon successful registration.
-   **Full-Viewport UI**: Responsive, centered, and polished React interface.

## Tech Stack

-   **Frontend**: React, Vite, Axios
-   **Backend**: FastAPI, Uvicorn, Python 3.10+
-   **AI Logic**: LangGraph, OpenAI GPT-4
-   **Database**: Supabase (PostgreSQL)

## Getting Started

### Prerequisites

-   Node.js & npm
-   Python 3.10+
-   Supabase Account
-   OpenAI API Key

### Installation

1.  **Clone the repository**
    ```bash
    git clone https://github.com/yourusername/ai-hospital-receptionist.git
    cd ai-hospital-receptionist
    ```

2.  **Backend Setup**
    ```bash
    cd backend
    python -m venv .venv
    source .venv/bin/activate  # Windows: .\.venv\Scripts\Activate.ps1
    pip install -r requirements.txt
    ```

3.  **Environment Configuration**
    Create a `.env` file in `backend/` with your secrets (see `.env.example`).
    ```env
    OPENAI_API_KEY=sk-...
    SUPABASE_URL=https://...
    SUPABASE_SERVICE_ROLE_KEY=ey...
    WEBHOOK_URL=https://...
    ```

4.  **Database Setup**
    Run the SQL script `database_setup.sql` in your Supabase SQL Editor to create the necessary tables.

5.  **Run the Application**
    *Terminal 1 (Backend):*
    ```bash
    uvicorn main:app --reload
    ```
    *Terminal 2 (Frontend):*
    ```bash
    cd frontend
    npm install
    npm run dev
    ```

## Security

-   **No Hardcoded Secrets**: All keys are managed via environment variables.
-   **Input Validation**: Strict Pydantic models for all data entry.
-   **RLS**: Database policies configured for secure access.

## License

MIT
