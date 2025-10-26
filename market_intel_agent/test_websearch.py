"""
Simple test script for WebSearchTool
"""
from tools.web_search_tool import WebSearchTool
from utils.logger import AgentLogger
import yaml

def main():
    # Initialize logger
    logger = AgentLogger('test_websearch')
    
    # Load API keys
    with open('configs/api_keys.yaml', 'r') as f:
        api_keys = yaml.safe_load(f)
    
    # Initialize WebSearchTool
    web_search = WebSearchTool(
        api_key=api_keys['serper']['api_key'],
        search_engine='serper',
        logger=logger
    )
    
    # Perform search
    results = web_search.search('latest trends in AI', 5)
    
    # Print results
    print('Search Results:')
    for i, result in enumerate(results):
        print(f'{i+1}. {result["title"]}')
        print(f'   URL: {result["url"]}')
        print(f'   Snippet: {result["snippet"]}')
        print()

if __name__ == "__main__":
    main()