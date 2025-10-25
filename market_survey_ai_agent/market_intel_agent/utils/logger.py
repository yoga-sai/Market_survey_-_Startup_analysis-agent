"""
Logger utility for Market Intelligence Research Agent.

This module provides logging functionality for tracking agent actions, thoughts, and observations.
"""
import logging
import os
from datetime import datetime

class AgentLogger:
    """
    Logger for tracking agent actions, thoughts, and observations.
    """
    
    def __init__(self, log_dir: str = "../logs", log_level: int = logging.INFO):
        """
        Initialize the logger.
        
        Args:
            log_dir: Directory to store log files
            log_level: Logging level
        """
        self.log_dir = log_dir
        
        # Create log directory if it doesn't exist
        os.makedirs(log_dir, exist_ok=True)
        
        # Create timestamp for log file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = os.path.join(log_dir, f"agent_log_{timestamp}.log")
        
        # Configure logger
        self.logger = logging.getLogger("market_intel_agent")
        self.logger.setLevel(log_level)
        
        # Create file handler
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(log_level)
        
        # Create console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        
        # Create formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Add handlers to logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
        
    def log_thought(self, thought: str):
        """
        Log an agent thought.
        
        Args:
            thought: The thought to log
        """
        self.logger.info(f"THOUGHT: {thought}")
        
    def log_action(self, action: str, params: dict = None):
        """
        Log an agent action.
        
        Args:
            action: The action name
            params: Action parameters
        """
        if params:
            self.logger.info(f"ACTION: {action} - PARAMS: {params}")
        else:
            self.logger.info(f"ACTION: {action}")
        
    def log_observation(self, observation: str):
        """
        Log an observation from an action.
        
        Args:
            observation: The observation to log
        """
        self.logger.info(f"OBSERVATION: {observation}")
        
    def log_error(self, error: str):
        """
        Log an error.
        
        Args:
            error: The error message
        """
        self.logger.error(f"ERROR: {error}")
        
    def log_info(self, message: str):
        """
        Log general information.
        
        Args:
            message: The message to log
        """
        self.logger.info(message)
        
    def log_debug(self, message: str):
        """
        Log debug information.
        
        Args:
            message: The message to log
        """
        self.logger.debug(message)