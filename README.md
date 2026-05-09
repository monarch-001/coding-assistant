# Multi-Agent AI Coding Assistant

A practical, technically strong multi-agent coding assistant built with **Google AI SDK (Gemini)** and Python. This project focuses on agentic orchestration, tool usage, and advanced workflow patterns.

## 🚀 Key Agentic Concepts Demonstrated

This project implements all mandatory Google ADK patterns:

1.  **First Agent:** Basic agentic implementation using the `google-genai` SDK.
2.  **Custom Tools:** Specialized Python tools for file I/O and AST-based code complexity analysis (`app/tools.py`).
3.  **Agent as Tool:** The **Router** agent manages specialized workflows (Sequential, Loop, Parallel) as higher-level tools.
4.  **Agent Memory:** Persistent conversation history using **SQLite** (`app/memory.py`), allowing context retention across CLI sessions.
5.  **Router Agent:** A chief orchestrator that analyzes user intent and selects the optimal agentic strategy (`app/router.py`).
6.  **Sequential Agent:** A multi-step flow where an **Architect** designs a plan and a **Developer** implements it (`app/orchestrator.py`).
7.  **Loop Agent:** A refinement cycle between a **Developer** and a **Reviewer** that continues until code quality standards are met (`app/orchestrator.py`).
8.  **Parallel Agent:** Simultaneous execution of code analysis tasks across multiple files using `asyncio.gather` (`app/orchestrator.py`).

## 🛠 Tech Stack

-   **LLM:** Gemini 2.5 Flash
-   **SDK:** `google-genai`
-   **CLI:** `rich` for professional terminal UI
-   **Database:** `aiosqlite` for persistent memory
-   **Analysis:** `ast` module for deterministic code complexity metrics

## ⚙️ Setup

1.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Configure Environment:**
    Create a `.env` file in the root directory:
    ```env
    GOOGLE_API_KEY=your_gemini_api_key_here
    ```

3.  **Run the Assistant:**
    ```bash
    python main.py
    ```

## 📖 Example Usage

-   **Sequential Task:** "Implement a Python class for a simple LRU cache."
-   **Loop/Refinement Task:** "Refactor this code for better performance and ensure it's critical: \[paste code]"
-   **Parallel Analysis:** "Analyze the complexity of multiple files: app/agents.py app/tools.py"

---
*Built as a showcase for Agentic AI Engineering principles.*
