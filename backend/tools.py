from claude_agent_sdk import (
    tool,
    create_sdk_mcp_server,
)
from rich import print
from rich.console import Console
from typing import Any, Optional
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


@tool(
    "edit",
    "Edit a file by replacing text strings",
    {
        "file_path": str,
        "old_string": str,
        "new_string": str,
        "replace_all": Optional[bool],
    },
)
async def edit_file_dangerously(args: dict[str, Any]) -> dict[str, Any]:
    """
    Edit a file by replacing text strings.
    """
    file_path = args["file_path"]
    old_string = args["old_string"]
    new_string = args["new_string"]
    replace_all = args.get("replace_all", False)

    try:
        path = Path(file_path)

        # Validate file exists
        if not path.exists():
            return {
                "content": [
                    {"type": "text", "text": f"Error: File not found: {file_path}"}
                ]
            }

        if not path.is_file():
            return {
                "content": [
                    {"type": "text", "text": f"Error: Path is not a file: {file_path}"}
                ]
            }

        # Read file content
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        # Count occurrences
        occurrences = content.count(old_string)

        if occurrences == 0:
            return {
                "content": [
                    {
                        "type": "text",
                        "text": f"No occurrences of '{old_string[:50]}{'...' if len(old_string) > 50 else ''}' found in file",
                    }
                ]
            }

        # Perform replacement
        if replace_all:
            new_content = content.replace(old_string, new_string)
            replacements_made = occurrences
        else:
            # Replace only first occurrence
            new_content = content.replace(old_string, new_string, 1)
            replacements_made = 1

        # Write back to file
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_content)

        # Create success message
        if replacements_made == 1:
            message = f"Successfully replaced 1 occurrence in {file_path}"
        else:
            message = (
                f"Successfully replaced {replacements_made} occurrences in {file_path}"
            )

        return {
            "content": [
                {
                    "type": "text",
                    "text": f"{message}\nReplacements made: {replacements_made}",
                }
            ]
        }

    except UnicodeDecodeError:
        return {
            "content": [
                {
                    "type": "text",
                    "text": f"Error: Cannot read file (not UTF-8): {file_path}",
                }
            ]
        }
    except Exception as e:
        return {"content": [{"type": "text", "text": f"Error editing file: {str(e)}"}]}


@tool(
    "edit",
    "Edit a only a specific element's content",
    {
        "file_path": str,
        "old_string": str,
        "new_string": str,
        "replace_all": Optional[bool],
    },
)
async def update_element_content(args: dict[str, Any]) -> dict[str, Any]:
    pass


@tool(
    "edit",
    "Update an element to have different color, size, background color, etc...",
    {
        "file_path": str,
        "old_string": str,
        "new_string": str,
        "replace_all": Optional[bool],
    },
)
async def update_element_styles(args: dict[str, Any]) -> dict[str, Any]:
    pass


