"""
Output Formatter Module for Market Intelligence Research Agent.

This module formats the synthesized report into Markdown or HTML format.
"""
from typing import Dict, List, Any, Optional
import os
import markdown
import json

class OutputFormatter:
    """
    Formats the synthesized report into Markdown or HTML format.
    Handles rendering of charts and tables.
    """
    
    def __init__(self, output_dir: str = "reports/generated_reports"):
        """
        Initialize the output formatter.
        
        Args:
            output_dir: Directory to save generated reports
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def format_report(self, report_data: Dict[str, Any], 
                     parsed_input: Dict[str, Any],
                     output_format: str = "markdown") -> str:
        """
        Format the report data into the specified output format.
        
        Args:
            report_data: Dictionary containing report sections
            parsed_input: Original parsed input
            output_format: Output format (markdown or html)
            
        Returns:
            Formatted report as string
        """
        # Generate report filename based on domain
        domain = parsed_input.get("domain", "market")
        filename = f"{domain.lower().replace(' ', '_')}_market_report"
        
        # Combine report sections
        markdown_content = self._combine_sections(report_data)
        
        # Save markdown report
        md_path = os.path.join(self.output_dir, f"{filename}.md")
        with open(md_path, "w") as f:
            f.write(markdown_content)
        
        # If HTML output is requested, convert markdown to HTML
        if output_format.lower() == "html":
            html_content = markdown.markdown(markdown_content)
            html_path = os.path.join(self.output_dir, f"{filename}.html")
            with open(html_path, "w") as f:
                f.write(self._wrap_html(html_content))
            return html_path
        
        return md_path
    
    def _combine_sections(self, report_data: Dict[str, Any]) -> str:
        """
        Combine report sections into a single markdown document.
        
        Args:
            report_data: Dictionary containing report sections
            
        Returns:
            Combined markdown content
        """
        sections = [
            report_data.get("executive_summary", "# Executive Summary\n\nNo data available."),
            report_data.get("competitor_landscape", "# Competitor Landscape\n\nNo data available."),
            report_data.get("funding_analysis", "# Funding Analysis\n\nNo data available."),
            report_data.get("swot_analysis", "# SWOT Analysis\n\nNo data available."),
            report_data.get("market_trends", "# Market Trends\n\nNo data available."),
            self._format_confidence_appendix(report_data.get("confidence_scores", {}))
        ]
        
        return "\n\n".join(sections)
    
    def _format_confidence_appendix(self, confidence_scores: Dict[str, float]) -> str:
        """
        Format confidence scores as an appendix.
        
        Args:
            confidence_scores: Dictionary of confidence scores
            
        Returns:
            Formatted confidence appendix
        """
        if not confidence_scores:
            return "# Confidence Appendix\n\nNo confidence data available."
        
        # Create confidence table
        table_header = "| Section | Confidence Score |\n| --- | --- |\n"
        table_rows = ""
        
        for section, score in confidence_scores.items():
            if section != "overall_confidence":
                section_name = section.replace("_", " ").title()
                table_rows += f"| {section_name} | {score:.2f} |\n"
        
        overall = confidence_scores.get("overall_confidence", 0.0)
        
        appendix = f"""
# Confidence Appendix

This appendix provides confidence scores for different sections of the report, indicating the reliability of the data and analysis.

{table_header}{table_rows}

**Overall Confidence Score: {overall:.2f}**

*Confidence scores range from 0.0 (low confidence) to 1.0 (high confidence).*
        """
        
        return appendix.strip()
    
    def _wrap_html(self, html_content: str) -> str:
        """
        Wrap HTML content in a basic HTML document with styling.
        
        Args:
            html_content: HTML content to wrap
            
        Returns:
            Complete HTML document
        """
        return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Market Intelligence Report</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }}
        h1, h2, h3 {{
            color: #2c3e50;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 20px 0;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }}
        th {{
            background-color: #f2f2f2;
        }}
        img {{
            max-width: 100%;
            height: auto;
        }}
        .confidence-score {{
            font-weight: bold;
            color: #3498db;
        }}
    </style>
</head>
<body>
    {html_content}
</body>
</html>"""