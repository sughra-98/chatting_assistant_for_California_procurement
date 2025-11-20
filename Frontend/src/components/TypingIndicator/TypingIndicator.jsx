{/* TypingIndicator.jsx
  this component renders a typing indicator for the assistant
  when it is generating a response.
  */}
import React from 'react';
import './TypingIndicator.css';

function TypingIndicator() {
  return (
    <div className="message-wrapper assistant">
      <div className="message-bubble assistant">
        <div className="typing-indicator">
          <span></span>
          <span></span>
          <span></span>
        </div>
      </div>
    </div>
  );
}

export default TypingIndicator;
