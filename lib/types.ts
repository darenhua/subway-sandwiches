export interface Slide {
  id: string
  title: string
  content: string
  backgroundColor: string
  textColor: string
  fontSize?: number
  layout?: "title-content" | "centered" | "two-column"
}

export interface SlideUpdate {
  original: Slide
  updated: Slide
  changes: string[]
  timestamp: number
}

export interface PromptHistory {
  id: string
  prompt: string
  timestamp: number
  type: "text" | "voice"
}
