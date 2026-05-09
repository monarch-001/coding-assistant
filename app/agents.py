import os
from google import genai
from google.genai import types
from typing import List, Optional, Callable
from .tools import tools as available_tools
from dotenv import load_dotenv

load_dotenv()

class CodingAgent:
    def __init__(
        self, 
        name: str, 
        system_instruction: str, 
        model_id: str = "gemini-2.5-flash", 
        tools: Optional[List[Callable]] = None
    ):
        self.name = name
        self.client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
        self.model_id = model_id
        self.system_instruction = system_instruction
        self.tools = tools or []

    async def run(self, prompt: str, history: Optional[List[dict]] = None) -> str:
        config = types.GenerateContentConfig(
            system_instruction=self.system_instruction,
            tools=self.tools,
        )
        
        # Prepare chat history if provided
        contents = []
        if history:
            for msg in history:
                contents.append(types.Content(role=msg["role"], parts=[types.Part(text=msg["content"])]))
        
        contents.append(types.Part(text=prompt))
        
        # Note: In a real-world scenario, we'd handle tool calling loops manually or use the SDK's automatic tool handling.
        # For simplicity and to demonstrate 'Agent-as-Tool', we will use the Client's tool capability.
        response = self.client.models.generate_content(
            model=self.model_id,
            contents=contents,
            config=config
        )
        return response.text

# --- Agent Definitions ---

ARCHITECT_PROMPT = """
You are a Senior Software Architect. Your job is to analyze coding requirements and design a high-level technical plan.
Focus on:
1. Identifying necessary modules and classes.
2. Defining data structures.
3. Outlining the logic flow.
Output a clear, structured Markdown plan. Do not write actual code unless necessary for clarity.
"""

DEVELOPER_PROMPT = """
You are an Expert Software Developer. Your job is to implement or refactor code based on a technical plan.
Use the provided tools to read existing code and write the new implementation.
Focus on:
1. Writing clean, idiomatic Python code.
2. Handling edge cases.
3. Following the Architect's plan strictly.
"""

REVIEWER_PROMPT = """
You are a Senior Code Reviewer. Your job is to evaluate code for quality, security, and correctness.
Check for:
1. Adherence to PEP 8.
2. Logical bugs or security vulnerabilities.
3. Performance bottlenecks.
If the code has issues, provide specific feedback for the developer to fix. If it's perfect, say "APPROVED".
"""

ANALYZER_PROMPT = """
You are a Code Performance & Complexity Analyst. Your job is to analyze code using the provided complexity tools.
Provide a detailed report on the structure and health of the codebase.
"""

# Instantiate Agents
architect = CodingAgent("Architect", ARCHITECT_PROMPT)
developer = CodingAgent("Developer", DEVELOPER_PROMPT, tools=available_tools)
reviewer = CodingAgent("Reviewer", REVIEWER_PROMPT, tools=available_tools)
analyzer = CodingAgent("Analyzer", ANALYZER_PROMPT, tools=available_tools)
