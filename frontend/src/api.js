import axios from 'axios';

// Ensure the backend URL is correct. Assuming default localhost:8000 for FastAPI.
// In production, this would come from import.meta.env.VITE_API_URL
const API_URL = 'http://localhost:8000/chat';

export const sendMessage = async (message, sessionId) => {
    try {
        const response = await axios.post(API_URL, {
            message: message,
            session_id: sessionId
        });
        return response.data;
    } catch (error) {
        console.error("API Error:", error);
        throw error;
    }
};
