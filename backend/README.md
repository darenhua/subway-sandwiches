# AI Slide Editor Backend

Python FastAPI backend for the AI Slide Editor application.

## Setup

1. Install dependencies:
\`\`\`bash
pip install -r requirements.txt
\`\`\`

2. Set your OpenAI API key:
\`\`\`bash
export OPENAI_API_KEY="your-api-key-here"
\`\`\`

3. Run the server:
\`\`\`bash
python main.py
\`\`\`

Or with uvicorn directly:
\`\`\`bash
uvicorn main:app --reload --port 8000
\`\`\`

## API Endpoints

- `GET /` - Root endpoint
- `GET /health` - Health check
- `POST /api/update-slide` - Update slide with AI

## Example Request

\`\`\`json
{
  "slide": {
    "id": "1",
    "title": "My Slide",
    "content": "Slide content",
    "backgroundColor": "#ffffff",
    "textColor": "#000000",
    "fontSize": 16,
    "layout": "title-content"
  },
  "prompt": "Make the title more engaging"
}
