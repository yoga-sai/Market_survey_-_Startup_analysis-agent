"""
Market Intelligence Research Agent - Main Entry Point

This script orchestrates the end-to-end workflow for the Market Intelligence Research Agent,
which transforms a startup idea into a comprehensive market intelligence report.
"""
import os
import argparse
import yaml
import time
from datetime import datetime
import json

# Import core modules
from core.input_parser import IntelligentInputParser
from core.reasoning_loop import ReasoningLoop
from core.synthesizer import Synthesizer
from core.output_formatter import OutputFormatter

# Import tools
from tools.competitor_finder import CompetitorFinder
from tools.funding_retriever import FundingRetriever
from tools.web_search_tool import WebSearchTool
from tools.rag_query_tool import RAGQueryTool

# Import utilities
from utils.logger import AgentLogger
from utils.memory import WorkingMemory
from utils.visualization import Visualizer
from utils.confidence_scorer import ConfidenceScorer

def load_config(config_path):
    """Load configuration from YAML file."""
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def main():
    """Main entry point for the Market Intelligence Research Agent."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Market Intelligence Research Agent')
    parser.add_argument('--idea', type=str, required=True, help='Startup idea to analyze')
    parser.add_argument('--output_dir', type=str, default='reports/generated_reports', 
                        help='Directory to save generated reports')
    parser.add_argument('--config', type=str, default='configs/model_config.yaml',
                        help='Path to model configuration file')
    args = parser.parse_args()
    
    # Create timestamp for report
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Initialize logger
    logger = AgentLogger(log_dir='logs')
    logger.log_info(f"Starting Market Intelligence Research Agent with idea: {args.idea}")
    
    # Load configuration
    try:
        config = load_config(args.config)
        logger.log_info("Configuration loaded successfully")
    except Exception as e:
        logger.log_error(f"Error loading configuration: {str(e)}")
        return
    
    # Initialize working memory
    memory = WorkingMemory()
    parsed_input = {}
    
    # Parse input idea into structured data
    input_parser = IntelligentInputParser()
    try:
        parsed_input = input_parser.parse(args.idea)
    except Exception as e:
        logger.log_error(f"Input parsing failed: {e}. Using defaults.")
        parsed_input = {
            "core_idea": args.idea,
            "domain": "technology",
            "niche": "",
            "key_features": [],
            "target_audience": ""
        }

    
    # Load API keys
    try:
        api_keys = load_config('configs/api_keys.yaml')
        logger.log_info("API keys loaded successfully")
    except Exception as e:
        logger.log_error(f"Error loading API keys: {str(e)}")
        return

    # Initialize tools
    competitor_finder = CompetitorFinder(dataset_path="data/indian_startup_dataset.csv")
    funding_retriever = FundingRetriever(dataset_path="data/crunchbase_investments.csv")
    web_search_tool = WebSearchTool(api_key=api_keys['serper']['api_key'], search_engine='serper', logger=logger)

    # Test WebSearchTool with Serper
    logger.log_info("Testing WebSearchTool with Serper...")
    test_query = "latest trends in AI"
    serper_results = web_search_tool.search(test_query)
    logger.log_info(f"Serper search results for '{test_query}': {serper_results}")

    print(f"\nSerper search results for '{test_query}':")
    if serper_results:
        for i, result in enumerate(serper_results):
            print(f"  {i+1}. Title: {result.get('title')}")
            print(f"     Link: {result.get('url')}")
            print(f"     Snippet: {result.get('snippet')}")
    else:
        print("  No results found.")
    # End of temporary test

    rag_query_tool = RAGQueryTool(embeddings_dir="vector_db/embeddings_store")
    
    # Initialize confidence scorer
    confidence_scorer = ConfidenceScorer()
    
    # Initialize reasoning loop
    reasoning_loop = ReasoningLoop(
        tools={
            "CompetitorFinder": competitor_finder,
            "FundingRetriever": funding_retriever,
            "WebSearchTool": web_search_tool,
            "RAGQueryTool": rag_query_tool
        },
        max_iterations=config['agent']['max_iterations']
    )
    
    # Run reasoning loop
    logger.log_info("Starting reasoning loop...")
    wm = reasoning_loop.run(parsed_input)
    logger.log_info("Reasoning loop completed")
    
    # Initialize synthesizer
    synthesizer = Synthesizer(llm_api_key=api_keys['openai']['api_key'])
    
    # Initialize visualizer
    visualizer = Visualizer(output_dir=args.output_dir)
    
    # Synthesize report
    logger.log_info("Synthesizing report...")
    report_data = synthesizer.synthesize(working_memory=wm, parsed_input=parsed_input)
    logger.log_info("Report synthesis completed")
    
    # Format output
    output_formatter = OutputFormatter()
    
    # Generate report filename based on domain
    domain = parsed_input.get('domain', 'startup')
    report_filename = f"{domain.lower().replace(' ', '_')}_{timestamp}_report"
    
    # Format and save report
    logger.log_info("Formatting report...")
    markdown_report = output_formatter.format_report(report_data, parsed_input=parsed_input, output_format='markdown')
    html_report = output_formatter.format_report(report_data, parsed_input=parsed_input, output_format='html')
    
    # Save reports
    with open(os.path.join(args.output_dir, f"{report_filename}.md"), 'w') as f:
        f.write(markdown_report)
    
    with open(os.path.join(args.output_dir, f"{report_filename}.html"), 'w') as f:
        f.write(html_report)
    
    # Save memory state for debugging
    with open(os.path.join(args.output_dir, f"{report_filename}_memory.json"), 'w') as f:
        json.dump(wm, f, indent=2)
    
    logger.log_info(f"Reports generated successfully and saved to {args.output_dir}")
    logger.log_info(f"Markdown report: {report_filename}.md")
    logger.log_info(f"HTML report: {report_filename}.html")
    
    print(f"\nMarket Intelligence Report generated successfully!")
    print(f"Reports saved to: {os.path.abspath(args.output_dir)}")
    print(f"Markdown report: {report_filename}.md")
    print(f"HTML report: {report_filename}.html")

if __name__ == "__main__":
    main()