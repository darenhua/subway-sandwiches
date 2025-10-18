"""
Slide-specific tools for working with Slidev presentations via the Claude Agent SDK.
"""

from claude_agent_sdk import (
    AssistantMessage,
    TextBlock,
    ResultMessage,
    ToolUseBlock,
    ToolResultBlock,
    ThinkingBlock,
    UserMessage,
    Message,
    SystemMessage,
)
from rich import print
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.console import Console
from rich.prompt import Prompt
from rich.syntax import Syntax
from dotenv import load_dotenv
from typing import Literal, Optional, Tuple, List
import argparse
import json
import re

load_dotenv()


# --------------------------------
# Parse runtime args from CLI
# --------------------------------

parser = argparse.ArgumentParser()
parser.add_argument("--stats", "-s", default="False", help="Print session stats")
parser.add_argument("--model", "-m", default="sonnet", help="Model to use")
parser.add_argument(
    "--output-style", "-os", default="Personal Assistant", help="Output style to use"
)
parser.add_argument("--print-raw", "-pr", default="False", help="Print raw messages")


# --------------------------------
# Convenience functions for printing messages
# --------------------------------


def print_rich_message(
    type: Literal["user", "assistant", "tool_use", "tool_result", "system"],
    message: str,
    console: Console,
):
    """
    Prints a message in a panel with a title and border color based on the message type.
    """
    styles = {
        "user": {
            "message_style": "bold yellow",
            "panel_title": "User Prompt",
            "border_style": "yellow",
        },
        "assistant": {
            "message_style": "bold green",
            "panel_title": "Assistant",
            "border_style": "green",
        },
        "tool_use": {
            "message_style": "bold blue",
            "panel_title": "Tool Use",
            "border_style": "blue",
        },
        "tool_result": {
            "message_style": "bold magenta",
            "panel_title": "Tool Result",
            "border_style": "magenta",
        },
        "system": {
            "message_style": "bold cyan",
            "panel_title": "System Message",
            "border_style": "cyan",
        },
    }

    # For tool results, try to apply JSON syntax highlighting
    if type == "tool_result" and is_json_string(message):
        panel_content = Syntax(message, "json", theme="monokai", line_numbers=False)
    else:
        panel_content = Text(message, style=styles[type]["message_style"])

    if type == "system":
        panel = Panel.fit(
            panel_content,
            title=styles[type]["panel_title"],
            border_style=styles[type]["border_style"],
        )
    else:
        panel = Panel(
            panel_content,
            title=styles[type]["panel_title"],
            border_style=styles[type]["border_style"],
        )
    console.print(panel, end="\n\n")


def is_json_string(text: str) -> bool:
    """Check if a string is valid JSON"""
    try:
        json.loads(text)
        return True
    except json.JSONDecodeError:
        return False


def format_tool_result(content) -> str:
    """
    Format tool result content nicely, handling nested JSON strings.
    """
    if isinstance(content, str):
        # Try to parse as JSON and format it
        try:
            parsed = json.loads(content)
            return json.dumps(parsed, indent=2)
        except json.JSONDecodeError:
            return content
    elif isinstance(content, list):
        # Handle list of content blocks (common format)
        formatted_parts = []
        for item in content:
            if isinstance(item, dict) and "text" in item:
                # Try to parse the text field as JSON
                text_content = item["text"]
                try:
                    parsed_json = json.loads(text_content)
                    formatted_json = json.dumps(parsed_json, indent=2)
                    formatted_parts.append(formatted_json)
                except json.JSONDecodeError:
                    # If not JSON, just use the text as-is
                    formatted_parts.append(text_content)
            else:
                # For other dict structures, format as JSON
                formatted_parts.append(json.dumps(item, indent=2))
        return "\n\n".join(formatted_parts)
    else:
        # For other types, convert to JSON
        return json.dumps(content, indent=2)


def get_user_input(console: Console) -> str:
    """
    Get user input and display it in a rich panel in one step.
    Returns the user input string.
    """
    user_input = Prompt.ask("\n[bold yellow]You[/bold yellow]", console=console)
    print()
    return user_input


# --------------------------------
# Slidev-specific tools for presentations
# --------------------------------


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


def parse_and_print_message(
    message: Message, console: Console, print_stats: bool = False
):
    """
    Parse and print a message based on its type and content.
    """
    # Assistant messages include TextBlock, ToolUseBlock, ThinkingBlock, and ToolResultBlock
    # https://docs.claude.com/en/api/agent-sdk/python#content-block-types
    if isinstance(message, SystemMessage):
        if message.subtype == "compact_boundary":
            print_rich_message(
                "system",
                f"Compaction completed \nPre-compaction tokens: {message.data["compact_metadata"]["pre_tokens"]} \nTrigger: {message.data["compact_metadata"]["trigger"]}",
                console,
            )
        else:
            print_rich_message("system", json.dumps(message.data, indent=2), console)
    elif isinstance(message, AssistantMessage):
        for block in message.content:
            if isinstance(block, TextBlock):
                print_rich_message("assistant", block.text, console)
            elif isinstance(block, ToolUseBlock):
                print_rich_message(
                    "tool_use", f"Tool: <{block.name}> \n\n {block.input}", console
                )
            elif isinstance(block, ThinkingBlock):
                print_rich_message("assistant", "Thinking...", console)
    elif isinstance(message, UserMessage):
        for block in message.content:
            if isinstance(block, ToolResultBlock):
                formatted_content = format_tool_result(block.content)
                print_rich_message("tool_result", formatted_content, console)
    elif isinstance(message, ResultMessage):

        if print_stats:
            result = message.subtype
            session_id = message.session_id
            duration_s = message.duration_ms / 1000
            cost_usd = message.total_cost_usd
            input_tokens = message.usage["input_tokens"]
            output_tokens = message.usage["output_tokens"]

            session_stats = {
                "Session ID": session_id,
                "Result": result,
                "Duration (s)": f"{duration_s:.2f}",
                "Cost (USD)": f"${cost_usd:.2f}" if cost_usd else "N/A",
                "Input Tokens": input_tokens,
                "Output Tokens": output_tokens,
            }

            if session_stats:
                stats_table = Table(
                    title="Session Stats", show_header=False, title_style="bold blue"
                )
                stats_table.add_column(style="cyan", no_wrap=True)
                stats_table.add_column(style="yellow")

                for stat_name, stat_value in session_stats.items():
                    stats_table.add_row(stat_name, str(stat_value))

                console.print(stats_table, end="\n")
