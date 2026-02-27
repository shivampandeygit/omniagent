import json
import os
from datetime import datetime
from rich.console import Console

console = Console()

class MemoryManager:
    def __init__(self, memory_file: str = "memory/agent_memory.json"):
        self.memory_file = memory_file
        self.short_term = []  # Current session
        self.long_term = {}   # Persistent across sessions
        self.load_memory()
    
    def load_memory(self):
        """Load memory from file"""
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, 'r') as f:
                    data = json.load(f)
                    self.long_term = data.get("long_term", {})
                console.print(f"[dim]🧠 Memory loaded: {len(self.long_term)} memories[/dim]")
            except:
                self.long_term = {}
    
    def save_memory(self):
        """Save memory to file"""
        os.makedirs(os.path.dirname(self.memory_file), exist_ok=True)
        with open(self.memory_file, 'w') as f:
            json.dump({"long_term": self.long_term}, f, indent=2)
    
    def add_short_term(self, role: str, content: str):
        """Add to current session memory"""
        self.short_term.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
    
    def remember(self, key: str, value: str):
        """Store important info permanently"""
        self.long_term[key] = {
            "value": value,
            "timestamp": datetime.now().isoformat()
        }
        self.save_memory()
        console.print(f"[dim]💾 Remembered: {key}[/dim]")
    
    def recall(self, key: str) -> str:
        """Recall specific memory"""
        if key in self.long_term:
            return self.long_term[key]["value"]
        return None
    
    def get_context(self) -> str:
        """Get all long term memories as context"""
        if not self.long_term:
            return "No previous memories."
        
        context = "Previous memories:\n"
        for key, val in self.long_term.items():
            context += f"- {key}: {val['value']}\n"
        return context
    
    def get_short_term(self, last_n: int = 10) -> list:
        """Get recent conversation history"""
        return self.short_term[-last_n:]
    
    def clear_short_term(self):
        """Clear current session"""
        self.short_term = []
