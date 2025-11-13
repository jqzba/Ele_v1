import React, { useState, useEffect } from 'react';
import './TodoApp.css';

const API_BASE_URL = 'http://localhost:7071/api/todo';

const TodoApp = () => {
  const [inputValue, setInputValue] = useState('');
  const [todos, setTodos] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Fetch todos from backend on component mount
  useEffect(() => {
    fetchTodos();
  }, []);

  // Helper function to parse error responses
  const parseError = async (response, defaultMessage) => {
    try {
      const errorData = await response.json();
      return errorData.error || errorData.message || defaultMessage;
    } catch {
      return defaultMessage;
    }
  };

  const fetchTodos = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch(API_BASE_URL);
      
      if (!response.ok) {
        const errorMessage = await parseError(response, 'Failed to fetch todos');
        throw new Error(errorMessage);
      }
      
      const data = await response.json();
      setTodos(data);
      console.log(`✅ Successfully loaded ${data.length} todos`);
    } catch (err) {
      console.error('❌ Error fetching todos:', err);
      
      // Network error vs server error
      if (err.message.includes('Failed to fetch') || err.name === 'TypeError') {
        setError('Cannot connect to backend. Make sure the Azure Functions server is running on http://localhost:7071');
      } else {
        setError(err.message || 'Failed to load todos. Please try again.');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Basic validation: don't submit if input is empty
    if (inputValue.trim() === '') {
      setError('Please enter a todo title');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const response = await fetch(API_BASE_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ title: inputValue.trim() }),
      });

      if (!response.ok) {
        const errorMessage = await parseError(response, 'Failed to create todo');
        throw new Error(errorMessage);
      }

      const newTodo = await response.json();
      console.log('✅ Successfully created todo:', newTodo);

      // Clear the input field after successful submission
      setInputValue('');

      // Refresh the todo list
      await fetchTodos();
    } catch (err) {
      console.error('❌ Error creating todo:', err);
      
      if (err.message.includes('Failed to fetch') || err.name === 'TypeError') {
        setError('Cannot connect to backend. Please check your connection.');
      } else {
        setError(err.message || 'Failed to create todo. Please try again.');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (e) => {
    setInputValue(e.target.value);
    // Clear error when user starts typing
    if (error) {
      setError(null);
    }
  };

  const handleRemove = async (todo) => {
    setLoading(true);
    setError(null);

    try {
      const response = await fetch(
        `${API_BASE_URL}/${todo.partitionKey}/${todo.rowKey}`,
        {
          method: 'DELETE',
        }
      );

      if (!response.ok) {
        const errorMessage = await parseError(response, 'Failed to delete todo');
        throw new Error(errorMessage);
      }

      console.log('✅ Successfully deleted todo:', todo.title);

      // Refresh the todo list
      await fetchTodos();
    } catch (err) {
      console.error('❌ Error deleting todo:', err);
      
      if (err.message.includes('Failed to fetch') || err.name === 'TypeError') {
        setError('Cannot connect to backend. Please check your connection.');
      } else if (err.message.includes('not found')) {
        setError('Todo item not found. It may have been already deleted.');
      } else {
        setError(err.message || 'Failed to delete todo. Please try again.');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="todo-app">
      <div className="todo-app-container">
        <h2>Todo Application</h2>
        
        {error && (
          <div className="error-message">
            {error}
          </div>
        )}
        
        <form onSubmit={handleSubmit} className="todo-form">
          <div className="form-group">
            <input
              type="text"
              value={inputValue}
              onChange={handleInputChange}
              placeholder="Enter a new todo..."
              className="todo-input"
              autoFocus
              disabled={loading}
            />
            <button 
              type="submit" 
              className="submit-btn"
              disabled={inputValue.trim() === '' || loading}
            >
              {loading ? 'Adding...' : 'Add Todo'}
            </button>
          </div>
        </form>

        {/* Todo Counter */}
        <div className="todo-counter">
          <p>Total items: {todos.length}</p>
        </div>

        {/* Todo List */}
        <div className="todo-list">
          {loading && todos.length === 0 ? (
            <p className="loading-message">Loading todos...</p>
          ) : todos.length === 0 ? (
            <p className="empty-message">No to-do items yet. Add one above!</p>
          ) : (
            <ul className="todo-items">
              {todos.map(todo => (
                <li key={todo.id} className="todo-item">
                  <span className="todo-title">{todo.title}</span>
                  <button 
                    onClick={() => handleRemove(todo)}
                    className="remove-btn"
                    aria-label={`Remove ${todo.title}`}
                    disabled={loading}
                  >
                    Remove
                  </button>
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>
    </div>
  );
};

export default TodoApp;