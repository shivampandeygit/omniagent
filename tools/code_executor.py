import subprocess
import sys
import os
import tempfile
from rich.console import Console

console = Console()

class CodeExecutorTool:
    def __init__(self):
        self.name = "code_executor"
        self.description = "Write and execute Python code"
    
    def run(self, code: str) -> str:
        console.print("[dim]⚡ Executing code...[/dim]")
        
        try:
            # Temp file mein code save karo
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(code)
                temp_file = f.name
            
            # Code run karo
            result = subprocess.run(
                [sys.executable, temp_file],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            os.unlink(temp_file)
            
            if result.returncode == 0:
                return f"✅ Code executed successfully!\nOutput:\n{result.stdout}"
            else:
                return f"❌ Error:\n{result.stderr}"
                
        except subprocess.TimeoutExpired:
            return "❌ Code execution timed out (30s limit)"
        except Exception as e:
            return f"❌ Execution failed: {str(e)}"
