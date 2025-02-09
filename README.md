# Zoover Backend Setup Guide

##  Project Setup
This guide explains how to set up the project, configure the database, and create the required tables.

---

##  Prerequisites
Ensure you have the following installed:
- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)
- Git

---

##  Installation & Setup
### **1. Clone the Repository**
```bash
 git clone 
 cd zoover-backend
```

### **2. Create and Configure `.env` File**
Create a `.env` file in the root directory:
```bash
touch .env
```

Then, add the variables which are send by 1password

> **Note:** Never commit your `.env` file to GitHub.

### **3. Build and Start the Docker Containers**
Run the following command to start PostgreSQL and the backend service:
```bash
docker-compose up --build -d
```
This will:
- Start a PostgreSQL database (`db` service)
- Build and start the Python backend (`zoover-backend` service)

### **4. Verify Database Connection**
To check if the database is running, run:
```bash
docker ps
```
You should see `zoover-db` and `zoover-backend` running.

To test if the backend container can connect to the database, run:
```bash
docker exec -it zoover-backend psql -h db -U zoover -d zoover
```
If connected successfully, you'll see:
```bash
zoover=#
```

---

## 📋 Creating the Database Tables
### **1. Run the Table Creation Script**
To create the database tables, execute:
```bash
docker exec -it zoover-backend python backend/create_tables.py

### **2. Verify Tables Exist**
You can check the created tables by running:
```bash
docker exec -it zoover-backend psql -h db -U zoover -d zoover -c "\dt"
```
This should list all database tables.


---

## 📖 Useful Commands
| Command | Description |
|---------|-------------|
| `docker-compose up -d` | Start the project |
| `docker-compose down` | Stop and remove containers |
| `docker ps` | List running containers |
| `docker logs zoover-db` | View PostgreSQL logs |
| `docker exec -it zoover-backend bash` | Access the backend container |
| `docker exec -it zoover-db psql -U zoover -d zoover` | Open PostgreSQL shell |
| `docker exec -it zoover-backend python backend/create_tables.py` | Create database tables |
| `docker exec -it zoover-backend python backend/import_data.py` | Import the data |

---

#  Importing Data into PostgreSQL

Once the database tables are created, the next step is to **import accommodations and reviews** from JSON files into the PostgreSQL database.

---

##  Importing Data from `accommodations.json` and `reviews.json`
### **1. Run the Data Import Script**
Execute the following command to import data into the database:
```bash
docker exec -it zoover-backend python backend/import_data.py
```

---

## Verify of FastAPI is running: 

```bash
docker ps
```

### FastAPI provides interactive documentation:

 Swagger UI (Interactive API) → http://localhost:8000/docs
 ReDoc (Alternative API Docs) → http://localhost:8000/redoc

## Api Endpoints

## List all accommodations
```bash
curl -s "http://localhost:8000/accommodations"

```

## Get a single accommodation
```bash
curl -s "http://localhost:8000/accommodations/<accommodation_id>" 

```
## List all Reviews from an Accommodation 
```bash
curl -s "http://localhost:8000/accommodations/<accommodation_id>" 

```
## List all Reviews from an Accommodation 
```bash
curl -s "http://localhost:8000/accommodations/<accommodation_id>" 

```
## Get a single Review 
```bash
curl -s "http://localhost:8000/accommodations/<accommodation_id>/reviews/<review_id>"


```

