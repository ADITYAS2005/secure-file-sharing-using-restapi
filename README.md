# secure-file-sharing-using-restapi
Secure File Sharing System with FastAPI, SQLAlchemy, and PostgreSQL. Supports two user roles (Ops and Client) with JWT authentication, file upload restrictions, email verification, and secure time-limited download URLs.
 Secure File Sharing System
This project implements a secure file sharing platform using FastAPI, SQLAlchemy, and PostgreSQL (or SQLite). It supports two user types:

Ops Users

Upload files (pptx, docx, xlsx only)

Client Users

Sign up and verify email

List available files

Get secure download links

Download files with time-limited tokens

🎯 Features
✅ JWT-based authentication
✅ Role-based access control
✅ Email verification links
✅ Secure signed download URLs
✅ RESTful API endpoints
✅ Supports PostgreSQL and SQLite

🛠️ Tech Stack
Python 3.11+

FastAPI

SQLAlchemy

Pydantic

Passlib

Python-Jose

Uvicorn

⚙️ How to Run
Clone the repo

bash
Copy
Edit
git clone https://github.com/YOUR-USERNAME/secure-file-sharing-system.git
cd secure-file-sharing-system
Create a virtual environment

nginx
Copy
Edit
python -m venv venv
Activate the virtual environment

On Windows:

Copy
Edit
.\venv\Scripts\activate
On macOS/Linux:

bash
Copy
Edit
source venv/bin/activate
Install dependencies

nginx
Copy
Edit
pip install -r requirements.txt
Set up the database

By default, uses SQLite (test.db)

For PostgreSQL, set DATABASE_URL in .env:

bash
Copy
Edit
DATABASE_URL=postgresql://username:password@localhost/dbname
Run the server

lua
Copy
Edit
uvicorn app.main:app --reload
Visit

arduino
Copy
Edit
http://127.0.0.1:8000/docs
to explore API docs.

🧩 Folder Structure
pgsql
Copy
Edit
secure-file-sharing-system/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── auth.py
│   ├── utils.py
│   └── database.py
├── uploads/
├── .env
├── requirements.txt
└── README.md
