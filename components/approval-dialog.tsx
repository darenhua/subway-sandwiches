"use client"

import type { SlideUpdate } from "@/lib/types"
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from "@/components/ui/alert-dialog"
import { Badge } from "@/components/ui/badge"
import { Check, X } from "lucide-react"

interface ApprovalDialogProps {
  update: SlideUpdate
  onApprove: () => void
  onReject: () => void
}

export function ApprovalDialog({ update, onApprove, onReject }: ApprovalDialogProps) {
  const { changes } = update

  return (
    <AlertDialog open={true}>
      <AlertDialogContent className="max-w-2xl">
        <AlertDialogHeader>
          <AlertDialogTitle>Review AI Changes</AlertDialogTitle>
          <AlertDialogDescription>
            The AI has proposed the following changes to your slide. Review them carefully before applying.
          </AlertDialogDescription>
        </AlertDialogHeader>

        <div className="py-4">
          <div className="space-y-4">
            <div>
              <h4 className="text-sm font-medium mb-2">Changes Made:</h4>
              <div className="flex flex-wrap gap-2">
                {changes.map((change, index) => (
                  <Badge key={index} variant="secondary">
                    {change}
                  </Badge>
                ))}
              </div>
            </div>

            <div className="p-4 rounded-lg bg-muted/50 space-y-2">
              <p className="text-sm font-medium">Preview:</p>
              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-1">
                  <p className="text-xs text-muted-foreground">Before</p>
                  <div
                    className="p-3 rounded border text-xs"
                    style={{
                      backgroundColor: update.original.backgroundColor,
                      color: update.original.textColor,
                    }}
                  >
                    <div className="font-bold mb-1">{update.original.title}</div>
                    <div className="line-clamp-3">{update.original.content}</div>
                  </div>
                </div>
                <div className="space-y-1">
                  <p className="text-xs text-muted-foreground">After</p>
                  <div
                    className="p-3 rounded border text-xs"
                    style={{
                      backgroundColor: update.updated.backgroundColor,
                      color: update.updated.textColor,
                    }}
                  >
                    <div className="font-bold mb-1">{update.updated.title}</div>
                    <div className="line-clamp-3">{update.updated.content}</div>
                  </div>
                </div>
              </div>
            </div>

            <div className="text-xs text-muted-foreground">
              <p>
                <strong>Tip:</strong> You can see detailed changes in the diff viewer below the current slide.
              </p>
            </div>
          </div>
        </div>

        <AlertDialogFooter>
          <AlertDialogCancel onClick={onReject} className="gap-2">
            <X className="h-4 w-4" />
            Reject Changes
          </AlertDialogCancel>
          <AlertDialogAction onClick={onApprove} className="gap-2">
            <Check className="h-4 w-4" />
            Apply Changes
          </AlertDialogAction>
        </AlertDialogFooter>
      </AlertDialogContent>
    </AlertDialog>
  )
}
