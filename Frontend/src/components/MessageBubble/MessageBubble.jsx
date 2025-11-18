import React from 'react';
import './MessageBubble.css';

function MessageBubble({ message }) {
  return (
    <div className={`message-wrapper ${message.role}`}>
      <div className={`message-bubble ${message.role} ${message.isError ? 'error' : ''}`}>
        <div className="message-content">
          {message.content}
        </div>
        
        {message.data && message.data.length > 0 && (
          <div className="message-data">
            <strong>📋 Data ({message.data.length} results):</strong>
            <div className="data-items">
              {message.data.slice(0, 3).map((item, i) => (
                <div key={i} className="data-item">
                  {Object.entries(item).slice(0, 4).map(([key, value]) => (
                    <div key={key} className="data-field">
                      <strong>{key}:</strong> {String(value).slice(0, 50)}
                    </div>
                  ))}
                </div>
              ))}
            </div>
          </div>
        )}

        <div className="message-timestamp">
          {message.timestamp?.toLocaleTimeString() || ''}
        </div>
      </div>
    </div>
  );
}

export default MessageBubble;
