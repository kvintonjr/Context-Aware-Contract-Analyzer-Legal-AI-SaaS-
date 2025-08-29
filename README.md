# Context-Aware-Contract-Analyzer-Legal-AI-SaaS

This is an AI-powered SaaS application that analyzes legal contracts. It summarizes the contract, identifies potential risks, and provides a "Risk Score".

## How to Run

This project is divided into a backend service and a frontend application.

### Prerequisites

- Python 3.x
- pip

### Backend Setup

1.  **Navigate to the backend directory:**
    ```bash
    cd backend
    ```

2.  **Create a virtual environment:**
    ```bash
    python -m venv venv
    ```

3.  **Activate the virtual environment:**
    -   On Windows:
        ```bash
        .\venv\Scripts\activate
        ```
    -   On macOS and Linux:
        ```bash
        source venv/bin/activate
        ```

4.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

5.  **Create an environment file:**
    Create a file named `.env` in the `backend` directory. This file will hold your OpenAI API key.
    ```
    OPENAI_API_KEY=your_openai_api_key_here
    ```
    Replace `your_openai_api_key_here` with your actual OpenAI API key.

6.  **Run the Flask server:**
    ```bash
    python app.py
    ```
    The backend server will start on `http://1227.0.0.1:5000`.

### Frontend Setup

1.  **Open the `index.html` file:**
    Navigate to the `frontend` directory and open the `index.html` file in your web browser.

2.  **Use the application:**
    -   Paste the contract text into the text area.
    -   Click the "Analyze" button.
    -   The analysis results will be displayed below the form.
