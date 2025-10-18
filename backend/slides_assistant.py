#!/usr/bin/env python3
"""
Slides Assistant - An example agent that uses the slide-specific tools
to help users modify Slidev presentations.
"""

from typing import Dict, Any, List, Optional
import json
from slidev_tools import (
    update_element_content,
    update_element_color,
    update_slide_background,
    create_new_slide,
    parse_slides,
    get_slide_content
)


class SlidesAssistant:
    """
    A slides assistant that can modify Slidev presentations using the custom tools.
    """

    def __init__(self, presentation_file: str):
        """Initialize the assistant with a presentation file."""
        self.presentation_file = presentation_file
        self.load_presentation()

    def load_presentation(self):
        """Load the presentation content from file."""
        try:
            with open(self.presentation_file, 'r') as f:
                self.content = f.read()
        except FileNotFoundError:
            # Create a default presentation if file doesn't exist
            self.content = self._create_default_presentation()
            self.save_presentation()

    def save_presentation(self):
        """Save the current presentation content to file."""
        with open(self.presentation_file, 'w') as f:
            f.write(self.content)

    def _create_default_presentation(self) -> str:
        """Create a default presentation template."""
        return """# Welcome

<p id="welcome-text">Start your presentation here</p>

---

# Content

<div id="main-content">
  Add your content here
</div>

---

# Thank You

<p id="thank-you">Thanks for watching!</p>
"""

    def get_slide_count(self) -> int:
        """Get the total number of slides."""
        return len(parse_slides(self.content))

    def get_slide_preview(self, slide_number: int) -> Optional[str]:
        """Get a preview of a specific slide."""
        slide_content, _, _ = get_slide_content(self.content, slide_number)
        if slide_content:
            # Return first 200 characters as preview
            return slide_content[:200] + ("..." if len(slide_content) > 200 else "")
        return None

    def list_all_slides(self) -> List[Dict[str, Any]]:
        """List all slides with their titles and previews."""
        slides = parse_slides(self.content)
        slide_info = []

        for i, slide in enumerate(slides, 1):
            # Extract title (first heading if exists)
            title = "Untitled"
            lines = slide.strip().split('\n')
            for line in lines:
                if line.startswith('#'):
                    title = line.lstrip('#').strip()
                    break

            slide_info.append({
                'number': i,
                'title': title,
                'preview': slide[:100] + ("..." if len(slide) > 100 else "")
            })

        return slide_info

    def update_text(self, slide_number: int, element_id: str, new_text: str) -> bool:
        """
        Update text content of an element.

        Returns True if successful, False otherwise.
        """
        try:
            self.content = update_element_content(
                self.content,
                slide_number,
                element_id,
                new_text
            )
            self.save_presentation()
            return True
        except Exception as e:
            print(f"Error updating text: {e}")
            return False

    def change_color(self, slide_number: int, element_id: str, color: str) -> bool:
        """
        Change the color of an element.

        Returns True if successful, False otherwise.
        """
        try:
            self.content = update_element_color(
                self.content,
                slide_number,
                element_id,
                color
            )
            self.save_presentation()
            return True
        except Exception as e:
            print(f"Error changing color: {e}")
            return False

    def set_background(self, slide_number: int, color: str) -> bool:
        """
        Set the background color of a slide.

        Returns True if successful, False otherwise.
        """
        try:
            self.content = update_slide_background(
                self.content,
                slide_number,
                color
            )
            self.save_presentation()
            return True
        except Exception as e:
            print(f"Error setting background: {e}")
            return False

    def add_slide(
        self,
        position: Optional[int] = None,
        title: Optional[str] = None,
        content: Optional[str] = None,
        background: Optional[str] = None,
        layout: str = "default"
    ) -> bool:
        """
        Add a new slide to the presentation.

        Returns True if successful, False otherwise.
        """
        try:
            self.content = create_new_slide(
                self.content,
                position,
                title,
                content,
                background,
                layout
            )
            self.save_presentation()
            return True
        except Exception as e:
            print(f"Error adding slide: {e}")
            return False

    def process_command(self, command: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a command from the user.

        Command format:
        {
            "action": "update_text" | "change_color" | "set_background" | "add_slide" | "list_slides",
            "params": {...}
        }
        """
        action = command.get("action")
        params = command.get("params", {})

        if action == "update_text":
            success = self.update_text(
                params.get("slide_number"),
                params.get("element_id"),
                params.get("new_text")
            )
            return {
                "success": success,
                "message": "Text updated successfully" if success else "Failed to update text"
            }

        elif action == "change_color":
            success = self.change_color(
                params.get("slide_number"),
                params.get("element_id"),
                params.get("color")
            )
            return {
                "success": success,
                "message": "Color changed successfully" if success else "Failed to change color"
            }

        elif action == "set_background":
            success = self.set_background(
                params.get("slide_number"),
                params.get("color")
            )
            return {
                "success": success,
                "message": "Background set successfully" if success else "Failed to set background"
            }

        elif action == "add_slide":
            success = self.add_slide(
                params.get("position"),
                params.get("title"),
                params.get("content"),
                params.get("background"),
                params.get("layout", "default")
            )
            return {
                "success": success,
                "message": "Slide added successfully" if success else "Failed to add slide"
            }

        elif action == "list_slides":
            slides = self.list_all_slides()
            return {
                "success": True,
                "slides": slides,
                "total": len(slides)
            }

        else:
            return {
                "success": False,
                "message": f"Unknown action: {action}"
            }


def demo_assistant():
    """Demonstrate the slides assistant functionality."""
    print("="*50)
    print("Slides Assistant Demo")
    print("="*50 + "\n")

    # Create an assistant
    assistant = SlidesAssistant("demo_presentation.md")

    # List current slides
    print("Current slides:")
    result = assistant.process_command({
        "action": "list_slides"
    })
    for slide in result["slides"]:
        print(f"  Slide {slide['number']}: {slide['title']}")

    print("\n" + "-"*30 + "\n")

    # Add a new slide
    print("Adding a new slide...")
    result = assistant.process_command({
        "action": "add_slide",
        "params": {
            "position": 2,
            "title": "New Feature",
            "content": '<p id="feature-desc">This is an amazing new feature!</p>',
            "background": "#3498db"
        }
    })
    print(f"Result: {result['message']}")

    print("\n" + "-"*30 + "\n")

    # Update text on the new slide
    print("Updating text on the new slide...")
    result = assistant.process_command({
        "action": "update_text",
        "params": {
            "slide_number": 2,
            "element_id": "feature-desc",
            "new_text": "This feature will revolutionize presentations!"
        }
    })
    print(f"Result: {result['message']}")

    print("\n" + "-"*30 + "\n")

    # Change color of an element
    print("Changing text color to red...")
    result = assistant.process_command({
        "action": "change_color",
        "params": {
            "slide_number": 2,
            "element_id": "feature-desc",
            "color": "#e74c3c"
        }
    })
    print(f"Result: {result['message']}")

    print("\n" + "-"*30 + "\n")

    # Set background for first slide
    print("Setting background for first slide...")
    result = assistant.process_command({
        "action": "set_background",
        "params": {
            "slide_number": 1,
            "color": "#2c3e50"
        }
    })
    print(f"Result: {result['message']}")

    print("\n" + "-"*30 + "\n")

    # List slides again to see changes
    print("Updated slides:")
    result = assistant.process_command({
        "action": "list_slides"
    })
    for slide in result["slides"]:
        print(f"  Slide {slide['number']}: {slide['title']}")

    print("\n" + "="*50)
    print("Demo completed! Check demo_presentation.md for the results.")


if __name__ == "__main__":
    demo_assistant()