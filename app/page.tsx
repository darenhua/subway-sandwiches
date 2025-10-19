import { SlideEditor } from "@/components/slide-editor"
import type { Slide } from "@/lib/types"

const initialSlide: Slide = {
  id: "1",
  title: "Replace with first slide content",
  content: "",
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
