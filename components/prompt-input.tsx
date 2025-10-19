"use client"

import type React from "react"

import { useState, useRef, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { Card } from "@/components/ui/card"
import { Mic, MicOff, Send, Loader2 } from "lucide-react"
import { useToast } from "@/hooks/use-toast"

interface PromptInputProps {
  onSubmit: (prompt: string, type: "text" | "voice") => void
  isProcessing: boolean
}

export function PromptInput({ onSubmit, isProcessing }: PromptInputProps) {
  const [prompt, setPrompt] = useState("")
  const [isRecording, setIsRecording] = useState(false)
  const [recognition, setRecognition] = useState<any>(null)
  const textareaRef = useRef<HTMLTextAreaElement>(null)
  const { toast } = useToast()

  useEffect(() => {
    // Initialize speech recognition if available
    if (typeof window !== "undefined") {
      const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition

      if (SpeechRecognition) {
        const recognitionInstance = new SpeechRecognition()
        recognitionInstance.continuous = true
        recognitionInstance.interimResults = true
        recognitionInstance.lang = "en-US"

        recognitionInstance.onresult = (event: any) => {
          const transcript = Array.from(event.results)
            .map((result: any) => result[0])
            .map((result: any) => result.transcript)
            .join("")

          setPrompt(transcript)
        }

        recognitionInstance.onerror = (event: any) => {
          console.error("[v0] Speech recognition error:", event.error)
          setIsRecording(false)
          toast({
            title: "Voice input error",
            description: "Failed to capture voice input. Please try again.",
            variant: "destructive",
          })
        }

        recognitionInstance.onend = () => {
          setIsRecording(false)
        }

        setRecognition(recognitionInstance)
      }
    }
  }, [toast])

  const handleTextSubmit = () => {
    if (prompt.trim() && !isProcessing) {
      onSubmit(prompt.trim(), "text")
      setPrompt("")
    }
  }

  const toggleRecording = () => {
    if (!recognition) {
      toast({
        title: "Voice input not supported",
        description: "Your browser doesn't support voice input.",
        variant: "destructive",
      })
      return
    }

    if (isRecording) {
      recognition.stop()
      setIsRecording(false)
      if (prompt.trim()) {
        onSubmit(prompt.trim(), "voice")
      }
    } else {
      setPrompt("")
      recognition.start()
      setIsRecording(true)
      toast({
        title: "Listening...",
        description: "Speak your prompt now",
      })
    }
  }

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault()
      handleTextSubmit()
    }
  }

  return (
    <Card className="p-4">
      <div className="space-y-4">
        <div className="space-y-2">
          <Textarea
            ref={textareaRef}
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="e.g., 'Make the title larger and change the background to blue' or 'Add bullet points to the content'"
            className="min-h-[120px] resize-none"
            disabled={isProcessing || isRecording}
          />
        </div>

        <div className="flex items-center gap-2">
          <Button
            onClick={toggleRecording}
            disabled={isProcessing}
            variant={isRecording ? "destructive" : "outline"}
            className="flex-1 h-12"
          >
            {isRecording ? <MicOff className="h-6 w-6" /> : <Mic className="h-6 w-6" />}
            <span className="sr-only">Toggle microphone</span>
          </Button>

          <Button
            onClick={handleTextSubmit}
            disabled={!prompt.trim() || isProcessing}
            size="icon"
            className="h-12 w-12"
            aria-label={isProcessing ? "Processing prompt" : "Submit prompt"}
          >
            {isProcessing ? (
              <Loader2 className="h-4 w-4 animate-spin" />
            ) : (
              <Send className="h-4 w-4" />
            )}
          </Button>
        </div>

        {isRecording && (
          <div className="flex items-center gap-2 text-sm text-muted-foreground">
            <div className="h-2 w-2 rounded-full bg-destructive animate-pulse" />
            Recording... Click the microphone button to stop
          </div>
        )}

        <div className="text-xs text-muted-foreground space-y-1">
          <p className="font-medium">Example prompts:</p>
          <ul className="list-disc list-inside space-y-1 ml-2">
            <li>Change the background color to dark blue</li>
            <li>Make the title text larger and bold</li>
            <li>Update the content to include three bullet points</li>
            <li>Center align all the text</li>
          </ul>
        </div>
      </div>
    </Card>
  )
}
