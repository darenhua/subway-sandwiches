import type { Slide } from "./types"

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"

export interface UpdateSlideRequest {
  slide: Slide
  prompt: string
}

export interface UpdateSlideResponse {
  updated_slide: Slide
  success: boolean
  message: string
}

export class APIClient {
  private baseUrl: string

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl
  }

  async updateSlide(slide: Slide, prompt: string): Promise<Slide> {
    try {
      const response = await fetch(`${this.baseUrl}/api/update-slide`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          slide,
          prompt,
        }),
      })

      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.detail || "Failed to update slide")
      }

      const data: UpdateSlideResponse = await response.json()
      return data.updated_slide
    } catch (error) {
      console.error("[v0] API Error:", error)
      throw error
    }
  }

  async healthCheck(): Promise<boolean> {
    try {
      const response = await fetch(`${this.baseUrl}/health`)
      return response.ok
    } catch (error) {
      console.error("[v0] Health check failed:", error)
      return false
    }
  }
}

export const apiClient = new APIClient()
