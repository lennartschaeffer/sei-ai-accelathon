import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Badge } from "@/components/ui/badge"
import { DollarSign, Activity, Wallet, AlertTriangle } from "lucide-react"

export function DashboardPanels() {
  const transactions = [
    { id: "0x1a2b...", from: "0xabc...", to: "0xdef...", amount: "10,000 USDC", stablecoin: "USDC", time: "2s ago" },
    { id: "0x3c4d...", from: "0xghi...", to: "0xjkl...", amount: "5,000 USDT", stablecoin: "USDT", time: "15s ago" },
    { id: "0x5e6f...", from: "0xmnp...", to: "0xqrst...", amount: "25,000 USDC", stablecoin: "USDC", time: "30s ago" },
    { id: "0x7g8h...", from: "0xuvw...", to: "0xxyz...", amount: "1,000 DAI", stablecoin: "DAI", time: "1m ago" },
    { id: "0x9i0j...", from: "0x123...", to: "0x456...", amount: "50,000 USDT", stablecoin: "USDT", time: "2m ago" },
  ]

  const whaleAlerts = [
    { id: 1, address: "0xWhale1...", type: "Large Transfer Out", amount: "5,000,000 USDC", time: "5m ago" },
    { id: 2, address: "0xWhale2...", type: "Significant Inflow", amount: "2,000,000 USDT", time: "10m ago" },
    { id: 3, address: "0xWhale3...", type: "Liquidity Pool Deposit", amount: "1,500,000 DAI", time: "15m ago" },
  ]

  const walletBalances = [
    { address: "0xMonitor1...", usdc: "1,234,567", usdt: "876,543", dai: "0" },
    { address: "0xMonitor2...", usdc: "500,000", usdt: "1,500,000", dai: "250,000" },
    { address: "0xMonitor3...", usdc: "0", usdt: "900,000", dai: "1,100,000" },
  ]

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
      {/* Live Transaction Feed */}
      <Card className="col-span-1 lg:col-span-2 bg-gray-900 border-gray-800 text-gray-50 shadow-lg shadow-purple-500/20">
        <CardHeader className="flex flex-row items-center justify-between pb-2">
          <CardTitle className="text-lg font-semibold text-purple-400 flex items-center gap-2">
            <DollarSign className="h-5 w-5" /> Live Transaction Feed
          </CardTitle>
          <Badge variant="secondary" className="bg-green-500/20 text-green-400 border-green-500/30">
            Real-time
          </Badge>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow className="border-gray-700">
                <TableHead className="text-gray-400">Tx Hash</TableHead>
                <TableHead className="text-gray-400">From</TableHead>
                <TableHead className="text-gray-400">To</TableHead>
                <TableHead className="text-gray-400 text-right">Amount</TableHead>
                <TableHead className="text-gray-400 text-right">Time</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {transactions.map((tx, index) => (
                <TableRow key={index} className="border-gray-800 hover:bg-gray-800/50">
                  <TableCell className="font-medium text-cyan-400">{tx.id.substring(0, 8)}...</TableCell>
                  <TableCell className="text-gray-300">{tx.from.substring(0, 8)}...</TableCell>
                  <TableCell className="text-gray-300">{tx.to.substring(0, 8)}...</TableCell>
                  <TableCell className="text-right text-emerald-400">{tx.amount}</TableCell>
                  <TableCell className="text-right text-gray-400">{tx.time}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>

      {/* Whale Activity Alerts */}
      <Card className="col-span-1 bg-gray-900 border-gray-800 text-gray-50 shadow-lg shadow-purple-500/20">
        <CardHeader className="flex flex-row items-center justify-between pb-2">
          <CardTitle className="text-lg font-semibold text-purple-400 flex items-center gap-2">
            <AlertTriangle className="h-5 w-5" /> Whale Activity Alerts
          </CardTitle>
          <Badge variant="secondary" className="bg-red-500/20 text-red-400 border-red-500/30">
            High Impact
          </Badge>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {whaleAlerts.map((alert) => (
              <div
                key={alert.id}
                className="flex items-start gap-3 p-3 rounded-md bg-gray-800/50 border border-gray-700"
              >
                <Activity className="h-5 w-5 text-yellow-400 shrink-0 mt-1" />
                <div>
                  <p className="text-sm font-medium text-gray-200">
                    {alert.type}: <span className="text-emerald-400">{alert.amount}</span>
                  </p>
                  <p className="text-xs text-gray-400">
                    Address: <span className="text-cyan-400">{alert.address.substring(0, 12)}...</span>
                  </p>
                  <p className="text-xs text-gray-500">{alert.time}</p>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Monitored Wallet Balances */}
      <Card className="col-span-1 lg:col-span-3 bg-gray-900 border-gray-800 text-gray-50 shadow-lg shadow-purple-500/20">
        <CardHeader className="flex flex-row items-center justify-between pb-2">
          <CardTitle className="text-lg font-semibold text-purple-400 flex items-center gap-2">
            <Wallet className="h-5 w-5" /> Monitored Wallet Balances
          </CardTitle>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow className="border-gray-700">
                <TableHead className="text-gray-400">Wallet Address</TableHead>
                <TableHead className="text-gray-400 text-right">USDC</TableHead>
                <TableHead className="text-gray-400 text-right">USDT</TableHead>
                <TableHead className="text-gray-400 text-right">DAI</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {walletBalances.map((wallet, index) => (
                <TableRow key={index} className="border-gray-800 hover:bg-gray-800/50">
                  <TableCell className="font-medium text-cyan-400">{wallet.address.substring(0, 12)}...</TableCell>
                  <TableCell className="text-right text-emerald-400">{wallet.usdc}</TableCell>
                  <TableCell className="text-right text-emerald-400">{wallet.usdt}</TableCell>
                  <TableCell className="text-right text-emerald-400">{wallet.dai}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  )
}
