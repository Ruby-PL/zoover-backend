# Use Python image
FROM python:3.11

# Set the working directory inside the container
WORKDIR /app

# Install dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# ✅ Copy backend files into `/app/backend/`
COPY backend /app/backend  

# ✅ Run FastAPI from the `backend/` module
CMD ["uvicorn", "backend.api:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

