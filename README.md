# 🔐 AuthAPI – FastAPI Authentication API with Supabase

## 📌 Project Overview

AuthAPI is a secure REST API built using **FastAPI** and **Supabase Authentication**. The project demonstrates modern authentication practices using **JSON Web Tokens (JWT)** to protect API endpoints.

Users can:

* Create an account
* Log in securely
* Access protected endpoints using a JWT
* Log out
* Test the API through the automatically generated Swagger UI

This project was developed as part of the FlyRank authentication assignment to demonstrate secure API development, bearer token authentication, and route protection.

---

# 🚀 Features

* User registration (Sign Up)
* User authentication (Log In)
* JWT Access Token authentication
* Protected API endpoints
* Public API endpoints
* Logout endpoint
* Reusable authentication dependency
* Interactive Swagger UI
* Environment variables for secure configuration
* GitHub ready

---

# 🛠 Technologies Used

* Python 3.10+
* FastAPI
* Supabase Authentication
* Uvicorn
* Pydantic
* Python Dotenv
* Swagger UI (FastAPI Docs)

---

# 📂 Project Structure

```text
AuthAPI
│
├── app
│   ├── __init__.py
│   ├── auth.py
│   ├── config.py
│   ├── dependencies.py
│   ├── main.py
│   ├── protected.py
│   ├── public.py
│   ├── schemas.py
│   └── security.py
│
├── screenshots
│   └── swagger.png
│
├── .env
├── .gitignore
├── README.md
└── requirements.txt
```

---

# ⚙️ Installation

## Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/AuthAPI.git
cd AuthAPI
```

---

## Create a virtual environment

Windows

```powershell
python -m venv .venv
```

Activate it

PowerShell

```powershell
.venv\Scripts\Activate.ps1
```

---

## Install dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create a file named `.env` in the project root.

```env
SUPABASE_URL=https://YOUR_PROJECT.supabase.co
SUPABASE_KEY=YOUR_SUPABASE_ANON_KEY
```

Replace these values with your own Supabase project credentials.

---

# ▶️ Running the Application

Start the development server

```bash
uvicorn app.main:app --reload
```

The API will be available at

```
http://127.0.0.1:8000
```

Swagger UI

```
http://127.0.0.1:8000/docs
```

---

# 🔒 Authentication Flow

1. Register a new account using **POST /auth/signup**.
2. Log in using **POST /auth/login**.
3. Copy the returned Access Token.
4. Click **Authorize** in Swagger UI.
5. Enter:

```
Bearer YOUR_ACCESS_TOKEN
```

6. Access protected endpoints.

---

# 📚 API Endpoints

| Method | Endpoint               | Authentication | Description                            |
| ------ | ---------------------- | -------------- | -------------------------------------- |
| POST   | `/auth/signup`         | ❌ No           | Register a new user                    |
| POST   | `/auth/login`          | ❌ No           | Authenticate user and receive JWT      |
| POST   | `/auth/logout`         | ✅ Yes          | Logout authenticated user              |
| GET    | `/public/info`         | ❌ No           | Public endpoint                        |
| GET    | `/protected/profile`   | ✅ Yes          | Returns authenticated user information |
| GET    | `/protected/dashboard` | ✅ Yes          | Example protected dashboard            |

---

# 🧪 Testing the API

## Sign Up

```json
{
    "email":"test@example.com",
    "password":"Password123!"
}
```

Expected response

```
201 Created
```

---

## Login

```json
{
    "email":"test@example.com",
    "password":"Password123!"
}
```

Expected response

```
200 OK
```

Returns

* Access Token
* Refresh Token

---

## Protected Endpoint

After authorizing with the JWT:

```
GET /protected/profile
```

Expected response

```
200 OK
```

If the token is invalid or expired

```
401 Unauthorized
```

---

# 🔐 Security Features

* JWT Authentication using Supabase
* Bearer Token Authorization
* Protected API routes
* Reusable authentication dependency
* Environment variables for API credentials
* `.gitignore` prevents sensitive information from being committed

---

# 📷 Swagger Documentation

![Swagger UI](screenshots/swagger.png)

The screenshot should show:

* All available endpoints
* Authorize button
* Protected routes
* Successful authorization

---

# 📖 HTTP Status Codes

| Status Code | Meaning            |
| ----------- | ------------------ |
| 200         | Request successful |
| 201         | User created       |
| 204         | Logout successful  |
| 400         | Bad request        |
| 401         | Unauthorized       |

---

# 📌 Future Improvements

* Refresh Token support
* User roles (Admin/User)
* Password reset
* Email verification
* Rate limiting
* Unit and integration testing
* Docker deployment
* CI/CD pipeline

---

# 👨‍💻 Author

**Ronaldo Jansen**
<img width="1362" height="724" alt="Swagger " src="https://github.com/user-attachments/assets/f34ef327-57da-45a6-a912-44a6af395910" />

GitHub: https://github.com/Naldo1818

LinkedIn: www.linkedin.com/in/ronaldo-jansen-0b0018350
