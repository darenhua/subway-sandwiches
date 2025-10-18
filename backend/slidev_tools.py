#!/usr/bin/env python3
"""
Standalone Slidev-specific tools for working with presentations.
These tools can be imported and used independently.
"""

from typing import Optional, Tuple, List
import re


def parse_slides(content: str) -> List[str]:
    """
    Parse a Slidev markdown file into individual slides.
    Slides are separated by '---' with newlines.

    Args:
        content: The full markdown content

    Returns:
        List of slide contents
    """
    # Split by slide delimiter (--- with optional whitespace)
    slides = re.split(r'\n---\n', content)
    return slides


def get_slide_content(content: str, slide_number: int) -> Tuple[Optional[str], int, int]:
    """
    Get the content of a specific slide and its position in the file.

    Args:
        content: The full markdown content
        slide_number: The slide number (1-indexed)

    Returns:
        Tuple of (slide_content, start_index, end_index) or (None, -1, -1) if not found
    """
    slides = parse_slides(content)

    if slide_number < 1 or slide_number > len(slides):
        return None, -1, -1

    # Calculate the position of this slide in the original content
    slide_index = slide_number - 1
    start_index = 0

    # Find the start position of this slide
    for i in range(slide_index):
        # Account for the slide content and the delimiter
        start_index += len(slides[i]) + 5  # 5 for '\n---\n'

    end_index = start_index + len(slides[slide_index])

    return slides[slide_index], start_index, end_index


def update_element_content(
    file_content: str,
    slide_number: int,
    element_id: str,
    new_content: str
) -> str:
    """
    Update the text content of a specific element within a slide.
    This tool looks for HTML elements with the specified ID and updates their content.

    Args:
        file_content: The full markdown file content
        slide_number: The slide number (1-indexed)
        element_id: The ID of the element to update (e.g., "slide-1-title")
        new_content: The new text content for the element

    Returns:
        Updated file content

    Example:
        Update content of <p id="intro-text">Old text</p> to "New text"
    """
    slide_content, start_idx, end_idx = get_slide_content(file_content, slide_number)

    if slide_content is None:
        raise ValueError(f"Slide {slide_number} not found")

    # Pattern to match HTML elements with the specified ID
    # Matches: <tag id="element_id">content</tag>
    pattern = rf'(<[^>]+\sid=["\']?{re.escape(element_id)}["\']?[^>]*>)(.*?)(<\/[^>]+>)'

    def replace_content(match):
        opening_tag = match.group(1)
        closing_tag = match.group(3)
        return f"{opening_tag}{new_content}{closing_tag}"

    # Update the content within the slide
    updated_slide = re.sub(pattern, replace_content, slide_content, flags=re.DOTALL)

    # If no match found, try to match self-closing tags or markdown headers with IDs
    if updated_slide == slide_content:
        # Try markdown header with ID syntax: # Title {#element_id}
        markdown_pattern = rf'(#{{1,6}}\s+)(.*?)(\s*\{{#\s*{re.escape(element_id)}\s*\}})'

        def replace_markdown(match):
            header = match.group(1)
            id_part = match.group(3)
            return f"{header}{new_content}{id_part}"

        updated_slide = re.sub(markdown_pattern, replace_markdown, slide_content)

    # Replace the slide content in the original file
    updated_content = (
        file_content[:start_idx] +
        updated_slide +
        file_content[end_idx:]
    )

    return updated_content


def update_element_color(
    file_content: str,
    slide_number: int,
    element_id: str,
    color: str
) -> str:
    """
    Update the color of a text element within a slide using CSS styles.
    This tool adds or updates a <style> block within the slide to set the color.

    Args:
        file_content: The full markdown file content
        slide_number: The slide number (1-indexed)
        element_id: The ID of the element to style
        color: The color value (e.g., "red", "#FF0000", "rgb(255, 0, 0)")

    Returns:
        Updated file content

    Example:
        Adds/updates style for #intro-text { color: red; }
    """
    slide_content, start_idx, end_idx = get_slide_content(file_content, slide_number)

    if slide_content is None:
        raise ValueError(f"Slide {slide_number} not found")

    # Check if there's already a <style> block in the slide
    style_pattern = r'<style>(.*?)</style>'
    style_match = re.search(style_pattern, slide_content, re.DOTALL)

    if style_match:
        # Update existing style block
        existing_styles = style_match.group(1)

        # Check if the element ID already has a color rule
        id_pattern = rf'#{re.escape(element_id)}\s*{{[^}}]*}}'
        id_match = re.search(id_pattern, existing_styles)

        if id_match:
            # Update existing rule
            old_rule = id_match.group(0)
            # Extract other properties if any
            color_pattern = r'color\s*:\s*[^;]+;?'
            if re.search(color_pattern, old_rule):
                # Replace existing color
                new_rule = re.sub(color_pattern, f'color: {color};', old_rule)
            else:
                # Add color to existing rule
                new_rule = old_rule.rstrip('}') + f'\n  color: {color};\n}}'

            updated_styles = existing_styles.replace(old_rule, new_rule)
        else:
            # Add new rule for this element
            updated_styles = existing_styles.rstrip() + f'\n\n#{element_id} {{\n  color: {color};\n}}\n'

        # Replace the style block
        updated_slide = re.sub(
            style_pattern,
            f'<style>{updated_styles}</style>',
            slide_content,
            flags=re.DOTALL
        )
    else:
        # Add a new style block at the end of the slide
        style_block = f'\n\n<style>\n#{element_id} {{\n  color: {color};\n}}\n</style>'
        updated_slide = slide_content.rstrip() + style_block

    # Replace the slide content in the original file
    updated_content = (
        file_content[:start_idx] +
        updated_slide +
        file_content[end_idx:]
    )

    return updated_content


