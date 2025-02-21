-- Create the 'users' table to store user information
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,  -- Automatically generated unique ID
    user_name VARCHAR(255) NOT NULL, -- User's name
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Timestamp of user creation
);

-- Create the 'goals' table to store user goals
CREATE TABLE goals (
    goal_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id) NOT NULL, -- Foreign key referencing users table
    goal_description TEXT NOT NULL, -- Description of the goal
    weightage NUMERIC(3, 2) NOT NULL, -- Weightage of the goal (e.g., 70.00, 30.00)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create the 'feedback' table to store feedback given by the chatbot or user
CREATE TABLE feedback (
    feedback_id SERIAL PRIMARY KEY,
    goal_id INTEGER REFERENCES goals(goal_id) NOT NULL, -- Foreign key referencing goals table
    feedback_text TEXT NOT NULL, -- The feedback given
    feedback_type VARCHAR(50) NOT NULL,  -- Type of feedback (e.g., 'LLM', 'User')
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Optionally, create a 'conversation_history' table to store the conversation
CREATE TABLE conversation_history (
    message_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id) NOT NULL,
    message_text TEXT NOT NULL,
    sender VARCHAR(50) NOT NULL, -- 'user' or 'bot'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Optionally, store user preferences or settings
CREATE TABLE user_preferences (
  preference_id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users(user_id) UNIQUE NOT NULL, -- One set of preferences per user
  # Add preference columns here:
  receive_notifications BOOLEAN DEFAULT TRUE,
  preferred_language VARCHAR(50) DEFAULT 'en',
  # ... other preferences
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);