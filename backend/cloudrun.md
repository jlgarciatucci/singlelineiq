# Deploying SingleLineIQ Backend to Google Cloud Run

This guide describes how to containerize and deploy the FastAPI backend of **SingleLineIQ** to Google Cloud Run.

---

## Prerequisites

1. Install the [Google Cloud SDK](https://cloud.google.com/sdk/docs/install).
2. Authenticate and set your active project:
   ```bash
   gcloud auth login
   gcloud config set project YOUR_PROJECT_ID
   ```
3. Enable the required GCP APIs:
   ```bash
   gcloud services enable run.googleapis.com \
                          containerregistry.googleapis.com \
                          cloudbuild.googleapis.com
   ```

---

## Step 1: Prepare Local Files
Before deploying, make sure that:
1. The synthetic data folder is copied to `backend/data/` (so that it's included in the Cloud Build context upload).
2. `requirements.txt` includes `fpdf2` (already configured).

---

## Step 2: Build Image Using Cloud Build
Run the build from the `backend/` directory:
```bash
cd backend
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/singlelineiq-backend .
```
This uploads the backend folder to Cloud Build, compiles the container, and pushes it to Google Container Registry (GCR).

---

## Step 3: Deploy to Cloud Run
Deploy the container dynamically reading the Google Cloud Run injected `PORT` variable (which defaults to 8080):
```bash
gcloud run deploy singlelineiq-backend \
  --image gcr.io/YOUR_PROJECT_ID/singlelineiq-backend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars USE_DEMO_SLD_EXTRACT=true,USE_GEMINI=false
```

### Enabling Google Gemini Mode in Cloud Run
If you decide to deploy with live Google Vertex AI Gemini support, set the environment variables accordingly:
```bash
gcloud run deploy singlelineiq-backend \
  --image gcr.io/YOUR_PROJECT_ID/singlelineiq-backend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars USE_DEMO_SLD_EXTRACT=false,USE_GEMINI=true,GOOGLE_API_KEY=YOUR_GEMINI_API_KEY
```

---

## Step 4: Verify Deployment
Once deployed, Cloud Run will output the service URL (e.g. `https://singlelineiq-backend-xxxxxx.run.app`). Verify the deployment by requesting:
* Health Check: `https://singlelineiq-backend-xxxxxx.run.app/health`
* Demo Calculation JSON: `https://singlelineiq-backend-xxxxxx.run.app/api/demo/run`
