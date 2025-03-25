from src.agents.llm import LLM
class ReflectionAgent:
    """
    Reflection Agent
    
    """
    def __init__(self,query):
        
        self.query = query
        
    
    def generate(self, query):
        """
        """
        return LLM.generate(query)
    
    def get_reflection(self, query):
        """
        """
        return LLM.generate(query)
    
    def run_agent(self, query):
        """
        """
        return self.generate(query)