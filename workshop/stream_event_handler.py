from typing import Any

from azure.ai.projects.aio import AIProjectClient
from azure.ai.projects.models import (
    AsyncAgentEventHandler,
    AsyncFunctionTool,
    MessageDeltaChunk,
    MessageStatus,
    RunStep,
    RunStepDeltaChunk,
    RunStepStatus,
    ThreadMessage,
    ThreadRun,
)

from utilities.utilities import Utilities


class StreamEventHandler(AsyncAgentEventHandler[str]):
    """Handle LLM streaming events and tokens."""

    def __init__(self, functions: AsyncFunctionTool, project_client: AIProjectClient, utilities: Utilities = None) -> None:
        self.functions = functions
        self.project_client = project_client
        self.util = utilities
        super().__init__()

    async def on_message_delta(self, delta: MessageDeltaChunk) -> None:
        """Handle message delta events. This will be the streamed token"""
        if self.util:
            self.util.log_token_blue(delta.text)
        else:
            print(delta.text, end="", flush=True)

    async def on_thread_message(self, message: ThreadMessage) -> None:
        """Handle thread message events."""
        if self.util:
            await self.util.get_files(message, self.project_client)

    async def on_thread_run(self, run: ThreadRun) -> None:
        """Handle thread run events"""
        if run.status == "failed":
            print(f"❌ Run failed. Error: {run.last_error}")

    async def on_run_step(self, step: RunStep) -> None:
        pass

    async def on_run_step_delta(self, delta: RunStepDeltaChunk) -> None:
        pass

    async def on_error(self, data: str) -> None:
        print(f"⚠️ An error occurred. Data: {data}")

    async def on_done(self) -> None:
        pass

    async def on_unhandled_event(self, event_type: str, event_data: Any) -> None:
        print(f"📎 Unhandled Event Type: {event_type}")
