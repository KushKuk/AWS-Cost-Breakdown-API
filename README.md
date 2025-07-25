AWS Cost Breakdown API
This project provides a simple REST API built with Python and FastAPI to fetch and display AWS cost breakdown data using the Boto3 SDK.

Objective
The primary goal of this application is to provide clear, structured JSON data for:

Total monthly cost.

Daily cost breakdown.

Cost breakdown by service.

Costs specifically for running EC2 instances.

Features
FastAPI Backend: A modern, fast (high-performance) web framework for building APIs.

Boto3 SDK: The AWS SDK for Python to interact with AWS services.

AWS Cost Explorer: The underlying AWS service used to query cost and usage data.

JSON Responses: All data is served in a clean, easy-to-parse JSON format.

Interactive API Docs: FastAPI automatically generates interactive API documentation (using Swagger UI).

Endpoints
The following endpoints are available:

GET /: Welcome message.

GET /total-cost: Fetches the total estimated cost for the current month.

GET /cost-by-service: Fetches the cost breakdown by AWS service for the current month.

GET /daily-cost-trend: Fetches the daily cost trend for the current month.

GET /ec2-cost: Fetches the cost specifically for running EC2 instances for the current month.

Prerequisites
Python 3.7+

An AWS account with programmatic access.

AWS credentials (Access Key ID and Secret Access Key) configured.

Setup and Installation
1. Clone the Repository
git clone <your-repository-link>
cd <your-repository-directory>

2. Create a Virtual Environment
It's highly recommended to use a virtual environment to manage project dependencies.

# For Unix/macOS
python3 -m venv venv
source venv/bin/activate

# For Windows
python -m venv venv
.\venv\Scripts\activate

3. Install Dependencies
Install the required Python packages using pip.

pip install -r requirements.txt

4. Configure AWS Credentials
The Boto3 library needs to be configured with your AWS credentials. The most common way is to use environment variables.

IMPORTANT: For the AWS Cost Explorer API, you must use the us-east-1 region, regardless of where your other resources are located.

# For Unix/macOS
export AWS_ACCESS_KEY_ID="YOUR_AWS_ACCESS_KEY_ID"
export AWS_SECRET_ACCESS_KEY="YOUR_AWS_SECRET_ACCESS_KEY"
# If you are using temporary credentials, also set the session token
# export AWS_SESSION_TOKEN="YOUR_AWS_SESSION_TOKEN"
export AWS_DEFAULT_REGION="us-east-1"

# For Windows (Command Prompt)
set AWS_ACCESS_KEY_ID="YOUR_AWS_ACCESS_KEY_ID"
set AWS_SECRET_ACCESS_KEY="YOUR_AWS_SECRET_ACCESS_KEY"
set AWS_DEFAULT_REGION="us-east-1"

# For Windows (PowerShell)
$env:AWS_ACCESS_KEY_ID="YOUR_AWS_ACCESS_KEY_ID"
$env:AWS_SECRET_ACCESS_KEY="YOUR_AWS_SECRET_ACCESS_KEY"
$env:AWS_DEFAULT_REGION="us-east-1"

Alternatively, you can configure credentials using an AWS credentials file (~/.aws/credentials).

5. IAM Permissions
Ensure the IAM user or role associated with your credentials has the necessary permissions to access the AWS Cost Explorer. A minimal policy would be:

{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ce:GetCostAndUsage"
            ],
            "Resource": "*"
        }
    ]
}

Running the Application
Once the setup is complete, you can run the FastAPI application using Uvicorn.

uvicorn main:app --reload

main: refers to the Python file main.py.

app: refers to the FastAPI instance app created inside main.py.

--reload: enables auto-reloading, so the server will restart after code changes.

The API will be available at http://127.0.0.1:8000.

Using the API
You can interact with the API using any HTTP client like curl, Postman, or your web browser.

Interactive Documentation
FastAPI provides automatically generated API documentation. Once the server is running, navigate to:

Swagger UI: http://127.0.0.1:8000/docs

ReDoc: http://127.0.0.1:8000/redoc

These interfaces allow you to explore and test the API endpoints directly from your browser.

Example curl Commands
# Get Total Cost
curl http://127.0.0.1:8000/total-cost

# Get Cost by Service
curl http://127.0.0.1:8000/cost-by-service

# Get Daily Cost Trend
curl http://127.0.0.1:8000/daily-cost-trend

# Get EC2 Instance Cost
curl http://127.0.0.1:8000/ec2-cost