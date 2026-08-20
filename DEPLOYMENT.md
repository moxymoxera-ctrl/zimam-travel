# Google Cloud Deployment Guide

## Step 1: Install Google Cloud SDK
```bash
# Download from: https://cloud.google.com/sdk/docs/install
# Or use:
winget install Google.CloudSDK
```

## Step 2: Initialize Google Cloud
```bash
gcloud init
# Login with your Google account
# Select your project (or create new one)
```

## Step 3: Enable Required APIs
```bash
gcloud services enable appengine.googleapis.com
gcloud services enable sqladmin.googleapis.com
gcloud services enable secretmanager.googleapis.com
```

## Step 4: Create Cloud SQL Instance
```bash
gcloud sql instances create travel-db \
  --database-version=POSTGRES_15 \
  --tier=db-f1-micro \
  --region=us-central1
```

## Step 5: Create Database and User
```bash
gcloud sql databases create travel_management_db --instance=travel-db
gcloud sql users create zimam --instance=travel-db --password=YOUR_PASSWORD
```

## Step 6: Deploy to App Engine
```bash
# Collect static files
python manage.py collectstatic --noinput

# Run migrations
python manage.py migrate

# Deploy
gcloud app deploy
```

## Step 7: Create Superuser
```bash
gcloud app exec -- python manage.py createsuperuser
```

## Step 8: Open the App
```bash
gcloud app browse
```

## Environment Variables
Set these in Google Cloud Secret Manager or App Engine config:
- DJANGO_SECRET_KEY
- DB_PASSWORD
- DB_HOST (Cloud SQL connection name)

## Cost Estimate
- App Engine F1 instance: ~$0.02/hour
- Cloud SQL F1: ~$0.02/hour
- Total: ~$30-50/month for low traffic