def update_slide_background(
    file_content: str,
    slide_number: int,
    background_color: str
) -> str:
    """
    Update the background color of a specific slide.
    This tool modifies or adds the frontmatter 'background' property.

    Args:
        file_content: The full markdown file content
        slide_number: The slide number (1-indexed)
        background_color: The background color (e.g., "#FF0000", "rgb(255, 0, 0)")

    Returns:
        Updated file content

    Example:
        Adds/updates frontmatter:
        ---
        background: "#FF0000"
        ---
    """
    slide_content, start_idx, end_idx = get_slide_content(file_content, slide_number)

    if slide_content is None:
        raise ValueError(f"Slide {slide_number} not found")

    # Check if the slide has frontmatter
    frontmatter_pattern = r'^---\n(.*?)\n---'
    frontmatter_match = re.match(frontmatter_pattern, slide_content, re.DOTALL)

    if frontmatter_match:
        # Update existing frontmatter
        frontmatter = frontmatter_match.group(1)

        # Check if background property exists
        background_pattern = r'^background:\s*.*$'
        if re.search(background_pattern, frontmatter, re.MULTILINE):
            # Replace existing background
            updated_frontmatter = re.sub(
                background_pattern,
                f'background: "{background_color}"',
                frontmatter,
                flags=re.MULTILINE
            )
        else:
            # Add background property
            updated_frontmatter = frontmatter.rstrip() + f'\nbackground: "{background_color}"'

        # Replace the frontmatter in the slide
        updated_slide = re.sub(
            frontmatter_pattern,
            f'---\n{updated_frontmatter}\n---',
            slide_content,
            flags=re.DOTALL
        )
    else:
        # Add frontmatter with background at the beginning of the slide
        frontmatter = f'---\nbackground: "{background_color}"\n---\n\n'
        updated_slide = frontmatter + slide_content

    # Replace the slide content in the original file
    updated_content = (
        file_content[:start_idx] +
        updated_slide +
        file_content[end_idx:]
    )

    return updated_content


def create_new_slide(
    file_content: str,
    slide_position: Optional[int] = None,
    title: Optional[str] = None,
    content: Optional[str] = None,
    background: Optional[str] = None,
    layout: Optional[str] = "default"
) -> str:
    """
    Create a new slide in the presentation.

    Args:
        file_content: The full markdown file content
        slide_position: Position to insert the slide (1-indexed). None means append at end.
        title: Optional title for the slide
        content: Optional content for the slide
        background: Optional background color
        layout: Slide layout (default, center, etc.)

    Returns:
        Updated file content with new slide
    """
    # Build the new slide
    slide_parts = []

    # Add frontmatter if needed
    if background or layout != "default":
        slide_parts.append("---")
        if layout != "default":
            slide_parts.append(f"layout: {layout}")
        if background:
            slide_parts.append(f'background: "{background}"')
        slide_parts.append("---")
        slide_parts.append("")

    # Add title if provided
    if title:
        slide_parts.append(f"# {title}")
        slide_parts.append("")

    # Add content if provided
    if content:
        slide_parts.append(content)

    new_slide = "\n".join(slide_parts)

    # Parse existing slides
    slides = parse_slides(file_content)

    if slide_position is None or slide_position > len(slides):
        # Append at the end
        if file_content.rstrip().endswith("---"):
            updated_content = file_content.rstrip() + "\n\n" + new_slide
        else:
            updated_content = file_content.rstrip() + "\n\n---\n\n" + new_slide
    else:
        # Insert at specific position
        if slide_position < 1:
            slide_position = 1

        # Reconstruct the file with the new slide inserted
        parts = []
        for i, slide in enumerate(slides):
            if i + 1 == slide_position:
                parts.append(new_slide)
            parts.append(slide)

        updated_content = "\n---\n".join(parts)

    return updated_content


if __name__ == "__main__":
    print("Slidev Tools Module")
    print("==================")
    print("\nAvailable functions:")
    print("  - parse_slides(content)")
    print("  - get_slide_content(content, slide_number)")
    print("  - update_element_content(content, slide_number, element_id, new_content)")
    print("  - update_element_color(content, slide_number, element_id, color)")
    print("  - update_slide_background(content, slide_number, background_color)")
    print("  - create_new_slide(content, position, title, content, background, layout)")
    print("\nImport this module to use these functions in your code.")