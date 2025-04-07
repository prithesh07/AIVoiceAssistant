# Flash: AI-Powered Voice Assistant

## Overview

Flash is an AI-powered voice assistant built on a FastAPI backend that integrates multiple cloud-based services. The project combines:
- **Twilio** for call handling and webhook integration,
- **Google Cloud Speech-to-Text** for transcribing user recordings,
- **Groq's AI API** for generating conversational responses,
- **Google Cloud Platform (GCP)** for hosting the FastAPI service and storing transcripts/recordings.

This repository contains the complete implementation of the basic flows, as demonstrated in the video demo.

## Features

- **FastAPI Backend:** A robust backend built with FastAPI for handling incoming Twilio webhook requests.
- **Twilio Integration:** Seamless call handling with Twilio, including webhook processing for incoming calls and recordings.
- **Google Cloud Storage & Transcription:** Recordings are fetched from Twilio and processed using Google Speech-to-Text, allowing voice-to-text conversion.
- **Groq AI Assistant:** Uses Groq's API to generate conversational replies based on the transcribed text.
- **GCP Hosting:** The FastAPI app is deployed on Google Cloud, leveraging free tiers (with some performance trade-offs).
- **Unified Flows:** Demonstrates the complete integration—from incoming voice call to AI-generated response—through a cohesive flow.

## Setup & Installation

### Prerequisites

- Python 3.9 or newer
- [Twilio account](https://www.twilio.com/) with valid credentials
- [Google Cloud Platform account](https://cloud.google.com/) with Speech-to-Text API enabled
- [Groq API key](https://www.groq.com/) for AI responses

### Environment Variables
Create a `.env` file with the following:

```properties
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
GROQ_API_KEY=your_groq_api_key
GOOGLE_APPLICATION_CREDENTIALS=path_to_credentials.json
GCP_BUCKET_NAME=your_bucket_name
WEBSOCKET_URL=your_ngrok_websocket_url
