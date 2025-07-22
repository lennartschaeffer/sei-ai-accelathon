import asyncio
import aiohttp
import json
from typing import Dict, Any, Optional

class RPCClient:
    def __init__(self, rpc_url: str = "https://evm-rpc.sei-apis.com"):
        self.rpc_url = rpc_url
        self.session = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def rpc_call(self, method: str, params: list = []):
        """Make a JSON-RPC call to Sei network"""
        if not self.session:
            raise RuntimeError("Session not initialized")
        
        payload = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params or [],
            "id": 1
        }
        
        try:
            async with self.session.post(
                self.rpc_url,
                json=payload,
                headers={"Content-Type": "application/json"}
            ) as response:
                result = await response.json()
                
                if "error" in result:
                    raise Exception(f"RPC Error: {result['error']}")
                
                return result.get("result")
                
        except Exception as e:
            raise Exception(f"RPC call failed for {method}: {e}")

    async def get_latest_block(self):
        """Get latest block data - returns full block info to match MCP interface"""
        block_number_hex = await self.rpc_call("eth_blockNumber")
        block_number = int(block_number_hex, 16)
        
        # Get full block data
        block_data = await self.rpc_call("eth_getBlockByNumber", [block_number_hex, True])
        
        # Add decoded number to match MCP client format
        block_data["number"] = block_number
        return block_data

    async def get_block_by_number(self, block_number: int):
        """Get block by number"""
        hex_block = hex(block_number)
        block_data = await self.rpc_call("eth_getBlockByNumber", [hex_block, True])
        
        if not block_data:
            raise Exception(f"Block {block_number} not found")
            
        # Add decoded number for consistency
        block_data["number"] = block_number
        return block_data

    async def get_transaction_receipt(self, tx_hash: str):
        """Get transaction receipt"""
        receipt = await self.rpc_call("eth_getTransactionReceipt", [tx_hash])
        
        if not receipt:
            raise Exception(f"Receipt for transaction {tx_hash} not found")
            
        return receipt

    async def get_balance(self, address: str, block_tag: str = "latest"):
        """Get ETH balance for address"""
        balance_hex = await self.rpc_call("eth_getBalance", [address, block_tag])
        balance_wei = int(balance_hex, 16)
        balance_eth = balance_wei / 10**18
        
        return {
            "wei": balance_wei,
            "eth": balance_eth,
            "formatted": str(balance_eth)
        }

    async def get_token_balance(self, wallet_address: str, token_address: str):
        """Get ERC-20 token balance using eth_call"""
        # ERC-20 balanceOf(address) function signature
        function_selector = "0x70a08231"  # balanceOf(address)
        
        # Encode address parameter (remove 0x and pad to 32 bytes)
        padded_address = wallet_address[2:].lower().zfill(64)
        data = function_selector + padded_address
        
        # Make eth_call
        result_hex = await self.rpc_call("eth_call", [
            {
                "to": token_address,
                "data": data
            },
            "latest"
        ])
        
        # Decode result
        if result_hex and result_hex != "0x":
            balance_wei = int(result_hex, 16)
            # USDC uses 6 decimals
            balance_formatted = balance_wei / 10**6
            
            return {
                "raw": str(balance_wei),
                "formatted": str(balance_formatted),
                "decimals": 6
            }
        else:
            return {
                "raw": "0",
                "formatted": "0",
                "decimals": 6
            }