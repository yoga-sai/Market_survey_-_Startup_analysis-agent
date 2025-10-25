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
    
    # Initialize input parser
    input_parser = IntelligentInputParser()
    
    # Parse input
    logger.log_info("Parsing input...")
    parsed_input = input_parser.parse(args.idea)
    memory.set_parsed_input(parsed_input)
    logger.log_info(f"Parsed input: {parsed_input}")
    
    # Initialize tools
    competitor_finder = CompetitorFinder(data_path="data/indian_startup_dataset.csv")
    funding_retriever = FundingRetriever(data_path="data/crunchbase_investments.csv")
    web_search_tool = WebSearchTool(
        engine=config['web_search']['engine'],
        results_per_query=config['web_search']['results_per_query']
    )
    rag_query_tool = RAGQueryTool(embeddings_dir="vector_db/embeddings_store")
    
    # Initialize confidence scorer
    confidence_scorer = ConfidenceScorer()
    
    # Initialize reasoning loop
    reasoning_loop = ReasoningLoop(
        memory=memory,
        tools={
            "competitor_finder": competitor_finder,
            "funding_retriever": funding_retriever,
            "web_search_tool": web_search_tool,
            "rag_query_tool": rag_query_tool
        },
        logger=logger,
        max_iterations=config['agent']['max_iterations'],
        confidence_threshold=config['agent']['confidence_threshold']
    )
    
    # Run reasoning loop
    logger.log_info("Starting reasoning loop...")
    reasoning_loop.run()
    logger.log_info("Reasoning loop completed")
    
    # Initialize synthesizer
    synthesizer = Synthesizer(memory=memory, logger=logger)
    
    # Initialize visualizer
    visualizer = Visualizer(output_dir=args.output_dir)
    
    # Synthesize report
    logger.log_info("Synthesizing report...")
    report_data = synthesizer.synthesize(visualizer=visualizer)
    logger.log_info("Report synthesis completed")
    
    # Format output
    output_formatter = OutputFormatter()
    
    # Generate report filename based on domain
    domain = parsed_input.get('domain', 'startup')
    report_filename = f"{domain.lower().replace(' ', '_')}_{timestamp}_report"
    
    # Format and save report
    logger.log_info("Formatting report...")
    markdown_report = output_formatter.format_report(report_data, format_type='markdown')
    html_report = output_formatter.format_report(report_data, format_type='html')
    
    # Save reports
    with open(os.path.join(args.output_dir, f"{report_filename}.md"), 'w') as f:
        f.write(markdown_report)
    
    with open(os.path.join(args.output_dir, f"{report_filename}.html"), 'w') as f:
        f.write(html_report)
    
    # Save memory state for debugging
    memory.save_to_file(os.path.join(args.output_dir, f"{report_filename}_memory.json"))
    
    logger.log_info(f"Reports generated successfully and saved to {args.output_dir}")
    logger.log_info(f"Markdown report: {report_filename}.md")
    logger.log_info(f"HTML report: {report_filename}.html")
    
    print(f"\nMarket Intelligence Report generated successfully!")
    print(f"Reports saved to: {os.path.abspath(args.output_dir)}")
    print(f"Markdown report: {report_filename}.md")
    print(f"HTML report: {report_filename}.html")

if __name__ == "__main__":
    main()