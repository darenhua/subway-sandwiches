# Subway Sandwiches Voice AI Product

## Overview

This project is a full-stack application for voice-driven slide editing and transcription, powered by Claude Sonnet, Corpus, and OpenAI. It features:

- 🎤 Text and voice input for slide updates
- 🤖 AI-powered slide modifications using GPT-4o-mini
- 👀 Visual diff viewer showing before/after changes
- ✅ Approval workflow before applying changes
- 🎨 Split-pane interface with resizable panels
- 🐍 Python FastAPI backend for AI processing

## Architecture

- **Frontend**: Next.js 15 with React, TypeScript, and Tailwind CSS
- **Backend**: Python FastAPI with OpenAI integration
- **AI Model**: GPT-4o-mini for slide updates

## Getting Started

### 1. Start the Python Backend

\`\`\`bash
cd backend
pip install -r requirements.txt
export OPENAI_API_KEY="your-api-key-here"
python main.py
\`\`\`

The backend will run on `http://localhost:8000`

### 2. Start the Frontend

\`\`\`bash
npm install
npm run dev
\`\`\`

The frontend will run on `http://localhost:3000`

### 3. Configure Environment Variables

Copy `.env.local.example` to `.env.local` and update if needed:

\`\`\`bash
cp .env.local.example .env.local
\`\`\`

## Usage

1. View your current slide in the left panel
2. Enter a text prompt or use voice input in the right panel
3. Review the AI-generated changes in the diff viewer
4. Approve or reject the changes

### Example Prompts

- "Make the title blue and add bullet points to the content"
- "Change the background to dark mode with white text"
- "Make the font size larger and center the content"
- "Add three bullet points about AI benefits"

## API Documentation

Once the backend is running, visit:

- API Docs: `http://localhost:8000/docs`
- Health Check: `http://localhost:8000/health`

## Tech Stack

- Next.js 15 (App Router)
- React 19
- TypeScript
- Tailwind CSS v4
- shadcn/ui components
- Python FastAPI
- OpenAI API
- Pydantic for data validation

## Creators

Daren Hua, Siri Pranitha, Nadia Choophungart, Nitya Pakala
Bootstrapping Reality Hackathon, October 18 2025
Collapse
message.txt
3 KB
nitu — Yesterday at 9:19 PM
q3:
throughout the past 12 hours, our team has gone from not knowing each other at all to collaborating closely on a project we’re genuinely passionate about ~ one built on strong communication, creativity, and teamwork. we’re most proud of how we came together to build something entirely new in such a short time.

while only a few of us had prior experience with voice ai, we quickly learned as a group, experimenting with different models like cubby and elevenlabs before ultimately choosing openai for its technical feasibility and seamless integration potential. throughout the process, we pushed ourselves to understand how to run voice-enabled applications end to end, from prompt engineering and model tuning to deployment and full-stack integration. it’s been an intense but incredibly rewarding experience that has helped show us what’s possible when we combine our skills and curiosity under tight constraints!
nitu — Yesterday at 9:29 PM
q2:
the project’s frontend architecture is built with next.js, react, typescript, and tailwind css, while the backend is powered by python fastapi with openai integration. we leveraged claude sonnet, openai, and corpus to handle different layers of intelligence—using gpt-4o-mini specifically for dynamic slide updates. data validation and type enforcement are managed through pydantic to ensure clean and reliable api communication between the frontend and backend.

the claude sonnet model was fine-tuned to interpret natural voice commands into structured update instructions for slide automation. we trained it on slidev documentation, using tools like webfetch to scrape and extract the most relevant api methods and configuration patterns. this allowed the model to map user intents directly to slidev actions, enabling accurate, context-aware slide generation and modification.
siri — Yesterday at 10:53 PM
Guys, what's happening - how are the other presentations



# Subway Sandwiches Voice AI Product

## Overview

This project is a full-stack application for voice-driven slide editing and transcription, powered by Claude Sonnet, Corpus, and OpenAI. It features:

- 🎤 Text and voice input for slide updates
- 🤖 AI-powered slide modifications using GPT-4o-mini
- 👀 Visual diff viewer showing before/after changes
- ✅ Approval workflow before applying changes
- 🎨 Split-pane interface with resizable panels
- 🐍 Python FastAPI backend for AI processing

## Architecture

- **Frontend**: Next.js 15 with React, TypeScript, and Tailwind CSS
- **Backend**: Python FastAPI with OpenAI integration
- **AI Model**: GPT-4o-mini for slide updates

## Getting Started

### 1. Start the Python Backend

\`\`\`bash
cd backend
pip install -r requirements.txt
export OPENAI_API_KEY="your-api-key-here"
python main.py
\`\`\`

The backend will run on `http://localhost:8000`

### 2. Start the Frontend

\`\`\`bash
npm install
npm run dev
\`\`\`

The frontend will run on `http://localhost:3000`

### 3. Configure Environment Variables

Copy `.env.local.example` to `.env.local` and update if needed:

\`\`\`bash
cp .env.local.example .env.local
\`\`\`

## Usage

1. View your current slide in the left panel
2. Enter a text prompt or use voice input in the right panel
3. Review the AI-generated changes in the diff viewer
4. Approve or reject the changes

### Example Prompts

- "Make the title blue and add bullet points to the content"
- "Change the background to dark mode with white text"
- "Make the font size larger and center the content"
- "Add three bullet points about AI benefits"

## API Documentation

Once the backend is running, visit:

- API Docs: `http://localhost:8000/docs`
- Health Check: `http://localhost:8000/health`

## Tech Stack

- Next.js 15 (App Router)
- React 19
- TypeScript
- Tailwind CSS v4
- shadcn/ui components
- Python FastAPI
- OpenAI API
- Pydantic for data validation

## Creators

Daren Hua, Siri Pranitha, Nadia Choophungart, Nitya Pakala
Bootstrapping Reality Hackathon, October 18 2025
