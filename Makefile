build-image:
	docker build -f deploy/Dockerfile --build-arg TOKEN=... -t chat-bot:0.1 .

run-bot:
	docker run --rm chat-bot:0.1

gcloud-push:
	gcloud builds submit --tag chat-bot

	gcloud builds submit --tag gcr.io/thaijourneybot/chat-bot .

	gcloud beta run deploy chat-bot --image gcr.io/thaijourneybot/chat-bot --region us-central1 --platform managed --allow-unauthenticated --quiet

	gcloud projects add-iam-policy-binding thaijourneybot \
            --member='user:mediankin.viktor@gmail.com' --role='roles/owner'

    gcloud run deploy ThaiJourneyBot --image gcr.io/thaijourneybot/chat-bot:latest --platform managed --region us-central1 --allow-unauthenticated

	1. docker tag LOCAL_IMAGE_NAME gcr.io/PROJECT_ID/IMAGE_NAME:TAG
	   docker tag chat-bot:0.1 gcr.io/thaijourneybot/chat-bot:0.1

	2. gcloud auth configure-docker

	3. docker push gcr.io/PROJECT_ID/IMAGE_NAME:TAG
	   docker push gcr.io/thaijourneybot/chat-bot:0.1

	4. gcloud run deploy SERVICE_NAME --image gcr.io/PROJECT_ID/IMAGE_NAME:TAG --platform managed --region REGION
	   gcloud run deploy thaijourneybot --image gcr.io/thaijourneybot/chat-bot:0.1 --platform managed --region asia-southeast1  # Singapore  europe-north1 Finland
