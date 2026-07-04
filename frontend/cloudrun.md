# Deploying SingleLineIQ Frontend to Google Cloud Run

This guide describes how to containerize and deploy the Next.js frontend to Google Cloud Run.

---

## Prerequisites
1. Ensure the backend service is deployed and that you have its live URL (e.g. `https://singlelineiq-backend-xxxxxx.run.app`).
2. Log in and configure your active Google Cloud CLI project:
   ```bash
   gcloud auth login
   gcloud config set project YOUR_PROJECT_ID
   ```

---

## Step 1: Build the Container Image using Cloud Build

Next.js bakes environment variables prefixed with `NEXT_PUBLIC_` into the static JavaScript bundles **at build-time**. 

To pass the backend URL during image compilation in Cloud Build, we use the `cloudbuild.yaml` file in this directory and specify the URL via the `--substitutions` flag.

Run this command from the `frontend/` directory (replacing the backend URL with your live service URL):

```bash
cd frontend
gcloud builds submit --config cloudbuild.yaml \
  --substitutions=_NEXT_PUBLIC_API_BASE_URL=https://singlelineiq-backend-1034700137651.us-central1.run.app .
```

---

## Step 2: Deploy to Google Cloud Run

Deploy the compiled container to Cloud Run. The container listens on port 3000 by default (set in the Dockerfile):

```bash
gcloud run deploy singlelineiq-frontend \
  --image gcr.io/YOUR_PROJECT_ID/singlelineiq-frontend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 3000
```

---

## Step 3: Access your Live App
Once deployed, Cloud Run will output your live frontend Service URL:
`https://singlelineiq-frontend-xxxxxx.run.app`

Open this link in your browser to access the live dashboard.
