# Flask Application with PDF RAG LLM CHAT

This project is a Flask-based web application that allows users to register, log in, and interact with a question-answering system. It includes various functionalities such as file uploads, question logging, and feedback management. The application uses DuckDB as the database for storing user information, questions, answers, and feedback.

## Features

- User registration and authentication
- Question logging with associated answers
- File upload and management
- Feedback on answers
- API endpoints for interacting with the application

## Setup and Installation

### Prerequisites

- Python 3.11.9
- chromadb==0.5.0
- duckdb==0.10.3
- fastembed==0.2.7
- Flask==3.0.3
- Flask-HTTPAuth==4.8.0
- Flask-Login==0.6.3
- Flask-RESTful==0.3.10
- langchain==0.2.1
- langchain-community==0.2.1
- langchain-core==0.2.1
- langchain-text-splitters==0.2.0
- PyPDF2==3.0.1

### Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/khoo2002/PDF-RAG-CHAT
    cd PDF-RAG-CHAT
    ```

2. Create and activate a virtual environment:
    ```sh
    python3 -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

4. Run the application:
    ```sh
    python app.py
    ```

The application will be available at `http://127.0.0.1:8000`.

## Directory Structure

flask-app/
│
├── app.py # Main application file
├── templates/ # HTML templates
│ ├── index.html
│ ├── login.html
│ ├── register.html
│ ├── admin.html
│ ├── user.html
│ └── question.html
└── uploaded/ # Directory for uploaded files

## API Endpoints

### Authentication

- `GET /login`: Render the login page
- `POST /login`: Log in the user
- `GET /register`: Render the registration page
- `POST /register`: Register a new user
- `GET /logout`: Log out the user

### File Management

- `POST /api/admin/file/upload`: Upload a file
- `GET /api/admin/file/get`: Get a list of uploaded files
- `GET /api/admin/file/get/<file>`: Download a specific file
- `POST /api/admin/file/delete/<file>`: Delete a specific file
- `GET /api/admin/file/ingest`: Ingest uploaded files

### Questions and Answers

- `GET /api/admin/questions/<int:page>`: Get a paginated list of questions
- `GET /api/admin/answers/<int:questionId>`: Get answers for a specific question

### User Interaction

- `POST /api/user/chat/`: Submit a question and get an answer
- `POST /api/user/feedback/`: Submit feedback for an answer
- `GET /api/user/feedback/<int:answer_id>`: Get feedback for a specific answer

### Utility

- `GET /get_my_ip`: Get the IP address of the requester

## Usage

1. **Register a new user**: Visit `/register` and create a new account.
2. **Log in**: Visit `/login` and log in with your credentials.
3. **Ask a question**: Use the `/api/user/chat/` endpoint to submit a question and receive an answer.
4. **Upload files**: Use the `/api/admin/file/upload` endpoint to upload PDF files.
5. **Provide feedback**: Use the `/api/user/feedback/` endpoint to submit feedback on answers.

## Database Schema

The application uses DuckDB to store data in the following tables:

- `users`: Stores user information.
- `questions`: Stores logged questions.
- `answers`: Stores answers to questions.
- `feedback`: Stores feedback on answers.
- `pdf_files`: Stores uploaded file information.
- `api_access`: Logs API access.
- `logs`: Logs requests and responses.

## Notes

- Ensure the `uploaded` directory exists or is created at runtime for file uploads.
- Customize IP restrictions in the `limit_access` function as needed.
- Admin and user roles are predefined, with role-based access control in place.

## License

This project is licensed under the MIT License.
