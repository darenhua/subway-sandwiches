"use client"

import { useState, useEffect } from "react"
import type { Slide, SlideUpdate } from "@/lib/types"
import { SlidePreview } from "./slide-preview"
import { PromptInput } from "./prompt-input"
import { ApprovalDialog } from "./approval-dialog"
import { DiffViewer } from "./diff-viewer"
import { ResizablePanelGroup, ResizablePanel, ResizableHandle } from "@/components/ui/resizable"
import { apiClient } from "@/lib/api-client"
import { createSlideUpdate } from "@/lib/slide-utils"
import { useToast } from "@/hooks/use-toast"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { AlertCircle, CheckCircle2 } from "lucide-react"

interface SlideEditorProps {
  initialSlide: Slide
}

export function SlideEditor({ initialSlide }: SlideEditorProps) {
  const [currentSlide, setCurrentSlide] = useState<Slide>(initialSlide)
  const [pendingUpdate, setPendingUpdate] = useState<SlideUpdate | null>(null)
  const [isProcessing, setIsProcessing] = useState(false)
  const [backendStatus, setBackendStatus] = useState<"checking" | "connected" | "disconnected">("checking")
  const { toast } = useToast()

  useEffect(() => {
    const checkBackend = async () => {
      const isHealthy = await apiClient.healthCheck()
      setBackendStatus(isHealthy ? "connected" : "disconnected")
    }
    checkBackend()
  }, [])

  const handlePromptSubmit = async (prompt: string, type: "text" | "voice") => {
    setIsProcessing(true)
    try {
      const updatedSlide = await apiClient.updateSlide(currentSlide, prompt)
      const slideUpdate = createSlideUpdate(currentSlide, updatedSlide)

      setPendingUpdate(slideUpdate)

      toast({
        title: "Slide updated",
        description: "Review the changes and approve or reject them.",
      })
    } catch (error) {
      console.error("[v0] Error processing prompt:", error)
      toast({
        title: "Error",
        description: error instanceof Error ? error.message : "Failed to process your prompt. Please try again.",
        variant: "destructive",
      })
    } finally {
      setIsProcessing(false)
    }
  }

  const handleApprove = () => {
    if (pendingUpdate) {
      setCurrentSlide(pendingUpdate.updated)
      setPendingUpdate(null)
      toast({
        title: "Changes applied",
        description: "Your slide has been updated successfully.",
      })
    }
  }

  const handleReject = () => {
    setPendingUpdate(null)
    toast({
      title: "Changes rejected",
      description: "The slide remains unchanged.",
    })
  }

  return (
    <div className="h-screen flex flex-col">
      <header className="border-b bg-card px-6 py-4">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold">AI Slide Editor</h1>
            <p className="text-sm text-muted-foreground">Edit your slides with natural language prompts</p>
          </div>
          <div className="flex items-center gap-2">
            {backendStatus === "connected" && (
              <div className="flex items-center gap-2 text-sm text-green-600">
                <CheckCircle2 className="h-4 w-4" />
                <span>Backend Connected</span>
              </div>
            )}
            {backendStatus === "disconnected" && (
              <div className="flex items-center gap-2 text-sm text-destructive">
                <AlertCircle className="h-4 w-4" />
                <span>Backend Disconnected</span>
              </div>
            )}
          </div>
        </div>
      </header>

      {backendStatus === "disconnected" && (
        <Alert variant="destructive" className="m-4">
          <AlertCircle className="h-4 w-4" />
          <AlertDescription>
            Cannot connect to Python backend. Make sure the backend server is running on port 8000.
          </AlertDescription>
        </Alert>
      )}

      <div className="flex-1 overflow-hidden">
        <ResizablePanelGroup direction="horizontal" className="h-full">
          <ResizablePanel defaultSize={60} minSize={30}>
            <div className="h-full p-6 overflow-auto">
              <div className="max-w-4xl mx-auto">
                <h2 className="text-lg font-semibold mb-4">Current Slide</h2>
                <SlidePreview slide={currentSlide} />

                {pendingUpdate && (
                  <div className="mt-6">
                    <h2 className="text-lg font-semibold mb-4">Proposed Changes</h2>
                    <DiffViewer update={pendingUpdate} />
                  </div>
                )}
              </div>
            </div>
          </ResizablePanel>

          <ResizableHandle withHandle />

          <ResizablePanel defaultSize={40} minSize={30}>
            <div className="h-full p-6 overflow-auto bg-muted/30">
              <div className="max-w-2xl mx-auto">
                <h2 className="text-lg font-semibold mb-4">Edit with AI</h2>
                <PromptInput onSubmit={handlePromptSubmit} isProcessing={isProcessing} />
              </div>
            </div>
          </ResizablePanel>
        </ResizablePanelGroup>
      </div>

      {pendingUpdate && <ApprovalDialog update={pendingUpdate} onApprove={handleApprove} onReject={handleReject} />}
    </div>
  )
}
