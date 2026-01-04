import React from 'react';

const ChatBubble = ({ message, isUser }) => {
    const bubbleStyle = {
        maxWidth: '80%',
        padding: '10px 15px',
        borderRadius: '15px',
        margin: '5px 0',
        alignSelf: isUser ? 'flex-end' : 'flex-start',
        backgroundColor: isUser ? '#007bff' : '#e9ecef',
        color: isUser ? 'white' : 'black',
        wordWrap: 'break-word'
    };

    const containerStyle = {
        display: 'flex',
        flexDirection: 'column',
        width: '100%'
    };

    return (
        <div style={containerStyle}>
            <div style={bubbleStyle}>
                {message}
            </div>
        </div>
    );
};

export default ChatBubble;
