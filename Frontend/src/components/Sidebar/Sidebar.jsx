import React, { useState } from 'react';
import './Sidebar.css';

function Sidebar({ 
  chatSessions, 
  currentSessionId, 
  onSelectSession, 
  onNewChat,
  onDeleteSession,
  isOpen,
  onToggle 
}) {
  const [hoveredId, setHoveredId] = useState(null);

  const formatDate = (date) => {
    const now = new Date();
    const chatDate = new Date(date);
    const diffTime = Math.abs(now - chatDate);
    const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24));

    if (diffDays === 0) {
      return 'Today';
    } else if (diffDays === 1) {
      return 'Yesterday';
    } else if (diffDays < 7) {
      return `${diffDays} days ago`;
    } else {
      return chatDate.toLocaleDateString();
    }
  };

  const getSessionTitle = (session) => {
    // Get first user message or use default
    const firstUserMessage = session.messages.find(m => m.role === 'user');
    if (firstUserMessage) {
      return firstUserMessage.content.slice(0, 50) + 
             (firstUserMessage.content.length > 50 ? '...' : '');
    }
    return 'New Chat';
  };

  return (
    <>
      {/* Mobile Toggle Button */}
      <button className="sidebar-toggle" onClick={onToggle}>
        {isOpen ? '✕' : '☰'}
      </button>

      {/* Sidebar */}
      <div className={`sidebar ${isOpen ? 'open' : ''}`}>
        {/* New Chat Button */}
        <button className="new-chat-button" onClick={onNewChat}>
          <span className="button-icon">➕</span>
          New Chat
        </button>

        {/* Chat History */}
        <div className="chat-history">
          <div className="history-label">Recent Chats</div>
          
          {chatSessions.length === 0 ? (
            <div className="empty-history">
              No chat history yet
            </div>
          ) : (
            <div className="chat-list">
              {chatSessions.map((session) => (
                <div
                  key={session.id}
                  className={`chat-item ${currentSessionId === session.id ? 'active' : ''}`}
                  onClick={() => onSelectSession(session.id)}
                  onMouseEnter={() => setHoveredId(session.id)}
                  onMouseLeave={() => setHoveredId(null)}
                >
                  <div className="chat-item-content">
                    <div className="chat-title">
                      💬 {getSessionTitle(session)}
                    </div>
                    <div className="chat-date">
                      {formatDate(session.createdAt)}
                    </div>
                    <div className="chat-count">
                      {session.messages.filter(m => m.role === 'user').length} messages
                    </div>
                  </div>
                  
                  {hoveredId === session.id && currentSessionId !== session.id && (
                    <button
                      className="delete-button"
                      onClick={(e) => {
                        e.stopPropagation();
                        onDeleteSession(session.id);
                      }}
                    >
                      🗑️
                    </button>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Footer Info */}
        <div className="sidebar-footer">
          <div className="footer-text">
            🏛️ CA Procurement Assistant
          </div>
        </div>
      </div>

      {/* Overlay for mobile */}
      {isOpen && <div className="sidebar-overlay" onClick={onToggle} />}
    </>
  );
}

export default Sidebar;
