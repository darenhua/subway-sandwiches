"use server"

import { generateObject } from "ai"
import type { Slide } from "@/lib/types"
import { z } from "zod"

const slideSchema = z.object({
  title: z.string(),
  content: z.string(),
  backgroundColor: z.string(),
  textColor: z.string(),
  fontSize: z.number().optional(),
  layout: z.enum(["title-content", "centered", "two-column"]).optional(),
})

export async function updateSlideWithAI(currentSlide: Slide, prompt: string): Promise<Slide> {
  try {
    const { object } = await generateObject({
      model: "openai/gpt-4o-mini",
      schema: slideSchema,
      prompt: `You are a presentation slide editor. Given the current slide and a user prompt, update the slide accordingly.

Current slide:
- Title: ${currentSlide.title}
- Content: ${currentSlide.content}
- Background Color: ${currentSlide.backgroundColor}
- Text Color: ${currentSlide.textColor}
- Font Size: ${currentSlide.fontSize || 16}
- Layout: ${currentSlide.layout || "title-content"}

User prompt: ${prompt}

Update the slide based on the user's request. Make sure:
1. Colors are valid hex codes (e.g., #ffffff, #000000)
2. Font sizes are reasonable (12-48px)
3. Content is well-formatted and clear
4. If the user asks for bullet points, format them with • or - symbols
5. Maintain professional presentation standards

Return the updated slide properties.`,
    })

    return {
      ...currentSlide,
      ...object,
    }
  } catch (error) {
    console.error("[v0] AI update error:", error)
    throw new Error("Failed to update slide with AI")
  }
}
