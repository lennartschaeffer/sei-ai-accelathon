def extract_address_from_topic(topic):
    return "0x" + topic[-40:]

def format_transfer_output(tx_hash, value, block_number, log_index):
    return f"""
Stablecoin Transfer Detected!
Tx Hash:   {tx_hash}
Value:     {value} USDC
Block:     {block_number}
LogIndex:  {log_index}
{'-'*40}
"""

def format_whale_event(whale_event):
    return f"""
🐋 WHALE ALERT! 🐋
Wallet:      {whale_event['wallet_address']}
Tx Hash:     {whale_event['tx_hash']}
Amount:      {whale_event['amount']:,.2f} USDC
Direction:   {whale_event['direction']}
Type:        {whale_event['event_type']}
Total Volume: {whale_event['total_volume']:,.2f} USDC
Timestamp:   {whale_event['timestamp']}
{'='*50}
"""