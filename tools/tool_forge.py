import os
import sys
import subprocess
import tempfile
from groq import Groq
from rich.console import Console

console = Console()

class ToolForge:
    def __init__(self, api_key: str):
        self.client = Groq(api_key=api_key)
        self.model = "llama-3.3-70b-versatile"
        self.custom_tools = {}
        self.tools_dir = "tools/custom"
        os.makedirs(self.tools_dir, exist_ok=True)
    
    def create_tool(self, tool_description: str) -> str:
        """Agent khud naya tool banayega"""
        console.print(f"[bold magenta]🔨 ToolForge: Creating new tool...[/bold magenta]")
        
        prompt = f"""Create a Python function for this task: {tool_description}

Rules:
- Write a complete working Python function
- Function name should be descriptive
- Add proper error handling
- Return the result as a string
- Only use standard Python libraries
- No external imports except: requests, json, os, datetime, math, random

Return ONLY the Python code, nothing else."""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}]
        )
        
        code = response.choices[0].message.content
        
        # Clean code
        if "```python" in code:
            code = code.split("```python")[1].split("```")[0].strip()
        elif "```" in code:
            code = code.split("```")[1].split("```")[0].strip()
        
        return code
    
    def save_and_run_tool(self, tool_name: str, code: str, input_data: str = "") -> str:
        """Tool save karo aur run karo"""
        try:
            # Tool file save karo
            tool_file = f"{self.tools_dir}/{tool_name}.py"
            
            # Runner code banao
            runner_code = f"""
{code}

# Auto run
import sys
input_data = '''{input_data}'''
# Find and call the main function
import inspect
functions = [(name, obj) for name, obj in globals().items() 
             if inspect.isfunction(obj) and not name.startswith('_')]
if functions:
    func_name, func = functions[0]
    try:
        if input_data:
            result = func(input_data)
        else:
            result = func()
        print(result)
    except Exception as e:
        try:
            result = func()
            print(result)
        except Exception as e2:
            print(f"Error: {{e2}}")
"""
            
            with open(tool_file, 'w') as f:
                f.write(runner_code)
            
            # Run karo
            result = subprocess.run(
                [sys.executable, tool_file],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0 and result.stdout:
                output = result.stdout.strip()
                # Tool save karo future use ke liye
                self.custom_tools[tool_name] = code
                console.print(f"[bold magenta]✅ Tool '{tool_name}' created and saved![/bold magenta]")
                return output
            else:
                return f"Tool output: {result.stderr}"
                
        except Exception as e:
            return f"ToolForge error: {str(e)}"
    
    def forge_and_run(self, task: str) -> str:
        """Main method — task ke liye tool banao aur run karo"""
        console.print(f"[bold magenta]⚡ ToolForge activated for: {task}[/bold magenta]")
        
        # Tool ka naam banao
        tool_name = "_".join(task.lower().split()[:3]).replace("-", "_")
        tool_name = ''.join(c if c.isalnum() or c == '_' else '' for c in tool_name)
        
        # Tool code generate karo
        code = self.create_tool(task)
        
        # Run karo
        result = self.save_and_run_tool(tool_name, code, task)
        
        return f"ToolForge created and ran a custom tool!\nResult: {result}"
