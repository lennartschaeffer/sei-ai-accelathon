from config.settings import STABLECOIN_ADDRESSES, USDC_DECIMALS
from core.utils import extract_address_from_topic, format_transfer_output

class TransactionAnalyzer:
    def __init__(self):
        self.stablecoin_addresses = {addr.lower() for addr in STABLECOIN_ADDRESSES.values()}
    
    def is_stablecoin_transfer(self, log):
        return log.get("address", "").lower() in self.stablecoin_addresses
    
    def parse_transfer_log(self, log, tx_hash):
        from_addr = extract_address_from_topic(log["topics"][1])
        to_addr = extract_address_from_topic(log["topics"][2])
        value = int(log["data"], 16) / 10**USDC_DECIMALS
        
        return {
            "tx_hash": tx_hash,
            "from_address": from_addr,
            "to_address": to_addr,
            "value": value,
            "block_number": log["blockNumber"],
            "log_index": log["logIndex"]
        }
    
    def analyze_transaction_logs(self, logs, tx_hash):
        transfers = []
        for log in logs:
            if self.is_stablecoin_transfer(log):
                transfer = self.parse_transfer_log(log, tx_hash)
                transfers.append(transfer)
                print(format_transfer_output(
                    transfer["tx_hash"],
                    transfer["value"],
                    transfer["block_number"],
                    transfer["log_index"]
                ))
        return transfers