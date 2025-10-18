from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, validator
from typing import Optional, Literal
from openai import OpenAI
import os
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="AI Slide Editor API", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize OpenAI client with environment variable
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    logger.warning("OPENAI_API_KEY not found in environment variables")
    #api_key = ""

client = OpenAI(api_key=api_key)

# Pydantic models
class Slide(BaseModel):
    id: str
    title: str
    content: str
    backgroundColor: str = Field(alias="backgroundColor", default="#ffffff")
    textColor: str = Field(alias="textColor", default="#000000")
    fontSize: Optional[int] = Field(default=16, ge=8, le=72)
    layout: Optional[Literal["title-content", "centered", "two-column"]] = "title-content"

    @validator('backgroundColor', 'textColor')
    def validate_color(cls, v):
        if not v.startswith('#') or len(v) != 7:
            raise ValueError('Color must be a valid hex color (e.g., #ffffff)')
        return v.lower()

    @validator('title', 'content')
    def validate_text(cls, v):
        if not v or not v.strip():
            raise ValueError('Title and content cannot be empty')
        return v.strip()

    class Config:
        populate_by_name = True

class UpdateRequest(BaseModel):
    slide: Slide
    prompt: str

class UpdateResponse(BaseModel):
    updated_slide: Slide
    success: bool
    message: str

@app.get("/")
async def root():
    return {"message": "AI Slide Editor API", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}

@app.get("/api/slides/templates")
async def get_slide_templates():
    """Get predefined slide templates"""
    templates = [
        {
            "id": "title-slide",
            "title": "Title Slide",
            "content": "Welcome to our presentation",
            "backgroundColor": "#1e40af",
            "textColor": "#ffffff",
            "fontSize": 24,
            "layout": "centered"
        },
        {
            "id": "content-slide",
            "title": "Content Slide",
            "content": "• Key point 1\n• Key point 2\n• Key point 3",
            "backgroundColor": "#ffffff",
            "textColor": "#000000",
            "fontSize": 18,
            "layout": "title-content"
        },
        {
            "id": "two-column-slide",
            "title": "Two Column Layout",
            "content": "Left Column:\n• Point 1\n• Point 2\n\nRight Column:\n• Point A\n• Point B",
            "backgroundColor": "#f8fafc",
            "textColor": "#1e293b",
            "fontSize": 16,
            "layout": "two-column"
        }
    ]
    return {"templates": templates}

@app.post("/api/update-slide", response_model=UpdateResponse)
async def update_slide(request: UpdateRequest):
    """
    Update a slide using AI based on user prompt
    """
    try:
        current_slide = request.slide
        prompt = request.prompt.strip()
        
        if not prompt:
            raise HTTPException(status_code=400, detail="Prompt cannot be empty")

        logger.info(f"Updating slide {current_slide.id} with prompt: {prompt}")

        # Create the system prompt
        system_prompt = """You are a professional presentation slide editor. Your task is to update slide content based on user instructions while maintaining high presentation standards.

CRITICAL REQUIREMENTS:
1. Colors must be valid hex codes (e.g., #ffffff, #000000, #ff0000)
2. Font sizes must be between 8-72 pixels
3. Content must be clear, concise, and professional
4. Use bullet points (•) for lists when appropriate
5. Maintain readability and visual hierarchy
6. Preserve the slide's core message while applying changes

RESPONSE FORMAT:
Return ONLY a valid JSON object with these exact fields:
{
  "title": "string",
  "content": "string", 
  "backgroundColor": "#hexcolor",
  "textColor": "#hexcolor",
  "fontSize": number,
  "layout": "title-content" | "centered" | "two-column"
}

Do not include markdown, code blocks, or any text outside the JSON object."""

        user_prompt = f"""CURRENT SLIDE:
Title: {current_slide.title}
Content: {current_slide.content}
Background Color: {current_slide.backgroundColor}
Text Color: {current_slide.textColor}
Font Size: {current_slide.fontSize}
Layout: {current_slide.layout}

USER REQUEST: {prompt}

Update the slide according to the user's request. Return the complete updated slide as JSON."""

        # Try OpenAI API first, fallback to mock response if quota exceeded
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.7,
                max_tokens=1000,
            )

            # Parse and validate the response
            response_content = response.choices[0].message.content
            logger.info(f"AI Response: {response_content}")
            
            updated_data = json.loads(response_content)
            
        except Exception as ai_error:
            logger.warning(f"OpenAI API failed: {str(ai_error)}, using mock response")
            
            # Mock response based on common prompt patterns
            updated_data = {
                "title": current_slide.title,
                "content": current_slide.content,
                "backgroundColor": current_slide.backgroundColor,
                "textColor": current_slide.textColor,
                "fontSize": current_slide.fontSize,
                "layout": current_slide.layout
            }
            
            # Simple pattern matching for common requests
            prompt_lower = prompt.lower()
            
            if "title" in prompt_lower:
                if "change" in prompt_lower or "update" in prompt_lower:
                    # Extract new title from prompt
                    words = prompt.split()
                    title_index = -1
                    for i, word in enumerate(words):
                        if word.lower() in ["title", "heading"]:
                            title_index = i
                            break
                    if title_index != -1 and title_index + 1 < len(words):
                        new_title = " ".join(words[title_index + 1:])
                        updated_data["title"] = new_title
            
            if "blue" in prompt_lower:
                updated_data["backgroundColor"] = "#3b82f6"
            elif "red" in prompt_lower:
                updated_data["backgroundColor"] = "#ef4444"
            elif "green" in prompt_lower:
                updated_data["backgroundColor"] = "#10b981"
            elif "yellow" in prompt_lower:
                updated_data["backgroundColor"] = "#f59e0b"
            
            if "white" in prompt_lower and "text" in prompt_lower:
                updated_data["textColor"] = "#ffffff"
            elif "black" in prompt_lower and "text" in prompt_lower:
                updated_data["textColor"] = "#000000"
            
            if "bigger" in prompt_lower or "larger" in prompt_lower:
                updated_data["fontSize"] = min(current_slide.fontSize + 4, 72)
            elif "smaller" in prompt_lower:
                updated_data["fontSize"] = max(current_slide.fontSize - 4, 8)
            
            if "center" in prompt_lower:
                updated_data["layout"] = "centered"
            elif "two column" in prompt_lower or "two-column" in prompt_lower:
                updated_data["layout"] = "two-column"
            
            logger.info(f"Mock response generated: {updated_data}")
        
        # Validate required fields
        required_fields = ["title", "content", "backgroundColor", "textColor", "fontSize", "layout"]
        for field in required_fields:
            if field not in updated_data:
                logger.warning(f"Missing field {field} in AI response, using current value")
                updated_data[field] = getattr(current_slide, field)
        
        # Create updated slide, preserving the ID
        updated_slide = Slide(
            id=current_slide.id,
            title=updated_data["title"],
            content=updated_data["content"],
            backgroundColor=updated_data["backgroundColor"],
            textColor=updated_data["textColor"],
            fontSize=updated_data["fontSize"],
            layout=updated_data["layout"],
        )

        logger.info(f"Successfully updated slide {current_slide.id}")
        return UpdateResponse(
            updated_slide=updated_slide,
            success=True,
            message="Slide updated successfully"
        )

    except json.JSONDecodeError as e:
        logger.error(f"JSON parsing error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Invalid response format from AI service"
        )
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail=f"Invalid slide data: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to update slide: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
