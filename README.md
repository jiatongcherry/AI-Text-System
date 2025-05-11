# AI-Powered Text Analysis System

This is a full-stack AI text analysis system for keyword extraction, text summarization, and topic classification built with React.JS, Python Flask.


## Features
- **Keyword Extraction**: Identifies and extracts the most significant keywords or phrases from a given text
- **Text Summarization**: Generates a concise summary of longer text, capturing the main ideas in a condensed form.
- **Topic Classification**: Categorizes text into predefined topics (Sports, Politics, Technology, Entertainment)

## Technology Used

- **Frontend**: React.JS
- **Backend**: Python, Flask
- **AI model**: DeepSeek
- **Candidate AI model for Performance Comparison**: BART, Qwen
- **HTTP Requests**: Axios
- **API Testing**: Postman

## Clone the Repository
1. Navigate to directory where stores the project:

   ```bash
   cd /path/to/your/directory
2. Clone the repository using Git:

   ```bash
    git clone https://github.com/jiatongcherry/AI-Text-System.git
3. Navigate to directory where stores the project:

   ```bash
    cd AI-Text-System

## Setup
### Backend
1. Navigate to backend:

    ```bash
   cd backend
2. Create and activate a virtual environment:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: .\venv\Scripts\activate
3. Install dependencies:
    ```bash
   pip install -r requirements.txt
4. Set up environment variables in backend/.env:

    ```bash
   DEEPSEEK_API_KEY=your-deepseek-api-key
   DEEPSEEK_API_URL=https://api.deepseek.com/v1/models
5. Start the Flask backend server:
    ```bash
   python llm_api.py

### Frontend
1. Navigate to the frontend directory:
    ```bash
   cd frontend
2. Install dependencies:
    ```bash
   npm install
3. Start the frontend server:
    ```bash
   npm run dev

## Usage
- Access the web interface at `http://localhost:5173`.
- Access the backend at `http://localhost:8000`.
- Enter text and use the buttons to extract keywords, summarize, or classify topics.
