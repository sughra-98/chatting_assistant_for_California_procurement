import React from 'react';
import './ExampleQuestions.css';

function ExampleQuestions({ questions, onQuestionClick }) {
  return (
    <div className="examples-container">
      <div className="examples-label">💡 Try these examples:</div>
      <div className="examples-buttons">
        {questions.map((question, idx) => (
          <button
            key={idx}
            onClick={() => onQuestionClick(question)}
            className="example-button"
          >
            {question}
          </button>
        ))}
      </div>
    </div>
  );
}

export default ExampleQuestions;
