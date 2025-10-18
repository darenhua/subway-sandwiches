import type { Slide, SlideUpdate } from "./types"

export function detectChanges(original: Slide, updated: Slide): string[] {
  const changes: string[] = []

  if (original.title !== updated.title) {
    changes.push("Title updated")
  }
  if (original.content !== updated.content) {
    changes.push("Content updated")
  }
  if (original.backgroundColor !== updated.backgroundColor) {
    changes.push("Background color changed")
  }
  if (original.textColor !== updated.textColor) {
    changes.push("Text color changed")
  }
  if (original.fontSize !== updated.fontSize) {
    changes.push("Font size adjusted")
  }
  if (original.layout !== updated.layout) {
    changes.push("Layout changed")
  }

  return changes
}

export function createSlideUpdate(original: Slide, updated: Slide): SlideUpdate {
  return {
    original,
    updated,
    changes: detectChanges(original, updated),
    timestamp: Date.now(),
  }
}

export function generateSlideId(): string {
  return `slide-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`
}
