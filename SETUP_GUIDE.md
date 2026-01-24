# 🚀 Nexora AI - Local Setup Guide (Windows)

This guide will help you run the Nexora AI project locally on your Windows machine.

---

## 📋 Prerequisites

Before starting, ensure you have the following installed:

| Tool | Required Version | Download Link |
|------|------------------|---------------|
| **Python** | 3.12+ | [python.org](https://www.python.org/downloads/) |
| **Node.js** | LTS (18+) | [nodejs.org](https://nodejs.org/) |
| **MySQL** | 8.0+ | [mysql.com](https://dev.mysql.com/downloads/installer/) |
| **Docker** (optional) | Latest | [docker.com](https://www.docker.com/products/docker-desktop/) |

---

## 🗄️ Step 1: Set Up MySQL Database

1. **Open MySQL command line or MySQL Workbench**

2. **Create the database:**
   ```sql
   CREATE DATABASE nexora_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

3. **Create a user (optional but recommended):**
   ```sql
   CREATE USER 'nexora_user'@'localhost' IDENTIFIED BY 'your_secure_password';
   GRANT ALL PRIVILEGES ON nexora_db.* TO 'nexora_user'@'localhost';
   FLUSH PRIVILEGES;
   ```

---

## 🔧 Step 2: Set Up the Backend

### 2.1 Navigate to backend directory

```powershell
cd c:\Users\mamta\Downloads\juststudy\Nexora-main\backend
```

### 2.2 Create a Python virtual environment

```powershell
python -m venv venv
```

### 2.3 Activate the virtual environment

```powershell
.\venv\Scripts\activate
```

### 2.4 Install Python dependencies

```powershell
pip install -r requirements.txt
```

### 2.5 Configure environment variables

Copy the example file to create your `.env` file:

```powershell
copy .env.example .env
```

Then edit the `.env` file and update these values:

```env
# Update with your MySQL credentials
DB_USER=nexora_user
DB_PASSWORD=your_secure_password
DB_HOST=localhost
DB_PORT=3306
DB_NAME=nexora_db

# Change this to a secure random string
SECRET_KEY=your-very-long-random-secret-key-here
SESSION_SECRET_KEY=another-random-secret-key

# ChromaDB URL (keep as-is if running locally via Docker)
CHROMA_DB_URL=http://localhost:8000
```

### 2.6 Start ChromaDB (Vector Database)

**Option A: Using Docker (Recommended)**

```powershell
docker run -d -p 8000:8000 --name nexora-chromadb chromadb/chroma:latest
```

**Option B: Using Docker Compose (from backend folder)**

```powershell
docker-compose up -d chromadb
```

### 2.7 Run the Backend Server

```powershell
# Make sure venv is activated
uvicorn src.main:app --reload --host 127.0.0.1 --port 8127
```

✅ The backend API will be running at: **http://localhost:8127**

📖 API Documentation: **http://localhost:8127/docs**

---

## 🎨 Step 3: Set Up the Frontend

### 3.1 Open a new terminal and navigate to frontend

```powershell
cd c:\Users\mamta\Downloads\juststudy\Nexora-main\frontend
```

### 3.2 Install Node.js dependencies

```powershell
npm install
```

### 3.3 Run the development server

```powershell
npm run dev
```

✅ The frontend will be running at: **http://localhost:3000**

---

## ✅ Step 4: Verify the Setup

1. Open your browser and go to: **http://localhost:3000**
2. You should see the Nexora AI landing page
3. Try registering a new account to verify the backend connection

---

## 🛠️ Optional: Create an Admin User

If you need an admin account, run:

```powershell
cd c:\Users\mamta\Downloads\juststudy\Nexora-main\backend
.\venv\Scripts\activate
python create_admin.py
```

---

## 📊 Quick Reference - Running the Application

| Service | Command | URL |
|---------|---------|-----|
| **MySQL** | (runs as service) | localhost:3306 |
| **ChromaDB** | `docker run -d -p 8000:8000 chromadb/chroma:latest` | localhost:8000 |
| **Backend** | `uvicorn src.main:app --reload --port 8127` | localhost:8127 |
| **Frontend** | `npm run dev` | localhost:3000 |

---

## ⚠️ Troubleshooting

### Common Issues

**1. MySQL Connection Error**
- Verify MySQL service is running
- Check credentials in `.env` file match your MySQL setup
- Ensure the database `nexora_db` exists

**2. ChromaDB Connection Error**
- Make sure Docker is running
- Check if ChromaDB container is active: `docker ps`
- Restart ChromaDB: `docker restart nexora-chromadb`

**3. Frontend can't connect to Backend**
- Ensure backend is running on port 8127
- Check the proxy configuration in `vite.config.js`

**4. Module not found errors (Backend)**
- Ensure virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`

**5. npm install fails**
- Clear npm cache: `npm cache clean --force`
- Delete `node_modules` and `package-lock.json`, then retry

---

## 🎉 You're Done!

Your Nexora AI instance should now be running locally:

- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8127
- **API Docs:** http://localhost:8127/docs
