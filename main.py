import boto3
from fastapi import FastAPI, HTTPException
from datetime import datetime, timedelta
import uvicorn
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(
    title="AWS Cost Explorer API",
    description="An API to fetch AWS cost and usage data using Boto3.",
    version="1.0.0",
)

# AWS credentials should be configured in your environment via a .env file.
# AWS_ACCESS_KEY_ID="YOUR_ACCESS_KEY"
# AWS_SECRET_ACCESS_KEY="YOUR_SECRET_KEY"

# Ensure the region is set to us-east-1 for Cost Explorer
try:
    aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")

    if not aws_access_key_id or not aws_secret_access_key:
        print("Warning: AWS credentials not found. Make sure AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY are set in your .env file.")
        client = None
    else:
        client = boto3.client(
            'ce',
            region_name='us-east-1',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key
        )
except Exception as e:
    print(f"Error initializing Boto3 client: {e}")
    client = None

def get_time_period():
    """Helper function to get the start and end date for the current month."""
    today = datetime.now()
    start_of_month = today.replace(day=1).strftime('%Y-%m-%d')
    next_month = today.replace(day=28) + timedelta(days=4)
    end_of_month = (next_month - timedelta(days=next_month.day)).strftime('%Y-%m-%d')
    return start_of_month, end_of_month

@app.on_event("startup")
async def startup_event():
    """Checks for Boto3 client initialization on startup."""
    if client is None:
        raise HTTPException(status_code=500, detail="Boto3 client could not be initialized. Please check your AWS credentials and configuration.")

@app.get("/")
def read_root():
    """Root endpoint to welcome users."""
    return {"message": "Welcome to the AWS Cost Explorer API. Use the /docs endpoint to see the API documentation."}

@app.get("/total-cost", summary="Fetch Total Cost", description="Fetches the total estimated cost for the current month.")
async def get_total_cost():
    """
    This endpoint returns the total unblended cost for the current month.
    """
    start_date, end_date = get_time_period()
    try:
        response = client.get_cost_and_usage(
            TimePeriod={
                'Start': start_date,
                'End': end_date
            },
            Granularity='MONTHLY',
            Metrics=['UnblendedCost']
        )
        total_cost = response['ResultsByTime'][0]['Total']['UnblendedCost']
        return {
            "time_period": {"start": start_date, "end": end_date},
            "total_cost": {
                "amount": round(float(total_cost['Amount']), 2),
                "unit": total_cost['Unit']
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/cost-by-service", summary="Fetch Cost Breakdown by Service", description="Fetches the cost breakdown by AWS service for the current month.")
async def get_cost_by_service():
    """
    This endpoint provides a breakdown of costs per AWS service for the current month.
    """
    start_date, end_date = get_time_period()
    try:
        response = client.get_cost_and_usage(
            TimePeriod={
                'Start': start_date,
                'End': end_date
            },
            Granularity='MONTHLY',
            Metrics=['UnblendedCost'],
            GroupBy=[
                {
                    'Type': 'DIMENSION',
                    'Key': 'SERVICE'
                }
            ]
        )
        services = []
        for item in response['ResultsByTime'][0]['Groups']:
            service_name = item['Keys'][0]
            cost = item['Metrics']['UnblendedCost']
            services.append({
                "service_name": service_name,
                "cost": {
                    "amount": round(float(cost['Amount']), 2),
                    "unit": cost['Unit']
                }
            })
        return {
             "time_period": {"start": start_date, "end": end_date},
             "services": services
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/daily-cost-trend", summary="Fetch Daily Cost Trend", description="Fetches the daily cost trend for the current month.")
async def get_daily_cost_trend():
    """
    This endpoint returns the daily cost for the current month, allowing for trend analysis.
    """
    start_date, end_date = get_time_period()
    try:
        response = client.get_cost_and_usage(
            TimePeriod={
                'Start': start_date,
                'End': end_date
            },
            Granularity='DAILY',
            Metrics=['UnblendedCost']
        )
        daily_costs = []
        for item in response['ResultsByTime']:
            date = item['TimePeriod']['Start']
            cost = item['Total']['UnblendedCost']
            daily_costs.append({
                "date": date,
                "cost": {
                    "amount": round(float(cost['Amount']), 2),
                    "unit": cost['Unit']
                }
            })
        return {
            "time_period": {"start": start_date, "end": end_date},
            "daily_costs": daily_costs
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/ec2-cost", summary="Fetch EC2 Instance Cost", description="Fetches the cost specifically for running EC2 instances for the current month.")
async def get_ec2_instance_cost():
    """
    This endpoint filters the costs to show only those related to Amazon EC2 running instances.
    """
    start_date, end_date = get_time_period()
    try:
        response = client.get_cost_and_usage(
            TimePeriod={
                'Start': start_date,
                'End': end_date
            },
            Granularity='MONTHLY',
            Metrics=['UnblendedCost'],
            Filter={
                "Dimensions": {
                    "Key": "SERVICE",
                    "Values": ["Amazon Elastic Compute Cloud - Compute"]
                }
            }
        )
        total_cost = response['ResultsByTime'][0]['Total']['UnblendedCost']
        return {
            "service": "Amazon EC2 Instances",
            "time_period": {"start": start_date, "end": end_date},
            "total_cost": {
                "amount": round(float(total_cost['Amount']), 2),
                "unit": total_cost['Unit']
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
