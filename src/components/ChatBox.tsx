import React, { useState, useEffect } from 'react';

interface Message {
    id: number;
    text: string;
    sender: 'user' | 'other';
}

const ChatBox: React.FC = () => {
    const [messages, setMessages] = useState<Message[]>([]);
    const [input, setInput] = useState('');
    const [isHidden, setIsHidden] = useState(false); // Toggle for hidden mode

    const sendMessage = () => {
        if (input.trim()) {
            const newMessage: Message = {
                id: Date.now(),
                text: input,
                sender: 'user',
            };
            setMessages([...messages, newMessage]);
            setInput('');
            // Simulate response (replace with real logic)
            setTimeout(() => {
                const response: Message = {
                    id: Date.now() + 1,
                    text: 'Response from other side',
                    sender: 'other',
                };
                setMessages(prev => [...prev, response]);
            }, 1000);
        }
    };

    const toggleHidden = () => {
        setIsHidden(!isHidden);
    };

    return (
        <div style={{ display: isHidden ? 'none' : 'block', border: '1px solid #ccc', padding: '10px' }}>
            <button onClick={toggleHidden}>Toggle Hidden</button>
            <div style={{ height: '200px', overflowY: 'scroll', border: '1px solid #eee' }}>
                {messages.map(msg => (
                    <div key={msg.id} style={{ textAlign: msg.sender === 'user' ? 'right' : 'left' }}>
                        {msg.text}
                    </div>
                ))}
            </div>
            <input
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
            />
            <button onClick={sendMessage}>Send</button>
        </div>
    );
};

export default ChatBox;