"""
Memory utility for Market Intelligence Research Agent.

This module provides working memory functionality for storing agent state.
"""
from typing import Dict, List, Any, Optional
import json
import os
from datetime import datetime

class WorkingMemory:
    """
    Working memory for storing agent state during reasoning loop.
    """
    
    def __init__(self):
        """Initialize working memory with empty collections."""
        self.thoughts = []
        self.actions = []
        self.observations = []
        self.collected_data = {
            "competitors": [],
            "funding_data": [],
            "web_search_results": [],
            "rag_results": []
        }
        self.parsed_input = {}
        
    def add_thought(self, thought: str):
        """
        Add a thought to memory.
        
        Args:
            thought: The thought to add
        """
        self.thoughts.append({
            "content": thought,
            "timestamp": datetime.now().isoformat()
        })
        
    def add_action(self, action_type: str, params: Dict[str, Any]):
        """
        Add an action to memory.
        
        Args:
            action_type: Type of action (e.g., "competitor_search")
            params: Action parameters
        """
        self.actions.append({
            "type": action_type,
            "params": params,
            "timestamp": datetime.now().isoformat()
        })
        
    def add_observation(self, action_type: str, result: Any):
        """
        Add an observation to memory.
        
        Args:
            action_type: Type of action that produced the observation
            result: Result of the action
        """
        self.observations.append({
            "action_type": action_type,
            "result": result,
            "timestamp": datetime.now().isoformat()
        })
        
    def update_collected_data(self, data_type: str, data: Any):
        """
        Update collected data.
        
        Args:
            data_type: Type of data (e.g., "competitors")
            data: The data to add
        """
        if data_type in self.collected_data:
            if isinstance(self.collected_data[data_type], list):
                if isinstance(data, list):
                    self.collected_data[data_type].extend(data)
                else:
                    self.collected_data[data_type].append(data)
            else:
                self.collected_data[data_type] = data
        else:
            self.collected_data[data_type] = data
            
    def set_parsed_input(self, parsed_input: Dict[str, Any]):
        """
        Set parsed input data.
        
        Args:
            parsed_input: Parsed input data
        """
        self.parsed_input = parsed_input
        
    def get_all_data(self) -> Dict[str, Any]:
        """
        Get all data from memory.
        
        Returns:
            Dictionary containing all memory data
        """
        return {
            "parsed_input": self.parsed_input,
            "thoughts": self.thoughts,
            "actions": self.actions,
            "observations": self.observations,
            "collected_data": self.collected_data
        }
        
    def save_to_file(self, file_path: str):
        """
        Save memory to a JSON file.
        
        Args:
            file_path: Path to save the file
        """
        with open(file_path, 'w') as f:
            json.dump(self.get_all_data(), f, indent=2)
            
    def load_from_file(self, file_path: str):
        """
        Load memory from a JSON file.
        
        Args:
            file_path: Path to load the file from
        """
        with open(file_path, 'r') as f:
            data = json.load(f)
            
        self.parsed_input = data.get("parsed_input", {})
        self.thoughts = data.get("thoughts", [])
        self.actions = data.get("actions", [])
        self.observations = data.get("observations", [])
        self.collected_data = data.get("collected_data", {
            "competitors": [],
            "funding_data": [],
            "web_search_results": [],
            "rag_results": []
        })