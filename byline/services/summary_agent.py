import logging
import json
from typing import Dict, Any
from openai import OpenAI
from .arxiv_tools import ArxivTools
from byline.models.user_models import UserInterest
from byline.services.templates.agent_prompt import generate_agent_prompt

class ExecutiveSummaryAgent:
    """LLM agent using OpenAI GPT-4 with function calling"""
    
    def __init__(self, openai_api_key: str):
        self.client = OpenAI(api_key=openai_api_key)
        self.model = "gpt-4.1"
        self.arxiv_tools = ArxivTools()
        logging.info(f"ExecutiveSummaryAgent initialized with OpenAI API key: {openai_api_key[:8]}...")
        
        self.tools = [
            {
                "type": "function",
                "name": "search_arxiv_papers",
                "description": "Search arXiv for academic papers within a specified time interval",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Search query to find relevant papers"
                        },
                        "days_back": {
                            "type": "integer",
                            "description": "Number of days to search back from today (default: 1)",
                            "default": 1
                        },
                        "max_results": {
                            "type": "integer",
                            "description": "Maximum number of results to return (default: 10)",
                            "default": 10
                        }
                    },
                    "required": ["query"]
                }
            }
        ]
    
    def search_arxiv_papers(self, query: str, days_back: int = 1, max_results: int = 10) -> Dict[str, Any]:
        """Function to search arXiv papers"""
        logging.info(f"search_arxiv_papers function called with query: '{query}', days_back: {days_back}, max_results: {max_results}")
        result = self.arxiv_tools.search_papers_by_time_interval(query, days_back, max_results)
        logging.info(f"search_arxiv_papers function completed successfully")
        return result
    
    def create_executive_summary(self, user_interest: UserInterest) -> str:
        """Chat with the agent using function calling for search"""
        logging.info(f"create_executive_summary called with user_interest: {user_interest}")
        
        prompt_message = generate_agent_prompt(user_interest)
        
        messages = [
            {"role": "user", "content": prompt_message}
        ]

        response = None
        should_continue = True

        while should_continue:
            
            response = self.client.responses.create(    
                model=self.model,
                input=messages,
                tools=self.tools,
            )
            
            # Handle tool calls if any
            output = response.output
            has_function_calls = False

            for message in output:
                if message.type == "function_call":
                    has_function_calls = True
                    logging.info(f"Tool calls detected.")
                    messages.append(message)
                
                    logging.info(f"Processing tool call: {message.name}")
                    if message.name == "search_arxiv_papers":
                        function_args = json.loads(message.arguments)
                        query = function_args.get("query")
                        days_back = function_args.get("days_back", 30)
                        max_results = function_args.get("max_results", 10)
                        
                        logging.info(f"Executing search_arxiv_papers with args: {function_args}")
                        
                        search_results = self.search_arxiv_papers(query, days_back, max_results)
                        
                        messages.append({
                            "call_id": message.call_id,
                            "type": "function_call_output",
                            "output": json.dumps(search_results)
                        })
                        
                    elif message.name == "download_and_read_arxiv_paper":
                        function_args = json.loads(message.arguments)
                        paper_id = function_args.get("paper_id")
                        
                        logging.info(f"Executing download_arxiv_paper with args: {function_args}")
                        paper_results = self.download_and_read_arxiv_paper(paper_id)
                        
                        messages.append({
                            "call_id": message.call_id,
                            "type": "function_call_output", 
                            "output": json.dumps(paper_results)
                        })  
                
                elif message.type == "text":
                    logging.info(f"Text message received: {message.text}")
                    messages.append(message)
            
            should_continue = has_function_calls

            if not should_continue:
                break
        
        result = response.output_text
        logging.info(f"Final response generated")
        return result
    
    def process_interests_and_query(self, user_interest: UserInterest) -> str:
        """Process user interests and query using function calling"""
        return self.create_executive_summary(user_interest)
