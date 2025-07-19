## Project Overview

This is an AI-powered stablecoin monitoring system for the Sei blockchain. The project implements a modular architecture that monitors on-chain stablecoin flows, identifies whale activity, and provides real-time transaction analysis with balance monitoring capabilities.

## Core Architecture

The system is built with a clean separation of concerns across multiple modules:

### Main Components

- **Entry Point** (`main.py`): Application entry point that initializes and runs the watcher agent
- **Watcher Agent** (`watcher/agent.py`): Orchestrates the monitoring process and MCP connection
- **Block Processor** (`watcher/block_processor.py`): Processes new blocks and coordinates analysis components
- **Transaction Analyzer** (`watcher/transaction_analyzer.py`): Analyzes transaction logs for stablecoin transfers
- **Whale Tracker** (`watcher/whale_tracker.py`): Detects and tracks large transactions and high-volume wallets
- **Balance Monitor** (`watcher/balance_monitor.py`): Monitors token balances for whale wallets
- **MCP Client** (`core/mcp_client.py`): Handles blockchain data retrieval via MCP protocol

### MCP Integration

- Uses `stdio_client` to connect to Sei MCP server via npx
- Key MCP tools available:
  - https://sei-js.docs.sei.io/mcp-server/tools#read-only-tools-always-available
  - https://sei-js.docs.sei.io/mcp-server/tools#network-%26-blockchain-data
  - https://sei-js.docs.sei.io/mcp-server/tools#read-only-contract-tools
- Connection established through `StdioServerParameters` with npx command

### Whale Detection Features

#### Large Transaction Detection
- Monitors individual transactions above configurable threshold (default: 100 USDC)
- Instantly flags whale transactions with detailed event information

#### High Volume Detection  
- Tracks cumulative transaction volume per wallet over time windows (default: 60 minutes)
- Identifies wallets exceeding volume thresholds (default: 500,000 USDC)
- Maintains rolling activity windows for accurate volume calculations

#### Whale Event Tracking
- **Event Types**: `large_transaction` and `high_volume`
- **Directions**: `incoming` and `outgoing` transaction flows
- **Metadata**: Total volume, timestamps, transaction hashes
- **Alerts**: Real-time console output with whale emoji indicators

### Balance Monitoring

- **Automatic Monitoring**: Whale wallets are automatically added to balance monitoring
- **Periodic Checks**: Balance updates every 5 blocks for monitored wallets
- **Real-time Updates**: Current USDC balances for all tracked whale addresses
- **Configurable**: Balance monitoring can be enabled/disabled via settings

## Development Commands

### Running the Application

```bash
python main.py
```

### Python Environment

The project uses a virtual environment located in `venv/`. Activate with:

```bash
source venv/bin/activate  # On macOS/Linux
```

## Configuration

All system settings are centralized in `config/settings.py`:

### Whale Detection Thresholds
- `WHALE_SINGLE_TX_THRESHOLD`: Minimum amount for large transaction alerts (default: 100 USDC)
- `WHALE_VOLUME_THRESHOLD`: Cumulative volume threshold for high-volume detection (default: 500,000 USDC)  
- `WHALE_TIME_WINDOW_MINUTES`: Time window for volume calculations (default: 60 minutes)

### Balance Monitoring
- `BALANCE_MONITORING_ENABLED`: Enable/disable balance tracking (default: True)
- `BALANCE_CHECK_INTERVAL_BLOCKS`: Blocks between balance checks (default: 5)

### Network Settings
- `NETWORK`: Target blockchain network (default: "sei")
- `POLL_INTERVAL`: Seconds between block polling (default: 5)
- `STABLECOIN_ADDRESSES`: Contract addresses for monitored tokens

## Key Dependencies

- `mcp`: Model Context Protocol client for blockchain integration
- `asyncio`: Asynchronous programming for real-time monitoring
- `json`: JSON parsing for blockchain data
- `datetime`: Timestamp handling for whale event tracking
- Node.js package: `@sei-js/mcp-server` (installed via npx)

## Data Processing

### Stablecoin Monitoring

- Tracks USDC transfers on Sei blockchain (contract: `0x3894085ef7ff0f0aedf52e2a2704928d1ec074f1`)
- Decodes ERC-20 Transfer events from transaction logs
- Extracts: from_address, to_address, value (converted from wei to USDC)
- Currently configured for 6-decimal USDC token

### Block Processing

- Polls every 5 seconds for new blocks (configurable)
- Processes blocks sequentially to avoid missing transactions
- Maintains `last_block_number` state to handle only new blocks
- Coordinates whale detection and balance monitoring across all transfers

### Utility Functions

The `core/utils.py` module provides helper functions:
- `extract_address_from_topic()`: Extracts Ethereum addresses from log topics
- `format_transfer_output()`: Formats stablecoin transfer information for console output
- `format_whale_event()`: Formats whale detection alerts with emoji indicators

## Important Notes

- The MCP server requires Node.js and npx to be available
- Private keys can be added via environment variables in `server_params.env`
- Transaction log parsing assumes standard ERC-20 Transfer event format
- Currently hardcoded for Sei network only
