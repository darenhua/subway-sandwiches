import asyncio
from claude_agent_sdk import (
    ClaudeSDKClient,
    ClaudeAgentOptions,
)
from rich.console import Console
from cli_tools import print_rich_message, parse_and_print_message, get_user_input
from dotenv import load_dotenv

console = Console()
load_dotenv()


async def main():
    model = "sonnet"
    options = ClaudeAgentOptions(
        model=model,
        cwd="./test-client/slides",
        allowed_tools=[
            "Read",
            "Write",
            "Edit",
            "MultiEdit",
            "Grep",
            "Glob",
            # Notice that you MUST allow MCP tools otherwise they will not be available by default.
            # 'mcp__Playwright__browser_navigate'
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

        while True:
            input_prompt = get_user_input(console)
            if input_prompt == "exit":
                break

            await client.query(input_prompt)

            async for message in client.receive_response():
                parse_and_print_message(message, console)


if __name__ == "__main__":
    asyncio.run(main())
