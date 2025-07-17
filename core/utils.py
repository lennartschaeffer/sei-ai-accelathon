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