# Use official Python base image
FROM python:3.10

# Set the working directory inside the container
WORKDIR /app

# Copy the necessary files into the container
COPY . /app

# Install google-cloud explicitly
RUN pip install google-cloud

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port Streamlit runs on
EXPOSE 8501

# Run the application
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
