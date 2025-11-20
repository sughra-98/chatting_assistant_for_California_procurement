{/* Body.jsx 
  this component renders the main chat body, displaying messages
  and a typing indicator when loading.

*/}

import React, { useRef, useEffect } from "react";
import MessageBubble from "../MessageBubble/MessageBubble";
import TypingIndicator from "../TypingIndicator/TypingIndicator";
import "./Body.css";

function Body({ messages, loading }) {
  const messagesEndRef = useRef(null); // Ref to scroll to bottom

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" }); // Smooth scroll
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, loading]);

  return (
    <div className="messages-container">
      {messages.map((message, index) => (
        <MessageBubble key={index} message={message} />
      ))}

      {loading && <TypingIndicator />}

      <div ref={messagesEndRef} />
    </div>
  );
}

export default Body;
