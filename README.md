# AI-Powered Stablecoin Monitoring Agent

A comprehensive monitoring system that tracks stablecoin risk on Sei blockchain, analyzes on-chain flows, identifies risky behavior patterns, and delivers real-time alerts to users through a Telegram interface.

## Project Overview

This system monitors stablecoin activity on the Sei blockchain using the Sei MCP Kit, processes events through a multi-agent pipeline, and provides real-time risk analysis and alerts to users via Telegram.

### Key Features

- Real-time monitoring of stablecoin transactions and liquidity pool events
- Automated risk scoring based on on-chain activity and historical patterns
- Natural language summarization of complex risk data
- User-friendly Telegram interface for alerts and queries
- Multi-agent architecture for scalable and modular processing

## System Architecture

The system consists of several interconnected agents working together:

```
                         ┌────────────────────────┐
                         │  Telegram Bot (User UI)│
                         └─────────┬──────────────┘
                                   │
                        User queries or receives alerts
                                   │
                         ▼─────────────────────▼
               ┌────────────────────┐    ┌─────────────────────┐
               │ Reasoning Agent    │<───│   Flight Risk Score │
               │ (LLM/NLP: Claude/  │    │     Classifier      │
               │  GPT via LangChain)│    └─────────────────────┘
               └────────┬───────────┘               ▲
                        │                          │
                        ▼                          │
               ┌────────────────────┐              │
               │    Event Parser    │◄─────────────┘
               │  (Signal Preprocessor)           Sei
               └────────┬───────────┘         MCP Kit Feed
                        │
                        ▼
               ┌────────────────────┐
               │  Watcher Agent     │
               │  (Wallet + Pool    │
               │   Monitor via Sei  │
               │   MCP Streams)     │
               └────────────────────┘
```

## Components

### 1. Watcher Agent
- Connects to Sei blockchain using Sei MCP Kit
- Monitors token transfers, swaps, and liquidity pool events
- Filters for stablecoins (USDC/USDT/DAI) and whale addresses

### 2. Event Parser
- Receives raw events from the Watcher Agent
- Normalizes and enriches data (wallet classification, pool TVL changes, behavior patterns)
- Outputs structured data for risk analysis

### 3. Flight Risk Score Classifier
- Assigns risk scores (0-100) to tokens based on event patterns
- Applies heuristic rules for risk assessment
- Tracks factors like whale exits, liquidity drops, and historical patterns

### 4. Reasoning Agent
- Uses LLM (OpenAI/Claude via LangChain) to generate human-readable summaries
- Contextualizes risk data with historical comparisons
- Creates concise risk updates for end users

### 5. Telegram Bot
- Provides user interface for interacting with the system
- Handles commands for status checks and alert subscriptions
- Delivers formatted risk alerts to users

### 6. Orchestrator (main.py)
- Coordinates all agent activities
- Routes events through the processing pipeline
- Manages periodic checks and alert triggers

## Implementation Steps

### Step 1: Set Up Project Structure
Create the basic directory structure for the project:
```
stablecoin-monitor/
├── watcher_agent/
│   └── watcher.py
├── parser_agent/
│   └── parser.py
├── classifier_agent/
│   └── classifier.py
├── reasoning_agent/
│   └── reasoning.py
├── telegram_bot/
│   └── bot.py
├── utils/
│   └── config.py
├── main.py
├── requirements.txt
```

### Step 2: Implement Watcher Agent
- Connect to Sei's WebSocket feed using Sei MCP Kit
- Subscribe to relevant events (Transfer, Swap, LiquidityRemove)
- Filter for stablecoins and whale addresses
- Create a data pipeline to pass events to the parser

### Step 3: Create Event Parser
- Build a function that normalizes raw blockchain events
- Add enrichment data like wallet classification and pool TVL changes
- Output structured event data for risk analysis

### Step 4: Develop Risk Classifier
- Implement a scoring system for flight risk (0-100)
- Apply heuristic rules based on transaction patterns and market conditions
- Generate detailed risk assessments with supporting evidence

### Step 5: Build Reasoning Agent
- Integrate with OpenAI or Claude API via LangChain
- Develop prompt templates for risk summarization
- Generate concise, human-readable risk updates

### Step 6: Create Telegram Bot
- Set up a Telegram bot with python-telegram-bot
- Implement commands for status checks and alert subscriptions
- Design clear and informative alert messages

### Step 7: Develop Main Orchestrator
- Create an async system to coordinate agent activities
- Implement event routing logic
- Set up periodic checks and alert triggers

## Setup and Installation

### Prerequisites
- Python 3.8+
- Sei blockchain node access or Sei MCP Kit credentials
- OpenAI or Claude API key
- Telegram Bot token

### Installation
1. Clone the repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Configure environment variables:
   - Create a `.env` file with necessary API keys and configurations
   - Set Sei node endpoints and authentication details
   - Add LLM API keys
   - Configure Telegram bot token

### Configuration
- Edit `utils/config.py` to set up:
  - Stablecoin addresses to monitor
  - Whale wallet thresholds
  - Risk scoring parameters
  - Alert thresholds

### Running the System
```
python main.py
```

## Dependencies
- python-telegram-bot
- websockets
- aiohttp
- pandas
- openai / anthropic
- langchain
- scikit-learn
- apscheduler (optional)
- dotenv

## Next Steps
- Implement event persistence with a database
- Add more sophisticated risk models
- Create a web dashboard for analytics
- Expand monitoring to more tokens and chains
