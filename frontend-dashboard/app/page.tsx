import { DragonEye } from "@/components/dragon-eye"
import { DashboardPanels } from "@/components/dashboard-panels"

export default function HomePage() {
  return (
    <div className="min-h-screen bg-gray-950 text-gray-50 antialiased">
      <div className="container mx-auto px-4 py-8">
        <header className="text-center mb-12">
          <h1 className="text-4xl font-bold tracking-tight sm:text-5xl lg:text-6xl text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-cyan-400 drop-shadow-lg">
            Sei Stablecoin Monitor
          </h1>
          <p className="mt-4 text-lg text-gray-400">
            Real-time insights into on-chain stablecoin flows and whale activity.
          </p>
        </header>

        <div className="relative flex justify-center mb-16">
          <DragonEye />
        </div>

        <DashboardPanels />
      </div>
    </div>
  )
}
