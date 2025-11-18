import React from 'react';
import './Header.css';

function Header({ stats }) {
  return (
    <header className="header">
      <h1 className="header-title">
        🏛️ California Procurement Assistant
      </h1>
      {stats && (
        <div className="header-stats">
          <span className="stat-item">
            📊 {stats.total_records?.toLocaleString() || 0} records
          </span>
          <span className="stat-item">
            🏢 {stats.departments || 0} departments
          </span>
          <span className="stat-item">
            🏪 {stats.suppliers || 0} suppliers
          </span>
        </div>
      )}
    </header>
  );
}

export default Header;
