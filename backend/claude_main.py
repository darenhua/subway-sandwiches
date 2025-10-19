import asyncio
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions, create_sdk_mcp_server
from rich.console import Console
from cli_tools import print_rich_message, parse_and_print_message, get_user_input
from dotenv import load_dotenv

# from slidev_tools import (
#     update_element_content,
#     update_element_color,
#     update_slide_background,
#     create_new_slide,
# )

console = Console()
load_dotenv()


async def main():
    # slidev_server = create_sdk_mcp_server(
    #     name="slidev",
    #     version="1.0.0",
    #     tools=[
    #         update_element_content,
    #         update_element_color,
    #         update_slide_background,
    #         create_new_slide,
    #     ],
    # )

    model = "opus"
    options = ClaudeAgentOptions(
        model=model,
        cwd="./test-client/slides",
        allowed_tools=[
            "Read",
            "Write",
            "Edit",
            "WebFetch",
            "MultiEdit",
            "Grep",
            "Glob",
            # Notice that you MUST allow MCP tools otherwise they will not be available by default.
            # "mcp__slidev__update_element_content",
            # "mcp__slidev__update_element_color",
            # "mcp__slidev__update_slide_background",
            # "mcp__slidev__create_new_slide",
        ],
        permission_mode="acceptEdits",
        setting_sources=["project"],
    )

    print_rich_message(
        "system",
        f"Welcome to your personal assistant, Kaya!\n\nSelected model: {model}",
        console,
    )

    async with ClaudeSDKClient(options=options) as client:
        # run slash command to create implementation plan

        while True:
            input_prompt = get_user_input(console)
            if input_prompt == "exit":
                break

            await client.query(input_prompt)

            async for message in client.receive_response():
                parse_and_print_message(message, console)


if __name__ == "__main__":
    asyncio.run(main())
