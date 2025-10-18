"""
Reasoning Loop Module for Market Intelligence Research Agent.

This module implements the ReAct (Reasoning, Acting, Observing) loop for autonomous research.
"""
from typing import Dict, List, Any, Callable, Optional
import json
import time

class ReasoningLoop:
    """
    Implements the ReAct (Reasoning, Acting, Observing) loop for autonomous market research.
    Maintains working memory and manages tool calls in an iterative process.
    """
    
    def __init__(self, tools: Dict[str, Callable], max_iterations: int = 10):
        """
        Initialize the reasoning loop with available tools.
        
        Args:
            tools: Dictionary mapping tool names to tool functions
            max_iterations: Maximum number of reasoning iterations
        """
        self.tools = tools
        self.max_iterations = max_iterations
        self.working_memory = {
            "thoughts": [],
            "actions": [],
            "observations": [],
            "collected_data": {
                "competitors": [],
                "funding_data": {},
                "web_search_results": [],
                "rag_results": []
            }
        }
        
    def run(self, parsed_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run the reasoning loop until completion or max iterations.
        
        Args:
            parsed_input: Structured input data from the input parser
            
        Returns:
            Working memory with all collected data
        """
        iteration = 0
        
        while iteration < self.max_iterations:
            # Generate thought
            thought = self._generate_thought(parsed_input, self.working_memory)
            self.working_memory["thoughts"].append(thought)
            
            # Determine next action
            action, tool_name, tool_args = self._determine_action(thought, self.working_memory)
            self.working_memory["actions"].append({
                "tool": tool_name,
                "args": tool_args,
                "timestamp": time.time()
            })
            
            # Execute action
            if tool_name in self.tools:
                observation = self.tools[tool_name](**tool_args)
                self.working_memory["observations"].append(observation)
                
                # Store results in the appropriate category
                self._update_collected_data(tool_name, observation)
            else:
                self.working_memory["observations"].append(f"Error: Tool '{tool_name}' not found")
            
            # Check if we have enough data to stop
            if self._should_stop():
                break
                
            iteration += 1
            
        return self.working_memory
    
    def _generate_thought(self, parsed_input: Dict[str, Any], memory: Dict[str, Any]) -> str:
        """
        Generate the next thought based on current state.
        In a production system, this would use an LLM.
        
        Args:
            parsed_input: Structured input data
            memory: Current working memory
            
        Returns:
            Thought string
        """
        # In production, this would call an LLM API
        # For now, implement a simple rule-based system
        
        collected_data = memory["collected_data"]
        
        if not collected_data["competitors"]:
            return f"I need to find competitors in the {parsed_input['domain']} domain"
        elif not collected_data["funding_data"] and collected_data["competitors"]:
            return "I should retrieve funding data for the identified competitors"
        elif not collected_data["web_search_results"]:
            return f"I need to search for market trends in {parsed_input['domain']}"
        elif not collected_data["rag_results"]:
            return "I should query the RAG system for additional context"
        else:
            return "I have collected sufficient data for analysis"
    
    def _determine_action(self, thought: str, memory: Dict[str, Any]) -> tuple:
        """
        Determine the next action based on the current thought.
        
        Args:
            thought: Current thought
            memory: Current working memory
            
        Returns:
            Tuple of (action description, tool name, tool arguments)
        """
        # In production, this would use an LLM to determine the action
        # For now, implement a simple rule-based system
        
        parsed_input = memory.get("parsed_input", {})
        
        if "find competitors" in thought.lower():
            return (
                "Search for competitors",
                "CompetitorFinder",
                {"domain": parsed_input.get("domain", ""), "features": parsed_input.get("key_features", [])}
            )
        elif "funding data" in thought.lower():
            competitors = memory["collected_data"]["competitors"]
            company_names = [comp["name"] for comp in competitors] if competitors else []
            return (
                "Retrieve funding data",
                "FundingRetriever",
                {"companies": company_names}
            )
        elif "search for market" in thought.lower():
            domain = parsed_input.get("domain", "")
            query = f"{domain} market trends 2023"
            return (
                "Web search for market trends",
                "WebSearchTool",
                {"query": query, "num_results": 5}
            )
        elif "query the RAG" in thought.lower():
            domain = parsed_input.get("domain", "")
            query = f"{domain} startup success factors"
            return (
                "RAG query for domain knowledge",
                "RAGQueryTool",
                {"query": query}
            )
        else:
            return (
                "No action needed",
                "NoOp",
                {}
            )
    
    def _update_collected_data(self, tool_name: str, observation: Any) -> None:
        """
        Update the collected data based on tool results.
        
        Args:
            tool_name: Name of the tool that was called
            observation: Result from the tool call
        """
        if tool_name == "CompetitorFinder":
            self.working_memory["collected_data"]["competitors"] = observation
        elif tool_name == "FundingRetriever":
            self.working_memory["collected_data"]["funding_data"] = observation
        elif tool_name == "WebSearchTool":
            self.working_memory["collected_data"]["web_search_results"] = observation
        elif tool_name == "RAGQueryTool":
            self.working_memory["collected_data"]["rag_results"] = observation
    
    def _should_stop(self) -> bool:
        """
        Determine if we have collected enough data to stop the loop.
        
        Returns:
            Boolean indicating whether to stop the loop
        """
        # Check if we have data in all categories
        collected_data = self.working_memory["collected_data"]
        
        has_competitors = len(collected_data["competitors"]) > 0
        has_funding = bool(collected_data["funding_data"])
        has_web_results = len(collected_data["web_search_results"]) > 0
        has_rag_results = len(collected_data["rag_results"]) > 0
        
        # We need at least competitors, funding data, and either web results or RAG results
        return has_competitors and has_funding and (has_web_results or has_rag_results)
    
    def get_working_memory(self) -> Dict[str, Any]:
        """
        Get the current working memory.
        
        Returns:
            Current working memory dictionary
        """
        return self.working_memory