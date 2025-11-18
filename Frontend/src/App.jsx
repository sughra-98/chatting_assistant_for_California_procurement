import React, { useState, useEffect } from 'react';
import Sidebar from './components/Sidebar/Sidebar';
import Header from './components/Header/Header';
import MessagesContainer from './components/Body/Body';
import ExampleQuestions from './components/ExampleQuestions/ExampleQuestions';
import InputArea from './components/InputArea/InputArea';
import api from './services/api';
import './App.css';
import Body from './components/Body/Body';

function App() {
  const [chatSessions, setChatSessions] = useState([]);
  const [currentSessionId, setCurrentSessionId] = useState(null);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [stats, setStats] = useState(null);
  const [sidebarOpen, setSidebarOpen] = useState(false);

  const exampleQuestions = [
    "How many purchases in 2014?",
    "Top 5 departments by spending",
    "Show LPA contracts",
    "IT purchases over $10,000"
  ];

  // Initialize with first chat session
  useEffect(() => {
    // Load sessions from localStorage
    const savedSessions = localStorage.getItem('chatSessions');
    if (savedSessions) {
      const sessions = JSON.parse(savedSessions);
      setChatSessions(sessions);
      if (sessions.length > 0) {
        setCurrentSessionId(sessions[0].id);
      } else {
        createNewChat();
      }
    } else {
      createNewChat();
    }

    fetchStats();
  }, []);

  // Save sessions to localStorage whenever they change
  useEffect(() => {
    if (chatSessions.length > 0) {
      localStorage.setItem('chatSessions', JSON.stringify(chatSessions));
    }
  }, [chatSessions]);

  const fetchStats = async () => {
    try {
      const data = await api.getStats();
      setStats(data);
    } catch (err) {
      console.error('Failed to fetch stats');
    }
  };

  const createNewChat = () => {
    const newSession = {
      id: Date.now().toString(),
      createdAt: new Date().toISOString(),
      messages: [
        {
          role: 'assistant',
          content: 'Hello! I\'m your California Procurement Assistant. Ask me anything about 346,000+ purchase records!',
          timestamp: new Date()
        }
      ]
    };

    setChatSessions(prev => [newSession, ...prev]);
    setCurrentSessionId(newSession.id);
    setSidebarOpen(false); // Close sidebar on mobile after creating new chat
  };

  const selectSession = (sessionId) => {
    setCurrentSessionId(sessionId);
    setSidebarOpen(false); // Close sidebar on mobile after selecting
  };

  const deleteSession = (sessionId) => {
    setChatSessions(prev => {
      const filtered = prev.filter(s => s.id !== sessionId);
      
      // If we deleted the current session, switch to another one
      if (sessionId === currentSessionId) {
        if (filtered.length > 0) {
          setCurrentSessionId(filtered[0].id);
        } else {
          // No sessions left, create a new one
          createNewChat();
        }
      }
      
      return filtered;
    });
  };

  const getCurrentSession = () => {
    return chatSessions.find(s => s.id === currentSessionId);
  };

  const updateCurrentSession = (updater) => {
    setChatSessions(prev => 
      prev.map(session => 
        session.id === currentSessionId 
          ? { ...session, ...updater(session) }
          : session
      )
    );
  };

  const handleSendMessage = async () => {
    if (!input.trim() || loading) return;

    const userMessage = {
      role: 'user',
      content: input,
      timestamp: new Date()
    };

    // Add user message to current session
    updateCurrentSession(session => ({
      messages: [...session.messages, userMessage]
    }));

    setInput('');
    setLoading(true);

    try {
      const response = await api.sendQuery(input);
      
      const assistantMessage = {
        role: 'assistant',
        content: response.answer,
        data: response.data,
        query: response.query_used,
        timestamp: new Date()
      };

      // Add assistant message to current session
      updateCurrentSession(session => ({
        messages: [...session.messages, assistantMessage]
      }));
    } catch (err) {
      const errorMessage = {
        role: 'assistant',
        content: `Sorry, I encountered an error: ${err.message || 'Failed to get answer'}`,
        timestamp: new Date(),
        isError: true
      };
      
      updateCurrentSession(session => ({
        messages: [...session.messages, errorMessage]
      }));
    } finally {
      setLoading(false);
    }
  };

  const handleExampleClick = (question) => {
    setInput(question);
  };

  const currentSession = getCurrentSession();
  const currentMessages = currentSession?.messages || [];
  const showExamples = currentMessages.length === 1;

  return (
    <div className="app-container">
      <Sidebar
        chatSessions={chatSessions}
        currentSessionId={currentSessionId}
        onSelectSession={selectSession}
        onNewChat={createNewChat}
        onDeleteSession={deleteSession}
        isOpen={sidebarOpen}
        onToggle={() => setSidebarOpen(!sidebarOpen)}
      />
      
      <div className="main-content">
        <Header stats={stats} />
        
        <Body 
          messages={currentMessages} 
          loading={loading} 
        />
        
        {showExamples && (
          <ExampleQuestions 
            questions={exampleQuestions}
            onQuestionClick={handleExampleClick}
          />
        )}
        
        <InputArea 
          input={input}
          setInput={setInput}
          onSubmit={handleSendMessage}
          loading={loading}
        />
      </div>
    </div>
  );
}

export default App;
