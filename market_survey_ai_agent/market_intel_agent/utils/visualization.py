"""
Visualization utility for Market Intelligence Research Agent.

This module provides visualization functionality for generating charts and graphs.
"""
import matplotlib.pyplot as plt
import os
from typing import List, Dict, Any, Optional

class Visualizer:
    """
    Visualizer for generating charts and graphs for market intelligence reports.
    """
    
    def __init__(self, output_dir: str = "../reports/generated_reports"):
        """
        Initialize the visualizer.
        
        Args:
            output_dir: Directory to save visualizations
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
    def create_funding_bar_chart(self, companies: List[str], funding_amounts: List[float], 
                                 title: str = "Funding Comparison", 
                                 filename: str = "funding_chart.png") -> str:
        """
        Create a bar chart comparing funding amounts.
        
        Args:
            companies: List of company names
            funding_amounts: List of funding amounts
            title: Chart title
            filename: Output filename
            
        Returns:
            Path to the saved chart
        """
        plt.figure(figsize=(10, 6))
        plt.bar(companies, funding_amounts)
        plt.title(title)
        plt.xlabel("Companies")
        plt.ylabel("Funding Amount (USD)")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        
        # Save the chart
        output_path = os.path.join(self.output_dir, filename)
        plt.savefig(output_path)
        plt.close()
        
        return output_path
    
    def create_market_share_pie_chart(self, companies: List[str], market_shares: List[float],
                                     title: str = "Market Share Distribution",
                                     filename: str = "market_share_chart.png") -> str:
        """
        Create a pie chart showing market share distribution.
        
        Args:
            companies: List of company names
            market_shares: List of market share percentages
            title: Chart title
            filename: Output filename
            
        Returns:
            Path to the saved chart
        """
        plt.figure(figsize=(10, 8))
        plt.pie(market_shares, labels=companies, autopct='%1.1f%%', startangle=90)
        plt.title(title)
        plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
        
        # Save the chart
        output_path = os.path.join(self.output_dir, filename)
        plt.savefig(output_path)
        plt.close()
        
        return output_path
    
    def create_trend_line_chart(self, x_values: List, y_values: List, 
                               title: str = "Market Trend",
                               x_label: str = "Time Period", 
                               y_label: str = "Value",
                               filename: str = "trend_chart.png") -> str:
        """
        Create a line chart showing trends over time.
        
        Args:
            x_values: X-axis values (e.g., time periods)
            y_values: Y-axis values (e.g., market size)
            title: Chart title
            x_label: X-axis label
            y_label: Y-axis label
            filename: Output filename
            
        Returns:
            Path to the saved chart
        """
        plt.figure(figsize=(10, 6))
        plt.plot(x_values, y_values, marker='o')
        plt.title(title)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.tight_layout()
        
        # Save the chart
        output_path = os.path.join(self.output_dir, filename)
        plt.savefig(output_path)
        plt.close()
        
        return output_path