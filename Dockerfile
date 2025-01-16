# Step 1: Use a base Python image
FROM python:3.10

# Step 2: Set the working directory
WORKDIR /app

# Step 3: Copy the requirements file
COPY requirements.txt /app/

# Step 4: Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Copy the application code
COPY . /app/

# Step 6: Expose the application port
EXPOSE 8000

# Step 7: Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
