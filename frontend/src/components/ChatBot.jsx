import React, { useState } from 'react';
import axios from "axios"

const ChatBot = () => {
  const [messages, setMessages] = useState([]);
  const [userMessage, setUserMessage] = useState('');

  const handleSendMessage = async () => {
    if (!userMessage) return;

    const newMessage = {
      sender: 'user',
      text: userMessage,
    };

    setMessages([...messages, newMessage]);
    setUserMessage('');
    console.log('user message', userMessage)

    try {
        console.log('inside try, making an api call')
        const response = await axios.post('http://127.0.0.1:8000/v1/get_sla_qna_response/', {
            question: userMessage,
        });
  
        const botResponse = {
          sender: 'bot',
          text: response.data || 'I didn\'t understand that.',
        };

        setMessages((prevMessages) => [...prevMessages, botResponse]);
      } catch (error) {
        console.error(error);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <div className="w-full h-full bg-gray-900 text-white flex flex-col justify-between p-4">
      <h2 className="text-xl font-semibold">More Queries? Ask me!</h2>

      <div className="flex-1 overflow-auto mt-4 mb-3 p-3 border border-gray-700 rounded-md bg-gray-800">
        {messages.map((message, index) => (
          <div key={index} className={`mb-4 ${message.sender === 'user' ? 'text-right' : ''}`}>
            <div className={`inline-block p-2 rounded-md ${message.sender === 'user' ? 'bg-blue-500' : 'bg-gray-600'}`} >
              {message.text}
            </div>
          </div>
        ))}
      </div>

      <div className="flex items-center">
        <input
          type="text"
          value={userMessage}
          onChange={(e) => setUserMessage(e.target.value)}
          onKeyDown={handleKeyDown}
          className="flex-1 px-3 py-2 rounded-md border border-gray-700 bg-gray-900 text-white focus:outline-none"
          placeholder="Type a message..."
        />
        <button
          onClick={handleSendMessage}
          className="ml-2 bg-blue-500 px-3 py-2 rounded-md hover:bg-blue-700 transition duration-200"
        >
          Send
        </button>
      </div>
    </div>
  );
};

export default ChatBot;
