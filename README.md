# **AWS Cost Breakdown API**

This project provides a simple REST API built with **Python** and **FastAPI** to fetch and display AWS cost breakdown data using the **Boto3 SDK**.

---

## **Objective**

The primary goal of this application is to provide clear, structured JSON data for:

- **Total monthly cost**
- **Daily cost breakdown**
- **Cost breakdown by service**
- **Costs specifically for running EC2 instances**

---

## **Features**

- **FastAPI Backend**: A modern, fast (high-performance) web framework for building APIs.
- **Boto3 SDK**: The AWS SDK for Python to interact with AWS services.
- **AWS Cost Explorer**: The underlying AWS service used to query cost and usage data.
- **JSON Responses**: All data is served in a clean, easy-to-parse JSON format.
- **Interactive API Docs**: FastAPI automatically generates interactive API documentation (using Swagger UI).

---

## **Endpoints**

The following endpoints are available:

- **GET `/`** – Welcome message
- **GET `/total-cost`** – Fetches the total estimated cost for the current month
- **GET `/cost-by-service`** – Fetches the cost breakdown by AWS service for the current month
- **GET `/daily-cost-trend`** – Fetches the daily cost trend for the current month
- **GET `/ec2-cost`** – Fetches the cost specifically for running EC2 instances for the current month

---

## **Prerequisites**

- **Python 3.7+**
- **An AWS account with programmatic access**
- **AWS credentials** (Access Key ID and Secret Access Key) configured

---

## **Setup and Installation**

### 1. **Clone the Repository**

```bash
git clone <your-repository-link>
cd <your-repository-directory>

### 2. **Create a Virtual Environment**

It's highly recommended to use a virtual environment to manage project dependencies.

For **Unix/macOS**:

```bash
python3 -m venv venv
source venv/bin/activate
```
For **Windows**:

```bash
python -m venv venv
venv\Scripts\activate
```
### 3. **Install Dependencies**

```bash
pip install -r requirements.txt
```
### 4. **Set AWS Credentials**

Before running the application, ensure that your AWS credentials are set up. You can do this by:

- Setting environment variables: `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`
- Using the AWS credentials file: `~/.aws/credentials`

### 5. **Run the Application**

```bash
uv run uvicorn main:app --reload
```

### 6. **Access the API**

Open your web browser and navigate to `http://127.0.0.1:8000/docs` to access the interactive API documentation.

---

## **License**

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.

---

## **Contact**

For any questions or feedback, please contact [kukrejakush@gmail.com](mailto:kukrejakush@gmail.com).
