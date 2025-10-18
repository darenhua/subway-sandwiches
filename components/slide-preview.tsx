"use client"

import type { Slide } from "@/lib/types"
import { Card } from "@/components/ui/card"

interface SlidePreviewProps {
  slide: Slide
  className?: string
}

export function SlidePreview({ slide, className }: SlidePreviewProps) {
  const fontSize = slide.fontSize || 16

  return (
    <Card
      className={className}
      style={{
        backgroundColor: slide.backgroundColor,
        color: slide.textColor,
        padding: "2rem",
        minHeight: "400px",
        display: "flex",
        flexDirection: "column",
        justifyContent: slide.layout === "centered" ? "center" : "flex-start",
        alignItems: slide.layout === "centered" ? "center" : "flex-start",
      }}
    >
      <h1 className="font-bold mb-4" style={{ fontSize: `${fontSize * 1.5}px` }}>
        {slide.title}
      </h1>
      <div className="whitespace-pre-wrap" style={{ fontSize: `${fontSize}px` }}>
        {slide.content}
      </div>
    </Card>
  )
}
