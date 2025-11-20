import React from 'react';
import './InputArea.css';

function InputArea({ input, setInput, onSubmit, loading }) {
  // Handle form submission
  const handleSubmit = (e) => {
    e.preventDefault();
    if (input.trim() && !loading) {
      onSubmit();
    }
  };

  return (
    <div className="input-container">
      <form onSubmit={handleSubmit} className="input-form">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask about procurement data..."
          disabled={loading}
          className="message-input"
        />
        <button
          type="submit"
          disabled={!input.trim() || loading}
          className="send-button"
        >
          {loading ? 'Sending...' : 'Send'}
        </button>
      </form>
    </div>
  );
}

export default InputArea;
