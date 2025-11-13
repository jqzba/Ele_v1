import React, { useState } from 'react';
import './TodoApp.css';

const TodoApp = () => {
  const [inputValue, setInputValue] = useState('');
  const [todos, setTodos] = useState([]);

  const handleSubmit = (e) => {
    e.preventDefault();
    
    // Basic validation: don't submit if input is empty
    if (inputValue.trim() === '') {
      return;
    }

    // Create new todo object with unique ID and timestamp
    const newTodo = {
      id: Date.now().toString(), // Simple ID generation
      title: inputValue.trim(),
      timestamp: new Date().toISOString()
    };

    // Add todo to the list
    setTodos(prevTodos => [...prevTodos, newTodo]);

    // Clear the input field after submission
    setInputValue('');
  };

  const handleInputChange = (e) => {
    setInputValue(e.target.value);
  };

  const handleRemove = (todoId) => {
    setTodos(prevTodos => prevTodos.filter(todo => todo.id !== todoId));
  };

  return (
    <div className="todo-app">
      <h2>Todo Application</h2>
      
      <form onSubmit={handleSubmit} className="todo-form">
        <div className="form-group">
          <input
            type="text"
            value={inputValue}
            onChange={handleInputChange}
            placeholder="Enter a new todo..."
            className="todo-input"
            autoFocus
          />
          <button 
            type="submit" 
            className="submit-btn"
            disabled={inputValue.trim() === ''}
          >
            Add Todo
          </button>
        </div>
      </form>

      {/* Todo Counter */}
      <div className="todo-counter">
        <p>Total items: {todos.length}</p>
      </div>

      {/* Todo List */}
      <div className="todo-list">
        {todos.length === 0 ? (
          <p className="empty-message">No to-do items yet. Add one above!</p>
        ) : (
          <ul className="todo-items">
            {todos.map(todo => (
              <li key={todo.id} className="todo-item">
                <span className="todo-title">{todo.title}</span>
                <button 
                  onClick={() => handleRemove(todo.id)}
                  className="remove-btn"
                  aria-label={`Remove ${todo.title}`}
                >
                  Remove
                </button>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
};

export default TodoApp;