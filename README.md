# AI Hospital Receptionist System

An intelligent, secure, and deterministic chatbot for hospital patient intake. Built with React, FastAPI, LangGraph, and Supabase.



## Features

-   **Deterministic Triage**: Automatically routes patients to **General**, **Emergency**, or **Mental Health** wards based on symptoms.
-   **Strict Data Collection**: Enforces collection of Name, Age, and Query to ensure complete records.
-   **Secure Persistence**: Stores patient data in **Supabase (PostgreSQL)** using Row Level Security (RLS) bypass via Service Role.
-   **Webhook Integration**: Triggers external workflows (e.g., Relay.app, Zapier) upon successful registration.
-   **Full-Viewport UI**: Responsive, centered, and polished React interface.

## Security

-   **No Hardcoded Secrets**: All keys are managed via environment variables.
-   **Input Validation**: Strict Pydantic models for all data entry.
-   **RLS**: Database policies configured for secure access.

## Live Deployment

The project is deployed with a separate backend and frontend.

**Backend (FastAPI – Render)**
👉 https://ai-receptionist-system.onrender.com/

Opening this link wakes up the API server. You should see a basic response or API info page.

**Frontend (Vite + React – Vercel)**
👉 https://ai-receptionist-system.vercel.app/

After the backend is awake, the chat works instantly.

**Recommended Usage Flow**

1. Open the backend link once to wake the server.
2. Open the frontend link.
3. Start chatting with the AI Receptionist.

## License

MIT

## Tech Stack

-   **Frontend**: React, Vite, Axios
-   **Backend**: FastAPI, Uvicorn, Python 3.10+
-   **AI Logic**: LangGraph, OpenAI GPT-4
-   **Database**: Supabase (PostgreSQL)

## Project Structure

```
AI_Receptionist_System/
├── backend/            # FastAPI server
│   ├── main.py        # App entry point
│   ├── graph.py       # LangGraph logic
│   └── requirements.txt
├── frontend/           # React application
│   ├── src/
│   │   ├── api.js     # API integration
│   │   └── App.jsx    # Main UI
│   └── package.json
└── README.md
```

## Getting Started

### Prerequisites

-   Node.js & npm
-   Python 3.10+
-   Supabase Account
-   OpenAI API Key

### Local Installation

1.  **Clone the repository**
    ```bash
    git clone https://github.com/TaranKhalsa1699/AI_Receptionist_System.git
    cd AI_Receptionist_System
    ```

2.  **Backend Setup**
    ```bash
    cd backend
    python -m venv .venv
    # Windows
    .\.venv\Scripts\Activate.ps1
    # Mac/Linux
    source .venv/bin/activate
    
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

4.  **Frontend Setup**
    ```bash
    cd ../frontend
    npm install
    ```

5.  **Run Locally**
    *Terminal 1 (Backend):*
    ```bash
    uvicorn main:app --reload
    ```
    *Terminal 2 (Frontend):*
    ```bash
    npm run dev
    ```

## Deployment

### Backend (Render/Railway)
1.  Deploy the `backend` folder as a Python Web Service.
2.  Build Command: `pip install -r requirements.txt`
3.  Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4.  Add Environment Variables from your local `.env`.

### Frontend (Vercel)
1.  Import the repository.
2.  Set Root Directory to `frontend`.
3.  Add Environment Variable:
    - `VITE_API_URL`: Your deployed backend URL (e.g., `https://your-app.onrender.com/chat`)

## Troubleshooting

-   **"Could not connect to server"**:
    -   If using Render free tier, the backend may be sleeping. Open the backend URL in your browser (e.g., `/docs`) to wake it up.
    -   Ensure `VITE_API_URL` is set correctly in Vercel settings.

## License

MIT
