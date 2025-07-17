from mcp import StdioServerParameters

STABLECOIN_ADDRESSES = {
    "USDC": "0x3894085ef7ff0f0aedf52e2a2704928d1ec074f1",
}

NETWORK = "sei"
POLL_INTERVAL = 5
USDC_DECIMALS = 6

SERVER_PARAMS = StdioServerParameters(
    command="npx",
    args=["-y", "@sei-js/mcp-server"],
    env=None,
)