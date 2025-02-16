# Use Python 3.10 as the base image
FROM python:3.10

# Set the working directory inside the container
WORKDIR /app

# Copy all project files to the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip && pip install -r requirements.txt

# Command to run the bot
CMD ["python", "bot.py"]
