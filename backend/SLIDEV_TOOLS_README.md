# Slidev-Specific Tools Documentation

## Overview

I've created a comprehensive set of slide-specific tools for working with Slidev presentations. These tools allow a slides assistant agent to programmatically modify markdown files that represent Slidev presentations.

## Files Created

### 1. `cli_tools.py`
- Main file with Claude Agent SDK integration
- Contains slide-specific tools that can be used by an agent
- Includes the original CLI helper functions

### 2. `slidev_tools.py`
- Standalone module with all slide manipulation functions
- Can be imported and used independently without SDK dependencies
- Core implementation of all slide tools

### 3. `slides_assistant.py`
- Example assistant class that demonstrates how to use the tools
- Provides a high-level interface for slide operations
- Includes command processing for common slide tasks

### 4. `test_slide_tools.py`
- Comprehensive test suite demonstrating all tool capabilities
- Includes examples of each tool function
- Creates sample presentations for testing

## Available Tools

### 1. **update_element_content**
Updates the text content of a specific element within a slide.

**Parameters:**
- `file_content`: The full markdown file content
- `slide_number`: The slide number (1-indexed)
- `element_id`: The ID of the element to update
- `new_content`: The new text content

**Example:**
```python
content = update_element_content(
    file_content,
    slide_number=1,
    element_id="intro-text",
    new_content="Welcome to our presentation!"
)
```

### 2. **update_element_color**
Updates the color of a text element using CSS styles.

**Parameters:**
- `file_content`: The full markdown file content
- `slide_number`: The slide number (1-indexed)
- `element_id`: The ID of the element to style
- `color`: The color value (e.g., "red", "#FF0000")

**Example:**
```python
content = update_element_color(
    file_content,
    slide_number=2,
    element_id="title",
    color="#3498db"
)
```

### 3. **update_slide_background**
Sets or updates the background color of a specific slide.

**Parameters:**
- `file_content`: The full markdown file content
- `slide_number`: The slide number (1-indexed)
- `background_color`: The background color

**Example:**
```python
content = update_slide_background(
    file_content,
    slide_number=1,
    background_color="#2c3e50"
)
```

### 4. **create_new_slide**
Creates a new slide in the presentation.

**Parameters:**
- `file_content`: The full markdown file content
- `slide_position`: Position to insert (None = append at end)
- `title`: Optional slide title
- `content`: Optional slide content
- `background`: Optional background color
- `layout`: Slide layout (default, center, etc.)

**Example:**
```python
content = create_new_slide(
    file_content,
    slide_position=2,
    title="New Feature",
    content='<p id="feature">Amazing feature!</p>',
    background="#3498db",
    layout="center"
)
```

### 5. **parse_slides**
Parses markdown content into individual slides.

**Parameters:**
- `content`: The full markdown content

**Returns:**
- List of slide contents

### 6. **get_slide_content**
Gets the content and position of a specific slide.

**Parameters:**
- `content`: The full markdown content
- `slide_number`: The slide number (1-indexed)

**Returns:**
- Tuple of (slide_content, start_index, end_index)

## Key Features

1. **Deterministic Element Targeting**: Tools use element IDs to precisely target text blocks
2. **CSS Style Injection**: Automatically adds or updates `<style>` blocks within slides
3. **Frontmatter Management**: Handles Slidev frontmatter for backgrounds and layouts
4. **Slide Delimiter Parsing**: Correctly handles `---` slide separators
5. **HTML Element Support**: Works with both HTML elements and markdown with IDs

## Usage Patterns

### For Text Updates
```markdown
<p id="intro-text">Old text</p>
<!-- Can be updated by targeting "intro-text" ID -->
```

### For Color Styling
```markdown
<h1 id="main-title">Title</h1>
<!-- Tool will add/update CSS: #main-title { color: red; } -->
```

### For Backgrounds
```markdown
---
background: "#2c3e50"
---
# Slide with dark background
```

## Testing

Run the test suite to see all tools in action:

```bash
python3 test_slide_tools.py
```

This will:
- Parse slides
- Update element content
- Change element colors
- Set slide backgrounds
- Create new slides
- Generate example presentations

## Example Assistant Usage

```python
from slides_assistant import SlidesAssistant

# Create assistant with presentation file
assistant = SlidesAssistant("my_presentation.md")

# List all slides
result = assistant.process_command({
    "action": "list_slides"
})

# Update text on slide 1
result = assistant.process_command({
    "action": "update_text",
    "params": {
        "slide_number": 1,
        "element_id": "title",
        "new_text": "New Title!"
    }
})

# Change color of element
result = assistant.process_command({
    "action": "change_color",
    "params": {
        "slide_number": 1,
        "element_id": "title",
        "color": "#e74c3c"
    }
})
```

## Integration with Claude Agent SDK

The tools in `cli_tools.py` are ready to be used by a Claude Agent. They follow the pattern of taking file content as input and returning modified content, making them suitable for agent-based slide editing workflows.

## Note on Slidev Syntax

The tools support standard Slidev features:
- Slide delimiters (`---`)
- Frontmatter (YAML between `---` markers)
- HTML elements with IDs
- Scoped `<style>` blocks
- Standard CSS properties

The tools specifically avoid MDC syntax and focus on standard CSS approaches as requested.