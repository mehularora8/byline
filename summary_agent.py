import logging
import json
from typing import Dict, Any
from openai import OpenAI
from exa import ExaSearch
from models import UserInterest

class ExecutiveSummaryAgent:
    """LLM agent using OpenAI GPT-4 with function calling"""
    
    def __init__(self, openai_api_key: str, exa_api_key: str):
        self.client = OpenAI(api_key=openai_api_key)
        self.model = "gpt-4.1"
        self.exa_search = ExaSearch(exa_api_key)
        logging.info(f"ExecutiveSummaryAgent initialized with OpenAI API key: {openai_api_key[:8]}...")
        
        # Define the Exa search tool
        self.tools = [{
            "type": "function",
            "name": "search_web",
            "description": "Search the web for information using Exa search API",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query to find relevant information"
                    },
                    "num_results": {
                        "type": "integer",
                        "description": "Number of results to return (default: 3)",
                        "default": 3
                    }
                },
                "required": ["query"]
            }
        }]
    
    def search_web(self, query: str, num_results: int = 3) -> Dict[str, Any]:
        """Function to be called by the LLM agent"""
        logging.info(f"search_web function called with query: '{query}', num_results: {num_results}")
        result = self.exa_search.search(query, num_results)
        logging.info(f"search_web function completed successfully")
        return result
    
    def create_executive_summary(self, user_interest: UserInterest) -> str:
        """Chat with the agent using function calling for search"""
        logging.info(f"create_executive_summary called with user_interest: {user_interest}")
        
        # Create system message with user interests context
        prompt_message = f"""Your job is to provide the user an executive summary to keep on top of their interests in the last day. 
        
        ## User Interests
        The user has the following interests, with interests in these specific keywords, and likes the following domains:
        {user_interest.to_dict()}.

        You should try to find information on the user's domains, but that is not an exhaustive list of domains you should search.
        
        ## Functions
        You will use the search_web function to find relevant information and provide helpful responses based on their interests.

        ## Output
        Your response should contain all the interests in the user_interest object, with 1-3 bullet points if information is available. 
        Your tone should be authoritative and informative. Keep it short and concise.
        
        ## Output Format
        Respond in HTML format. For each topic, you should have a heading and a list of bullet points.
        <h3>TOPIC</h3>
        <ul>
            <li>1-3 bullet points about this topic if information is available.</li>
            <li>If no information is available, say "No information available"</li>
        </ul>
        """
        
        messages = [
            {"role": "user", "content": prompt_message}
        ]
    
        
        logging.info(f"Calling OpenAI API with model: {self.model}")
        response = self.client.responses.create(    
            model=self.model,
            input=messages,
            tools=self.tools,
        )
        
        logging.info(f"OpenAI API response received: {response}")
        
        # Handle tool calls if any
        output = response.output

        for message in output:
            if message.type == "function_call":
                logging.info(f"Tool calls detected.")
                # Add assistant message to conversation
                messages.append(message)
            
                logging.info(f"Processing tool call: {message.name}")
                if message.name == "search_web":
                    # Parse function arguments
                    function_args = json.loads(message.arguments)
                    query = function_args.get("query")
                    num_results = function_args.get("num_results", 3)
                    
                    logging.info(f"Executing search_web with args: {function_args}")
                    
                    # Execute search
                    search_results = self.search_web(query, num_results)
                    
                    # Add tool response
                    messages.append({
                        "call_id": message.call_id,
                        "type": "function_call_output",
                        "output": json.dumps(search_results)
                    })
            elif message.type == "text":
                logging.info(f"Text message received: {message.text}")
                messages.append(message)
            
        # Get final response
        logging.info("Getting final response from OpenAI API")
        final_response = self.client.responses.create(
            model=self.model,
            input=messages
        )
        
        result = final_response.output_text
        logging.info(f"Final response generated successfully")
        return result
    
    def process_interests_and_query(self, user_interest: UserInterest) -> str:
        """Process user interests and query using function calling"""
        return self.create_executive_summary(user_interest)
