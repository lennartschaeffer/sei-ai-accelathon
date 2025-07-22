#!/usr/bin/env python3
"""
Quick test script to call Sei RPC methods and see responses.
Tests the core methods used by the watcher system.
"""

import asyncio
import aiohttp
import json
from typing import Dict, Any, Optional

# Sei mainnet RPC endpoint
SEI_RPC_URL = "https://evm-rpc.sei-apis.com"

class SeiRPCTester:
    def __init__(self, rpc_url: str = SEI_RPC_URL):
        self.rpc_url = rpc_url
        self.session = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def rpc_call(self, method: str, params: list = []) -> Dict[str, Any]:
        """Make a JSON-RPC call to Sei network"""
        if not self.session:
            raise RuntimeError("Session not initialized")
        
        payload = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params or [],
            "id": 1
        }
        
        print(f"\n🔍 Calling {method} with params: {params}")
        
        try:
            async with self.session.post(
                self.rpc_url,
                json=payload,
                headers={"Content-Type": "application/json"}
            ) as response:
                result = await response.json()
                
                if "error" in result:
                    print(f"❌ Error: {result['error']}")
                    return result
                
                print(f"✅ Success: {method}")
                return result
                
        except Exception as e:
            print(f"💥 Exception calling {method}: {e}")
            return {"error": str(e)}

    async def test_latest_block(self):
        """Test eth_blockNumber - get latest block number"""
        print("\n" + "="*50)
        print("Testing eth_blockNumber (latest block)")
        print("="*50)
        
        result = await self.rpc_call("eth_blockNumber")
        if "result" in result:
            block_num = int(result["result"], 16)
            print(f"📊 Latest block number: {block_num}")
            print(f"📊 Hex: {result['result']}")
            return block_num
        return None

    async def test_get_block_by_number(self, block_number: Optional[int] = None):
        """Test eth_getBlockByNumber"""
        print("\n" + "="*50)
        print("Testing eth_getBlockByNumber")
        print("="*50)
        
        if block_number is None:
            # Get latest block first
            latest = await self.test_latest_block()
            if latest:
                block_number = latest - 1  # Use previous block to ensure it exists
        
        if block_number:
            hex_block = hex(block_number)
            result = await self.rpc_call("eth_getBlockByNumber", [hex_block, True])
            
            if "result" in result and result["result"]:
                block_data = result["result"]
                print(f"📦 Block {block_number}:")
                print(f"   Hash: {block_data.get('hash', 'N/A')}")
                print(f"   Parent: {block_data.get('parentHash', 'N/A')}")
                print(f"   Transactions: {len(block_data.get('transactions', []))}")
                print(f"   Gas Used: {int(block_data.get('gasUsed', '0x0'), 16) if block_data.get('gasUsed') else 0}")
                print(f"   Timestamp: {int(block_data.get('timestamp', '0x0'), 16) if block_data.get('timestamp') else 0}")
                
                # Return first transaction hash for next test
                txs = block_data.get('transactions', [])
                if txs and isinstance(txs[0], dict):
                    return txs[0].get('hash')
                elif txs and isinstance(txs[0], str):
                    return txs[0]
            else:
                print("❌ No block data returned")
        
        return None

    async def test_get_balance(self, address: str = ""):
        """Test eth_getBalance"""
        print("\n" + "="*50)
        print("Testing eth_getBalance")
        print("="*50)
        
        # Use a well-known address if none provided
        if not address:
            address = "0x0000000000000000000000000000000000000000"  # Zero address
            
        result = await self.rpc_call("eth_getBalance", [address, "latest"])
        
        if "result" in result:
            balance_wei = int(result["result"], 16)
            balance_eth = balance_wei / 10**18
            print(f"💰 Balance for {address}:")
            print(f"   Wei: {balance_wei}")
            print(f"   SEI: {balance_eth:.6f}")
            print(f"   Hex: {result['result']}")

    async def test_transaction_receipt(self, tx_hash: Optional[str] = None):
        """Test eth_getTransactionReceipt"""
        print("\n" + "="*50)
        print("Testing eth_getTransactionReceipt")
        print("="*50)
        
        if not tx_hash:
            print("⚠️  No transaction hash provided, skipping receipt test")
            return
            
        result = await self.rpc_call("eth_getTransactionReceipt", [tx_hash])
        
        if "result" in result and result["result"]:
            receipt = result["result"]
            print(f"🧾 Receipt for {tx_hash}:")
            print(f"   Block: {int(receipt.get('blockNumber', '0x0'), 16) if receipt.get('blockNumber') else 'N/A'}")
            print(f"   Status: {'Success' if receipt.get('status') == '0x1' else 'Failed'}")
            print(f"   Gas Used: {int(receipt.get('gasUsed', '0x0'), 16) if receipt.get('gasUsed') else 0}")
            print(f"   Logs: {len(receipt.get('logs', []))}")
            
            # Show first few logs if any
            logs = receipt.get('logs', [])
            if logs:
                print(f"   First log topics: {logs[0].get('topics', [])[:2]}...")
        else:
            print("❌ No receipt data returned")

    async def test_get_logs(self):
        """Test eth_getLogs for recent transfers"""
        print("\n" + "="*50)
        print("Testing eth_getLogs")
        print("="*50)
        
        # ERC20 Transfer event topic
        transfer_topic = "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef"
        
        result = await self.rpc_call("eth_getLogs", [{
            "fromBlock": "latest",
            "toBlock": "latest", 
            "topics": [transfer_topic]
        }])
        
        if "result" in result:
            logs = result["result"]
            print(f"📜 Found {len(logs)} transfer logs in latest block")
            
            if logs:
                log = logs[0]
                print(f"   Address: {log.get('address')}")
                print(f"   Block: {int(log.get('blockNumber', '0x0'), 16) if log.get('blockNumber') else 'N/A'}")
                print(f"   Topics: {len(log.get('topics', []))}")

async def main():
    """Run all RPC tests"""
    print("🚀 Starting Sei RPC Tests")
    print(f"📡 Using endpoint: {SEI_RPC_URL}")
    
    async with SeiRPCTester() as tester:
        # Test 1: Get latest block
        latest_block = await tester.test_latest_block()
        
        # Test 2: Get block by number (and get a tx hash)
        tx_hash = await tester.test_get_block_by_number(latest_block)
        
        # Test 3: Get balance
        await tester.test_get_balance()
        
        # Test 4: Get transaction receipt (if we have a tx hash)
        if tx_hash:
            await tester.test_transaction_receipt(tx_hash)
        
        # Test 5: Get logs
        await tester.test_get_logs()
    
    print("\n✨ All tests completed!")

if __name__ == "__main__":
    asyncio.run(main())