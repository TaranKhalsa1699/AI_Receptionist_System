from supabase import create_client, Client
from config import SUPABASE_URL, SUPABASE_KEY
from models import WebhookPayload
import logging

# Initialize Supabase Client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def persist_patient_data(data: WebhookPayload) -> bool:
    """
    Persists validated patient data to Supabase 'patients' table.
    Returns True if successful, False otherwise.
    Uses parameterized queries via the Supabase client.
    """
    try:
        response = supabase.table("patients").insert({
            "name": data.patient_name,
            "age": data.patient_age,
            "query": data.patient_query,
            "ward": data.ward
        }).execute()
        
        # Check if any data was returned (implies success)
        if response.data:
            return True
        return False

    except Exception as e:
        logging.error(f"Database Persistence Error: {e}")
        return False
