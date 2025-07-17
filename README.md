## Project Overview

This is an AI-powered stablecoin monitoring system for the Sei blockchain. The project implements a multi-agent architecture that monitors on-chain stablecoin flows, identifies risky behavior, and provides real-time analysis.

## Core Architecture

### Watcher Agent (`watcher_agent.py`)

- Main monitoring component that connects to Sei blockchain via MCP (Model Context Protocol)
- Uses `@sei-js/mcp-server` npm package to access blockchain data
- Continuously polls for new blocks and analyzes transaction logs
- Specifically monitors USDC transfers (contract: `0x3894085ef7ff0f0aedf52e2a2704928d1ec074f1`)
- Extracts transfer events and decodes transaction data

### MCP Integration

- Uses `stdio_client` to connect to Sei MCP server via npx
- Key MCP tools available:
  - https://sei-js.docs.sei.io/mcp-server/tools#read-only-tools-always-available
  - https://sei-js.docs.sei.io/mcp-server/tools#network-%26-blockchain-data
  - https://sei-js.docs.sei.io/mcp-server/tools#read-only-contract-tools
- Connection established through `StdioServerParameters` with npx command

### Planned Multi-Agent System

- **Watcher Agent**: Normalizes blockchain events into structured data
  - [] Whale wallet tracking and classification
- **Depeg Risk Agent** evaluate depeg risk of a stablecoin based on recent on-chain events - LangChain integration for natural language querying
- Multi-token support beyond USDC

## Development Commands

### Running the Watcher Agent

```bash
python watcher_agent.py
```

### Python Environment

The project uses a virtual environment located in `venv/`. Activate with:

```bash
source venv/bin/activate  # On macOS/Linux
```

## Key Dependencies

- `mcp`: Model Context Protocol client for blockchain integration
- `asyncio`: Asynchronous programming for real-time monitoring
- `json`: JSON parsing for blockchain data
- Node.js package: `@sei-js/mcp-server` (installed via npx)

## Data Processing

### Stablecoin Monitoring

- Tracks USDC transfers on Sei blockchain
- Decodes ERC-20 Transfer events from transaction logs
- Extracts: from_address, to_address, value (converted from wei to USDC)
- Currently configured for 6-decimal USDC token

### Block Processing

- Polls every 5 seconds for new blocks
- Processes blocks sequentially to avoid missing transactions
- Maintains `last_block_number` state to handle only new blocks

## Important Notes

- The MCP server requires Node.js and npx to be available
- Private keys can be added via environment variables in `server_params.env`
- Transaction log parsing assumes standard ERC-20 Transfer event format
- Currently hardcoded for Sei network only
