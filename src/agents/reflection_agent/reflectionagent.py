from src.agents.llm import llm
class ReflectionAgent:
    """
    
    """
    def __init__(self,query):
        
        self.query = query
    
    def load_model(self):
        """
        """
        
        
        pass
    
    
    def predict(self, query):
        """
        """
    
    def get_reflection(self, query):
        """
        """
        return groq.execute(query)