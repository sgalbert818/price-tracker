# price-tracker: serverless web scraper

# live demo

https://main.dsrqd59wkn2z0.amplifyapp.com/

# overview

This project is a serverless web scraper designed to track product prices from various e-commerce websites. Users can input a URL, and the scraper will retrieve the product information, storing it in a DynamoDB database. Using AWS Lambda, the scraper runs every 24 hours to check for price drops and notifies users accordingly.

# technologies used

Frontend: React
Backend: Flask (Python)
Web Scraping: Selenium
Database: AWS DynamoDB
Serverless Architecture: AWS Lambda
Containerization: Docker
Hosting: AWS EC2

# features

User-friendly React frontend for URL submission.
Efficient web scraping using Selenium in a Flask application.
Items stored in DynamoDB for easy retrieval and management.
Scheduled price checks every 24 hours using AWS Lambda.
Notifications for users when price drops occur.

# prerequisites

Docker
AWS Account
Python 3.x
Node.js and npm

# getting started

Clone the repository:
git clone https://github.com/yourusername/your-repo.git
cd your-repo

Set up the frontend:
cd frontend
npm install
npm start

Build the backend Docker image:
cd backend
docker build -t scraper-backend .

Run the Docker container:
docker run -p 5000:5000 scraper-backend

# deployment

Set up your Flask application on an EC2 instance.
Create a DynamoDB table to store the product information.
Create a Lambda function to run the scraper every 24 hours.
Ensure it has permissions to access DynamoDB and trigger your Flask application.
Set up an SNS topic or another method to notify users of price drops.

# usage

Open the frontend application in your web browser.
Enter the URL of the product you want to track and submit.
The scraper will retrieve the product information and store it in the database.
Users will be notified of any price drops within 24 hours.
