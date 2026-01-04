import React, { useState, useEffect, useRef } from 'react';
import { v4 as uuidv4 } from 'uuid';
import { sendMessage } from './api';
import ChatBubble from './components/ChatBubble';

function App() {
  const [view, setView] = useState('home'); // 'home' | 'chat'
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId, setSessionId] = useState('');
  const [showPopup, setShowPopup] = useState(false);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    // Generate a session ID on mount
    setSessionId(uuidv4());
  }, []);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleNewChat = () => {
    const newSession = uuidv4();
    setSessionId(newSession);
    setMessages([]);
    setInput('');
    setShowPopup(false);
    console.log("New session started:", newSession);
  };

  const handleStartChat = () => {
    setView('chat');
  };

  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMsg = input.trim();
    setInput('');

    // Add user message to UI immediately
    setMessages(prev => [...prev, { text: userMsg, isUser: true }]);
    setIsLoading(true);

    try {
      const data = await sendMessage(userMsg, sessionId);
      setMessages(prev => [...prev, { text: data.reply, isUser: false }]);

      // Trigger popup if registration is complete
      if (data.reply.includes("Registration complete")) {
        setShowPopup(true);
      }
    } catch (error) {
      setMessages(prev => [...prev, { text: "Error: Could not connect to server.", isUser: false }]);
    } finally {
      setIsLoading(false);
    }
  };

  const closePopup = () => {
    setShowPopup(false);
  };

  // --- Styles ---
  const appWrapperStyle = {
    width: '100%',
    height: '100%',
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    fontFamily: "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
  };

  // Welcome Screen Styles
  const welcomeCardStyle = {
    backgroundColor: 'white',
    padding: '40px',
    borderRadius: '20px',
    boxShadow: '0 4px 15px rgba(0,0,0,0.1)',
    textAlign: 'center',
    maxWidth: '500px',
    width: '90%',
  };

  const titleStyle = {
    color: '#2c3e50',
    marginBottom: '10px',
    fontSize: '2.5rem',
    margin: '0 0 10px 0'
  };

  const subtitleStyle = {
    color: '#7f8c8d',
    marginBottom: '30px',
    fontSize: '1.1rem'
  };

  const startButtonStyle = {
    backgroundColor: '#007bff',
    color: 'white',
    border: 'none',
    padding: '15px 40px',
    fontSize: '1.2rem',
    borderRadius: '50px',
    cursor: 'pointer',
    transition: 'background-color 0.3s',
    boxShadow: '0 4px 6px rgba(0,123,255,0.3)',
    marginTop: '20px'
  };

  // Chat Screen Styles
  const chatContainerStyle = {
    backgroundColor: 'white',
    borderRadius: '20px',
    boxShadow: '0 10px 25px rgba(0,0,0,0.1)',
    width: '95%',
    maxWidth: '800px',
    height: '80vh',
    display: 'flex',
    flexDirection: 'column',
    overflow: 'hidden',
    margin: '0 auto'
  };

  const chatHeaderStyle = {
    backgroundColor: '#007bff',
    color: 'white',
    padding: '20px',
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center'
  };

  const chatBodyStyle = {
    flex: 1,
    padding: '20px',
    overflowY: 'auto',
    backgroundColor: '#fff'
  };

  const inputAreaStyle = {
    padding: '20px',
    backgroundColor: '#f8f9fa',
    borderTop: '1px solid #e9ecef',
    display: 'flex',
    gap: '10px'
  };

  const inputStyle = {
    flex: 1,
    padding: '15px',
    borderRadius: '30px',
    border: '1px solid #ced4da',
    fontSize: '1rem',
    outline: 'none'
  };

  const sendButtonStyle = {
    backgroundColor: '#007bff',
    color: 'white',
    border: 'none',
    borderRadius: '50%',
    width: '50px',
    height: '50px',
    cursor: 'pointer',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    fontSize: '1.2rem'
  };

  const smallButtonStyle = {
    backgroundColor: 'rgba(255,255,255,0.2)',
    color: 'white',
    border: 'none',
    padding: '8px 15px',
    borderRadius: '15px',
    cursor: 'pointer',
    fontSize: '0.9rem'
  };

  // Popup Styles
  const popupOverlayStyle = {
    position: 'fixed',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    backgroundColor: 'rgba(0,0,0,0.5)',
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    zIndex: 1000
  };

  const popupContentStyle = {
    backgroundColor: 'white',
    padding: '30px',
    borderRadius: '15px',
    textAlign: 'center',
    boxShadow: '0 5px 30px rgba(0,0,0,0.3)',
    maxWidth: '400px',
    width: '90%'
  };

  const checkmarkStyle = {
    fontSize: '3rem',
    color: '#2ecc71',
    marginBottom: '20px',
    display: 'block'
  };

  // --- Render ---

  if (view === 'home') {
    return (
      <div style={appWrapperStyle}>
        <div style={welcomeCardStyle}>
          <h1 style={titleStyle}>Hospital AI</h1>
          <p style={subtitleStyle}>Intelligent Reception & Triage System</p>
          <div style={{ fontSize: '4rem', margin: '30px 0' }}>
            🏥 🚑 🩺
          </div>
          <button
            style={startButtonStyle}
            onClick={handleStartChat}
          >
            Query Report / Start
          </button>
          <p style={{ marginTop: '30px', fontSize: '0.8rem', color: '#bdc3c7' }}>
            Secure • Private • Instant
          </p>
        </div>
      </div>
    );
  }

  return (
    <div style={appWrapperStyle}>
      <div style={chatContainerStyle}>
        <div style={chatHeaderStyle}>
          <h2 style={{ margin: 0, fontSize: '1.3rem' }}>Reception Desk</h2>
          <button onClick={handleNewChat} style={smallButtonStyle}>
            New Session
          </button>
        </div>

        <div style={chatBodyStyle}>
          {messages.length === 0 && (
            <div style={{ textAlign: 'center', color: '#95a5a6', marginTop: '50px' }}>
              <p>Welcome to the reception.</p>
              <p>Please describe your symptoms or reason for visit.</p>
            </div>
          )}
          {messages.map((msg, index) => (
            <ChatBubble key={index} message={msg.text} isUser={msg.isUser} />
          ))}
          {isLoading && (
            <div style={{ alignSelf: 'flex-start', color: '#95a5a6', fontStyle: 'italic', margin: '10px' }}>
              Typing...
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        <form onSubmit={handleSend} style={inputAreaStyle}>
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type your message here..."
            style={inputStyle}
            disabled={isLoading}
          />
          <button type="submit" style={sendButtonStyle} disabled={isLoading}>
            ➤
          </button>
        </form>
      </div>

      {showPopup && (
        <div style={popupOverlayStyle}>
          <div style={popupContentStyle}>
            <span style={checkmarkStyle}>✓</span>
            <h2 style={{ color: '#2c3e50', margin: '0 0 10px 0' }}>Query Noted</h2>
            <p style={{ color: '#7f8c8d', marginBottom: '20px' }}>
              Registration is complete. Your details have been sent to the desk.
            </p>
            <button
              onClick={closePopup}
              style={{ ...startButtonStyle, marginTop: '0', padding: '10px 30px', fontSize: '1rem' }}
            >
              Close
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
