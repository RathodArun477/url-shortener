# 🔗 URL Shortener

A lightweight, secure, and modern URL shortener built with **Python (Flask)**, **SQLite**, and **Vanilla JavaScript** styled with **Tailwind CSS**.

---

## ✨ Features

- **Cryptographically Secure Short Codes**: Uses Python's `secrets` module instead of pseudo-random generators to generate 6-character unique codes.
- **Collision Handling**: Database-enforced uniqueness backed by an automatic retry mechanism.
- **Smart URL Normalization**: Automatically prepends `https://` if omitted and validates protocols (`http` / `https`).
- **Real-Time Click Analytics**: Tracks total click counts per shortened link, incremented atomically upon redirect.
- **Modern Responsive Web UI**: Clean interface styled with Tailwind CSS via CDN featuring:
  - One-click **Copy to Clipboard** with instant visual feedback.
  - Quick **Open Link** external shortcut.
  - Live **Click Counter** refresh.
- **RESTful API**: Supports both programmatic API access and browser usage with proper HTTP status codes (`201`, `302`, `400`, `404`, `500`).
- **Automated Test Suite**: Tested end-to-end using `pytest`.

---

## 📁 Project Structure

```text
.
├── app.py              # Flask app, routing, and HTTP handlers
├── db.py               # SQLite database setup, queries, and migrations
├── utils.py            # Code generation and URL normalization utilities
├── templates/
│   └── index.html      # Responsive frontend with Tailwind CSS & Vanilla JS
├── test_app.py         # Automated pytest test suite
├── requirements.txt    # Project dependencies
└── urls.db             # SQLite database (auto-generated)
```

---

## 🚀 Getting Started

### 1. Prerequisites
Ensure you have **Python 3.10+** installed.

### 2. Clone the Repository
```bash
git clone https://github.com/your-username/url-shortner.git
cd url-shortner
```

### 3. Create and Activate a Virtual Environment
```bash
python3 -m venv venv

# On Linux / macOS:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Run the Application
```bash
flask run
```

Open your browser and visit: **`http://127.0.0.1:5000`**

---

## 📡 API Endpoints

### 1. Web Interface
- **Endpoint**: `GET /`
- **Description**: Renders the frontend UI.

---

### 2. Shorten a URL
- **Endpoint**: `POST /shorten`
- **Headers**: `Content-Type: application/json`
- **Request Body**:
  ```json
  {
    "url": "https://github.com"
  }
  ```
- **Response** (`201 Created`):
  ```json
  {
    "code": "aB3dE1",
    "message": "url shortened successfully",
    "short_url": "http://127.0.0.1:5000/aB3dE1"
  }
  ```

---

### 3. Redirect to Original URL
- **Endpoint**: `GET /<code>`
- **Response**: `302 Found` (redirects to the target destination) or `404 Not Found`.

---

### 4. Get URL Analytics
- **Endpoint**: `GET /stats/<code>`
- **Response** (`200 OK`):
  ```json
  {
    "code": "aB3dE1",
    "original_url": "https://github.com",
    "created_at": "2026-11-11 16:30:00",
    "clicks": 5
  }
  ```

---

## 🧪 Running Tests

The project includes unit and integration tests covering API endpoints, input validation, click tracking, and error states.

Run the test suite with:

```bash
pytest -v
```

---

## 🛡️ Security & Best Practices

- **Parameterized SQL Queries**: Fully protected against SQL injection attacks using parameterized SQLite queries (`?`).
- **Input Validation**: Rejects malformed JSON payloads, non-string inputs, and unsupported schemes (e.g., `javascript:`, `ftp:`).
- **Safe Database Lifecycles**: Explicit connection closing in `finally` blocks to prevent database locks.

