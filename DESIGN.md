# Simple Study: Design Document

## 1. Overview
Simple Study is a web application aimed at helping students organize their academic life. It features:
- A to-do list for task management
- A study method quiz to personalize study strategies
- Login and Sign-Up functionality for user authentication

This document explains the technical architecture, tools, and design decisions.

---

## 2. System Architecture

### 2.1 Application Flow
1. Frontend: HTML templates render user interfaces (e.g., task manager, quiz)
2. Backend: Flask handles user requests and serves responses
3. Database: SQLite stores user data, tasks, and quiz results

---

### 2.2 Diagram
```
User --> Browser --> Flask App --> SQLite Database
```

---

## 3. Directory Structure

```
Simple-Study/
│
├── app.py               # Main Flask application
├── style.css            # CSS styles for frontend
├── users.db             # SQLite database file
├── templates/           # HTML templates (frontend views)
│   ├── dashbaord.html   # To-Do List page
│   ├── login.html       # Login page
│   ├── edit_task.html   # Page for editing an existing task
│   ├── signup.html      # Signup page
│   ├── quiz.html        # Study method quiz page
│   └── history.html     # Task history page
└── venv/                # Virtual environment (optional)
```

---

## 4. Key Features

### 4.1 To-Do List
- Description: Allows users to create, edit, delete, and mark tasks as completed
- Implementation: 
  - Backend routes handle task creation (`POST`) and fetching tasks (`GET`)
  - Data is stored in a database table (`tasks`)

### 4.2 Study Method Quiz
- Description: A quiz that provides users with personalized study methods based on their answers
- Implementation: 
  - Quiz questions are stored in the database or hardcoded
  - Responses are processed to generate results using predefined logic

### 4.3 Login and Sign-Up
- Description: Provides user authentication with a simple username-password mechanism
- Implementation:
  - Users' credentials are stored securely in the `users.db` file
  - Passwords should ideally be hashed using `bcrypt`

---

## 5. Tools and Technologies

### 5.1 Backend
- Flask: Manages routing, logic, and rendering views
- SQLite: Database for storing persistent data

### 5.2 Frontend
- HTML: Defines structure and content of the pages
- CSS: Enhances design and user experience
- JavaScript: (Optional) Adds interactivity, e.g., dynamic updates for the To-Do List

### 5.3 Libraries (to install)
- Flask (`pip install flask`)
- Werkzeug (built into Flask for request handling)
- Optional: bcrypt (`pip install bcrypt`) for secure password storage

---

## 6. Database Design

### 6.1 Tables
#### Users Table:
| Field         | Type     | Description                   |
|---------------|----------|-------------------------------|
| `id`          | Integer  | Primary Key                  |
| `username`    | Text     | Unique username              |
| `password`    | Text     | Hashed password              |

#### Tasks Table:
| Field         | Type     | Description                   |
|---------------|----------|-------------------------------|
| `id`          | Integer  | Primary Key                  |
| `user_id`     | Integer  | Foreign Key to Users table   |
| `task`        | Text     | Task description             |
| `completed`   | Boolean  | Task completion status       |

---

## 7. API Endpoints

### 7.1 Authentication
- POST `/signup`: Registers a new user
- POST `/login`: Authenticates existing users

### 7.2 To-Do List
- GET `/tasks`: Fetch all tasks for the logged-in user
- POST `/tasks`: Add a new task
- PUT `/tasks/<id>`: Mark a task as completed
- DELETE `/tasks/<id>`: Delete a task

---

## 8. Future Enhancements

- Add password recovery through email
- Enhance security using JWT for session handling

---

## 9. Development Guidelines

1. Coding Standards: Follow PEP 8 for Python.
2. Branching Strategy: Use `feature/<name>` for new features and `fix/<name>` for bug fixes
3. Testing: Add unit tests for routes and database queries
4. Error Handling: Implement error messages for invalid inputs

---

## 10. Appendix

### References
- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLite Tutorial](https://sqlite.org/docs.html)

---