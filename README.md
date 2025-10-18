# AI Slide Editor

A Cursor-like slide editor that uses AI to update slides based on text and voice prompts. Features a Python FastAPI backend with OpenAI integration.

## Features

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
