import os
from google import genai
from google.genai import types
from typing import List, Optional
from .orchestrator import sequential_workflow, loop_workflow, parallel_workflow
from .memory import MemoryManager
import uuid

class RouterAgent:
    def __init__(self, thread_id: str = None):
        self.client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
        self.model_id = "gemini-2.5-flash"
        self.memory = MemoryManager()
        self.thread_id = thread_id or str(uuid.uuid4())
        
        self.system_instruction = """
        You are the Chief AI Software Engineer and Router. Your job is to analyze the user's request and decide which specialized workflow to trigger.
        
        Workflows available (you don't call them as Python functions yourself, but you describe which one you are choosing):
        1. 'sequential_workflow': Best for standard implementation tasks. (Architect -> Developer).
        2. 'loop_workflow': Best for critical code, bug fixes, or complex refactoring that needs validation. (Developer <-> Reviewer loop).
        3. 'parallel_workflow': Best for analyzing multiple files or metrics at once. (Parallel Analyzer).
        
        You have internal access to these workflows. When the user asks a question, determine the intent and explain which agentic strategy you are using to solve it.
        """

    async def initialize(self):
        await self.memory.initialize()
        await self.memory.create_thread(self.thread_id)

    async def chat(self, user_input: str) -> str:
        # Save user message to memory
        await self.memory.add_message(self.thread_id, "user", user_input)
        
        # Get history for context
        history = await self.memory.get_messages(self.thread_id)
        
        # In a more advanced implementation using the ADK 'Agent-as-Tool' pattern, 
        # the Router would have functions like `refactor_code` which internally calls `loop_workflow`.
        # For this demonstration, we'll use a logic block to route.
        
        # Logic-based routing for the demo
        if any(word in user_input.lower() for word in ["refactor", "fix", "critical", "loop"]):
            result = await loop_workflow(user_input)
        elif any(word in user_input.lower() for word in ["analyze", "complexity", "multiple", "parallel"]):
            # Simple heuristic to extract files if any
            files = [word for word in user_input.split() if "." in word]
            if not files: files = ["app/agents.py"] # Default for demo
            result_dict = await parallel_workflow(files)
            result = str(result_dict)
        else:
            result = await sequential_workflow(user_input)
            
        # Save assistant response to memory
        await self.memory.add_message(self.thread_id, "assistant", result)
        
        return result
