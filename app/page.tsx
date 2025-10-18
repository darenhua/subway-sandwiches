import { SlideEditor } from "@/components/slide-editor"
import type { Slide } from "@/lib/types"

const initialSlide: Slide = {
  id: "1",
  title: "Welcome to AI Slide Editor",
  content: "Use text or voice prompts to update your slides with AI assistance. Review changes before applying them.",
  backgroundColor: "#ffffff",
  textColor: "#000000",
  fontSize: 16,
  layout: "title-content",
}

export default function Page() {
  return (
    <main className="min-h-screen bg-background">
      <SlideEditor initialSlide={initialSlide} />
    </main>
  )
}
