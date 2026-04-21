# Market Intelligence Research Agent

An autonomous agent that transforms a plain-English startup idea into a comprehensive Market Intelligence Report through autonomous reasoning, retrieval, and synthesis.

## 🧩 System Architecture

```
/market_intel_agent
  ├── main.py                 # Main entry point
  ├── core/                   # Core agent components
  │   ├── input_parser.py     # Parses user input into structured format
  │   ├── reasoning_loop.py   # ReAct reasoning loop implementation
  │   ├── synthesizer.py      # Synthesizes collected data into report
  │   └── output_formatter.py # Formats report into Markdown/HTML
  ├── tools/                  # Modular tools for data collection
  │   ├── competitor_finder.py # Finds competitors from dataset
  │   ├── funding_retriever.py # Retrieves funding data
  │   ├── rag_query_tool.py    # Performs RAG queries
  │   ├── web_search_tool.py   # Performs web searches
  │   ├── news_api_tool.py     # Retrieves real-time news articles
  │   ├── yahoo_finance_tool.py # Retrieves financial market data
  ├── data/                   # Local datasets
  │   ├── indian_startup_dataset.csv
  │   ├── crunchbase_investments.csv
  ├── vector_db/              # Vector database for RAG
  │   └── embeddings_store/
  ├── utils/                  # Utility modules
  │   ├── logger.py           # Logging functionality
  │   ├── memory.py           # Working memory management
  │   ├── visualization.py    # Chart generation
  │   └── confidence_scorer.py # Source reliability scoring
  ├── configs/                # Configuration files
  │   ├── api_keys.yaml       # API keys (not committed to version control)
  │   └── model_config.yaml   # Model and agent configuration
  └── reports/                # Generated reports
      └── generated_reports/
```

## ⚙️ System Workflow

The Market Intelligence Research Agent follows a four-phase workflow:

1. **Input Parsing & Understanding**: Converts user text into structured JSON
2. **ReAct Reasoning Loop**: Implements autonomous "Think → Act → Observe" cycle
3. **Synthesis & Report Generation**: Aggregates collected data into a comprehensive report
4. **Final Structured Output**: Renders the report in Markdown and HTML formats

## 🛠️ Installation

1. Clone the repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Add your API keys to `configs/api_keys.yaml`

## 📊 Usage

Run the agent with a startup idea:

```bash
python main.py --idea "We are building a menstrual health app with AI-driven cycle prediction and community features."
```

## 📋 Output

The agent generates:
- A comprehensive market intelligence report in Markdown and HTML formats
- Visualizations for funding data, market share, and trends
- Detailed logs of the reasoning process

## 🧠 Key Components

### Core Modules

- **IntelligentInputParser**: Converts user input into structured JSON
- **ReasoningLoop**: Implements the ReAct cycle for autonomous reasoning
- **Synthesizer**: Aggregates data and generates the report
- **OutputFormatter**: Formats the report in Markdown and HTML

### Tool Modules

- **CompetitorFinder**: Finds competitors using the Indian Startup dataset
- **FundingRetriever**: Retrieves funding data using the Crunchbase dataset
- **WebSearchTool**: Performs web searches using external APIs
- **RAGQueryTool**: Performs semantic search using a vector database
- **NewsAPITool**: Retrieves real-time news articles related to companies and industries
- **YahooFinanceTool**: Retrieves financial market data, stock prices, and company information

### Utility Modules

- **AgentLogger**: Logs agent actions, thoughts, and observations
- **WorkingMemory**: Stores agent state during the reasoning loop
- **Visualizer**: Generates charts and graphs for the report
- **ConfidenceScorer**: Scores the reliability of information sources

## 📝 Example Report Structure

1. **Executive Summary**
2. **Competitor Landscape Table + Bar Chart**
3. **Funding Analysis**
4. **Financial Overview** (when company data is available)
5. **Recent Headlines** (when news data is available)
6. **SWOT Analysis**
7. **Market Trends (with citations)**
8. **Confidence Appendix**

## 🔄 Fallback Mechanism

The agent includes an intelligent fallback mechanism that:
- Automatically detects when data collection tools fail to provide quality results
- Falls back to web search when specialized tools don't return sufficient data
- Configurable confidence thresholds and maximum fallback attempts
- Ensures comprehensive reports even when primary data sources are unavailable

## 🔄 Extending the System

The modular architecture allows for easy extension:
- Add new tools in the `tools/` directory
- Modify the reasoning loop in `core/reasoning_loop.py`
- Add new visualization types in `utils/visualization.py`
- Configure model parameters in `configs/model_config.yaml`
