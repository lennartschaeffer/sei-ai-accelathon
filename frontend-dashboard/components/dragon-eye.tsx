"use client"

import { useState, useEffect } from "react"
import { cn } from "@/lib/utils"

export function DragonEye() {
  const [isBlinking, setIsBlinking] = useState(false)

  useEffect(() => {
    const blinkInterval = setInterval(
      () => {
        setIsBlinking(true)
        const blinkDuration = 300 // Duration of the blink animation
        setTimeout(() => {
          setIsBlinking(false)
        }, blinkDuration)
      },
      Math.random() * 5000 + 3000,
    ) // Blinks every 3-8 seconds

    return () => clearInterval(blinkInterval)
  }, [])

  return (
    <div className="relative w-64 h-32 sm:w-80 sm:h-40 lg:w-96 lg:h-48 overflow-hidden rounded-[50%] bg-gradient-to-br from-gray-800 to-gray-900 shadow-2xl shadow-purple-500/30 flex items-center justify-center">
      {/* Eye Outline / Sclera */}
      <div className="relative w-[90%] h-[70%] rounded-[50%] bg-gray-700 shadow-inner shadow-gray-900/50 flex items-center justify-center">
        {/* Iris */}
        <div className="relative w-2/3 h-2/3 rounded-full bg-gradient-to-br from-green-500 to-emerald-700 shadow-lg shadow-green-500/50 animate-eye-move flex items-center justify-center">
          {/* Pupil */}
          <div className="w-1/3 h-1/3 rounded-full bg-gray-900 shadow-inner shadow-gray-700/50" />
          {/* Light reflection */}
          <div className="absolute top-1/4 left-1/4 w-1/6 h-1/6 rounded-full bg-white opacity-70 blur-[1px]" />
        </div>

        {/* Eyelids */}
        <div
          className={cn(
            "absolute inset-0 rounded-[50%] bg-gray-950 transition-transform duration-300 ease-in-out",
            isBlinking ? "scale-y-100" : "scale-y-0",
          )}
          style={{ transformOrigin: "center center" }}
        >
          <div className="absolute top-0 left-0 w-full h-1/2 bg-gray-950 rounded-t-[50%] origin-bottom" />
          <div className="absolute bottom-0 left-0 w-full h-1/2 bg-gray-950 rounded-b-[50%] origin-top" />
        </div>
      </div>
    </div>
  )
}
