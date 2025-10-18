#!/usr/bin/env python3
"""
Test script to demonstrate the Slidev-specific tools functionality.
"""

from slidev_tools import (
    update_element_content,
    update_element_color,
    update_slide_background,
    create_new_slide,
    parse_slides,
    get_slide_content
)

# Sample Slidev markdown content
sample_slidev_content = """# Welcome to My Presentation

<p id="intro-text">This is the introduction slide</p>

<div id="main-content">
  Learn about amazing things
</div>

---

# Second Slide

<h2 id="subtitle">Key Features</h2>

<ul id="feature-list">
  <li>Feature 1</li>
  <li>Feature 2</li>
  <li>Feature 3</li>
</ul>

---

---
layout: center
---

# Third Slide

<p id="centered-text">This is centered content</p>

---

# Fourth Slide

<div id="code-example">
  This slide has code examples
</div>

<style>
#code-example {
  font-family: monospace;
}
</style>
"""


def test_parse_slides():
    """Test parsing slides from markdown."""
    print("Testing: parse_slides()")
    slides = parse_slides(sample_slidev_content)
    print(f"Found {len(slides)} slides\n")
    for i, slide in enumerate(slides, 1):
        print(f"Slide {i} preview: {slide[:50]}...")
    print("\n" + "="*50 + "\n")


def test_get_slide_content():
    """Test getting specific slide content."""
    print("Testing: get_slide_content()")
    slide_content, start, end = get_slide_content(sample_slidev_content, 2)
    print(f"Slide 2 content:\n{slide_content}\n")
    print(f"Position in file: {start} to {end}")
    print("\n" + "="*50 + "\n")


def test_update_element_content():
    """Test updating element content."""
    print("Testing: update_element_content()")
    print("Original intro text: 'This is the introduction slide'")

    updated_content = update_element_content(
        sample_slidev_content,
        slide_number=1,
        element_id="intro-text",
        new_content="Welcome to our amazing Slidev presentation!"
    )

    # Extract and show the updated part
    slides = parse_slides(updated_content)
    print(f"Updated intro text in slide 1:\n{slides[0][:200]}")
    print("\n" + "="*50 + "\n")


def test_update_element_color():
    """Test updating element color."""
    print("Testing: update_element_color()")
    print("Adding red color to 'subtitle' element on slide 2")

    updated_content = update_element_color(
        sample_slidev_content,
        slide_number=2,
        element_id="subtitle",
        color="#FF0000"
    )

    # Extract and show the updated slide
    slides = parse_slides(updated_content)
    print(f"Updated slide 2 with color style:\n{slides[1]}")
    print("\n" + "="*50 + "\n")


def test_update_slide_background():
    """Test updating slide background."""
    print("Testing: update_slide_background()")
    print("Setting blue background for slide 1")

    updated_content = update_slide_background(
        sample_slidev_content,
        slide_number=1,
        background_color="#0066CC"
    )

    # Extract and show the updated slide
    slides = parse_slides(updated_content)
    print(f"Updated slide 1 with background:\n{slides[0]}")
    print("\n" + "="*50 + "\n")


def test_create_new_slide():
    """Test creating a new slide."""
    print("Testing: create_new_slide()")
    print("Creating a new slide at position 2")

    updated_content = create_new_slide(
        sample_slidev_content,
        slide_position=2,
        title="New Inserted Slide",
        content='<p id="new-content">This is a newly inserted slide with some content</p>',
        background="#FFCC00",
        layout="center"
    )

    # Show the total number of slides
    slides = parse_slides(updated_content)
    print(f"Total slides after insertion: {len(slides)}")
    print(f"\nNew slide at position 2:\n{slides[1]}")
    print("\n" + "="*50 + "\n")


def test_complex_scenario():
    """Test a complex scenario with multiple operations."""
    print("Testing: Complex scenario with multiple operations")
    print("1. Adding a new slide")
    print("2. Updating element content")
    print("3. Changing element color")
    print("4. Setting slide background")

    # Start with original content
    content = sample_slidev_content

    # 1. Add a new slide at the end
    content = create_new_slide(
        content,
        title="Conclusion",
        content='<p id="conclusion-text">Thank you for watching!</p>',
        layout="center"
    )

    # 2. Update the conclusion text
    content = update_element_content(
        content,
        slide_number=5,  # New slide is now slide 5
        element_id="conclusion-text",
        new_content="Thank you for watching this amazing presentation!"
    )

    # 3. Make the conclusion text green
    content = update_element_color(
        content,
        slide_number=5,
        element_id="conclusion-text",
        color="#00FF00"
    )

    # 4. Set a dark background for the conclusion slide
    content = update_slide_background(
        content,
        slide_number=5,
        background_color="#1a1a1a"
    )

    # Show the final conclusion slide
    slides = parse_slides(content)
    print(f"\nFinal conclusion slide:\n{slides[-1]}")
    print("\n" + "="*50 + "\n")


def save_example_presentation():
    """Save an example presentation file."""
    print("Creating example presentation file: example_presentation.md")

    # Create a complete presentation
    content = """# My Amazing Presentation

<p id="title-subtitle">Built with Slidev and Python Tools</p>

---

# Introduction

<div id="intro-section">
  <p id="intro-p1">Welcome to this demonstration</p>
  <p id="intro-p2">We'll explore amazing features</p>
</div>

---

---
background: "#2c3e50"
---

# Features

<ul id="features">
  <li>Easy slide creation</li>
  <li>Dynamic content updates</li>
  <li>CSS styling support</li>
</ul>

<style>
#features {
  color: white;
}
</style>

---

# Code Example

<div id="code-block">
```python
def hello_world():
    print("Hello, Slidev!")
```
</div>

---

---
layout: center
background: "#e74c3c"
---

# Thank You!

<p id="contact">Contact: example@email.com</p>

<style>
#contact {
  color: white;
  font-size: 24px;
}
</style>
"""

    with open("example_presentation.md", "w") as f:
        f.write(content)

    print("Saved example_presentation.md")
    print("\nYou can now use the slide tools to modify this presentation!")
    print("\nExample usage:")
    print('  content = open("example_presentation.md").read()')
    print('  updated = update_element_content(content, 1, "title-subtitle", "New subtitle!")')
    print('  updated = update_slide_background(updated, 1, "#3498db")')
    print("\n" + "="*50 + "\n")


if __name__ == "__main__":
    print("="*50)
    print("Testing Slidev-specific Tools")
    print("="*50 + "\n")

    # Run all tests
    test_parse_slides()
    test_get_slide_content()
    test_update_element_content()
    test_update_element_color()
    test_update_slide_background()
    test_create_new_slide()
    test_complex_scenario()
    save_example_presentation()

    print("All tests completed!")