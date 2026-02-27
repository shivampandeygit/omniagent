from groq import Groq
from tools.web_search import WebSearchTool
from tools.code_executor import CodeExecutorTool
from tools.tool_forge import ToolForge
from memory.memory_manager import MemoryManager
from rich.console import Console
from rich.panel import Panel
import os
from dotenv import load_dotenv
load_dotenv(override=True)

console = Console()

class OrchestratorAgent:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.client = Groq(api_key=self.api_key)
        self.model = "llama-3.3-70b-versatile"
        self.memory = MemoryManager()
        self.web_search = WebSearchTool()
        self.code_executor = CodeExecutorTool()
        self.tool_forge = ToolForge(api_key=self.api_key)
        self.system_prompt = """You are OmniAgent v4.0 — an advanced autonomous AI assistant.

You have access to these tools:

1. Web Search:
TOOL_CALL: web_search
QUERY: your search query

2. Code Executor:
TOOL_CALL: code_executor
CODE:
```python
your code here
```

3. Remember:
TOOL_CALL: remember
KEY: key_name
VALUE: actual_value

4. ToolForge (when no existing tool can do the job — CREATE a new tool!):
TOOL_CALL: tool_forge
TASK: describe what the tool should do

STRICT RULES:
- Use web_search for internet/current info
- Use code_executor for coding/calculations
- Use tool_forge when task needs something unique not covered by other tools
- Use remember for saving user info
- NEVER save wrong values in remember
- Think step by step always"""

    def parse_tool_call(self, response: str):
        if "TOOL_CALL: web_search" in response:
            for line in response.split("\n"):
                if line.startswith("QUERY:"):
                    return "web_search", line.replace("QUERY:", "").strip()
        
        if "TOOL_CALL: code_executor" in response:
            if "```python" in response:
                code = response.split("```python")[1].split("```")[0].strip()
                return "code_executor", code
        
        if "TOOL_CALL: remember" in response:
            lines = response.split("\n")
            key = value = None
            for line in lines:
                if line.startswith("KEY:"):
                    key = line.replace("KEY:", "").strip()
                if line.startswith("VALUE:"):
                    value = line.replace("VALUE:", "").strip()
            if key and value:
                return "remember", {"key": key, "value": value}
        
        if "TOOL_CALL: tool_forge" in response:
            for line in response.split("\n"):
                if line.startswith("TASK:"):
                    return "tool_forge", line.replace("TASK:", "").strip()
        
        return None, None

    def chat(self, user_message):
        self.memory.add_short_term("user", user_message)
        memory_context = self.memory.get_context()
        
        messages = [
            {"role": "system", "content": self.system_prompt + f"\n\n{memory_context}"},
            *[{"role": m["role"], "content": m["content"]} for m in self.memory.get_short_term()],
        ]
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages
        )
        
        assistant_message = response.choices[0].message.content
        tool_name, tool_input = self.parse_tool_call(assistant_message)
        
        if tool_name == "web_search":
            console.print("[bold yellow]⚡ Tool: Web Search[/bold yellow]")
            tool_result = self.web_search.run(tool_input)
        elif tool_name == "code_executor":
            console.print("[bold yellow]⚡ Tool: Code Executor[/bold yellow]")
            tool_result = self.code_executor.run(tool_input)
        elif tool_name == "remember":
            self.memory.remember(tool_input["key"], tool_input["value"])
            tool_result = f"Remembered: {tool_input['key']} = {tool_input['value']}"
        elif tool_name == "tool_forge":
            console.print("[bold magenta]⚡ Tool: ToolForge — Creating new tool![/bold magenta]")
            tool_result = self.tool_forge.forge_and_run(tool_input)
        else:
            tool_result = None
        
        if tool_result:
            messages.append({"role": "assistant", "content": assistant_message})
            messages.append({"role": "user", "content": f"Tool result:\n{tool_result}\n\nNow give final answer."})
            
            final_response = self.client.chat.completions.create(
                model=self.model,
                messages=messages
            )
            assistant_message = final_response.choices[0].message.content
        
        self.memory.add_short_term("assistant", assistant_message)
        return assistant_message

    def run(self):
        console.print(Panel.fit(
            "[bold cyan]🤖 OmniAgent v4.0[/bold cyan]\n[yellow]Web Search + Code + Memory + ToolForge![/yellow]\n[dim]Type 'exit' to quit[/dim]",
            border_style="cyan"
        ))
        
        while True:
            user_input = input("\n👤 You: ").strip()
            
            if user_input.lower() == "exit":
                console.print("[bold red]👋 OmniAgent shutting down...[/bold red]")
                break
                
            if not user_input:
                continue
            
            console.print("[dim]🤔 Thinking...[/dim]")
            response = self.chat(user_message=user_input)
            console.print(Panel(
                f"[bold green]🤖 OmniAgent:[/bold green]\n{response}",
                border_style="green"
            ))
