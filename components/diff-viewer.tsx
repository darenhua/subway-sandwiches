"use client"

import type { SlideUpdate } from "@/lib/types"
import { Card } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"

interface DiffViewerProps {
  update: SlideUpdate
}

interface DiffItemProps {
  label: string
  original: string | number | undefined
  updated: string | number | undefined
  hasChanged: boolean
}

function DiffItem({ label, original, updated, hasChanged }: DiffItemProps) {
  if (!hasChanged) {
    return (
      <div className="space-y-2">
        <div className="text-sm font-medium">{label}</div>
        <div className="p-3 rounded-md bg-muted/50 text-sm">{String(original)}</div>
      </div>
    )
  }

  return (
    <div className="space-y-2">
      <div className="text-sm font-medium flex items-center gap-2">
        {label}
        <Badge variant="secondary" className="text-xs">
          Modified
        </Badge>
      </div>
      <div className="grid grid-cols-2 gap-2">
        <div className="space-y-1">
          <div className="text-xs text-muted-foreground">Original</div>
          <div className="p-3 rounded-md bg-diff-removed text-sm border border-destructive/20">{String(original)}</div>
        </div>
        <div className="space-y-1">
          <div className="text-xs text-muted-foreground">Updated</div>
          <div className="p-3 rounded-md bg-diff-added text-sm border border-accent/20">{String(updated)}</div>
        </div>
      </div>
    </div>
  )
}

function ColorDiff({ label, original, updated }: { label: string; original: string; updated: string }) {
  const hasChanged = original !== updated

  if (!hasChanged) {
    return (
      <div className="space-y-2">
        <div className="text-sm font-medium">{label}</div>
        <div className="flex items-center gap-2">
          <div className="w-12 h-12 rounded-md border" style={{ backgroundColor: original }} />
          <span className="text-sm font-mono">{original}</span>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-2">
      <div className="text-sm font-medium flex items-center gap-2">
        {label}
        <Badge variant="secondary" className="text-xs">
          Modified
        </Badge>
      </div>
      <div className="grid grid-cols-2 gap-2">
        <div className="space-y-1">
          <div className="text-xs text-muted-foreground">Original</div>
          <div className="flex items-center gap-2 p-3 rounded-md bg-diff-removed border border-destructive/20">
            <div className="w-8 h-8 rounded border" style={{ backgroundColor: original }} />
            <span className="text-sm font-mono">{original}</span>
          </div>
        </div>
        <div className="space-y-1">
          <div className="text-xs text-muted-foreground">Updated</div>
          <div className="flex items-center gap-2 p-3 rounded-md bg-diff-added border border-accent/20">
            <div className="w-8 h-8 rounded border" style={{ backgroundColor: updated }} />
            <span className="text-sm font-mono">{updated}</span>
          </div>
        </div>
      </div>
    </div>
  )
}

export function DiffViewer({ update }: DiffViewerProps) {
  const { original, updated, changes } = update

  return (
    <Card className="p-6">
      <div className="space-y-6">
        <div>
          <h3 className="text-lg font-semibold mb-2">Changes Summary</h3>
          <div className="flex flex-wrap gap-2">
            {changes.map((change, index) => (
              <Badge key={index} variant="outline">
                {change}
              </Badge>
            ))}
          </div>
        </div>

        <Tabs defaultValue="side-by-side" className="w-full">
          <TabsList className="grid w-full grid-cols-2">
            <TabsTrigger value="side-by-side">Side by Side</TabsTrigger>
            <TabsTrigger value="preview">Preview Comparison</TabsTrigger>
          </TabsList>

          <TabsContent value="side-by-side" className="space-y-4 mt-4">
            <DiffItem
              label="Title"
              original={original.title}
              updated={updated.title}
              hasChanged={original.title !== updated.title}
            />

            <DiffItem
              label="Content"
              original={original.content}
              updated={updated.content}
              hasChanged={original.content !== updated.content}
            />

            <ColorDiff label="Background Color" original={original.backgroundColor} updated={updated.backgroundColor} />

            <ColorDiff label="Text Color" original={original.textColor} updated={updated.textColor} />

            <DiffItem
              label="Font Size"
              original={original.fontSize || 16}
              updated={updated.fontSize || 16}
              hasChanged={original.fontSize !== updated.fontSize}
            />

            <DiffItem
              label="Layout"
              original={original.layout || "title-content"}
              updated={updated.layout || "title-content"}
              hasChanged={original.layout !== updated.layout}
            />
          </TabsContent>

          <TabsContent value="preview" className="space-y-4 mt-4">
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <div className="text-sm font-medium">Original</div>
                <div
                  className="p-6 rounded-md border min-h-[300px]"
                  style={{
                    backgroundColor: original.backgroundColor,
                    color: original.textColor,
                  }}
                >
                  <h2 className="font-bold mb-4" style={{ fontSize: `${(original.fontSize || 16) * 1.5}px` }}>
                    {original.title}
                  </h2>
                  <div className="whitespace-pre-wrap" style={{ fontSize: `${original.fontSize || 16}px` }}>
                    {original.content}
                  </div>
                </div>
              </div>

              <div className="space-y-2">
                <div className="text-sm font-medium">Updated</div>
                <div
                  className="p-6 rounded-md border min-h-[300px]"
                  style={{
                    backgroundColor: updated.backgroundColor,
                    color: updated.textColor,
                  }}
                >
                  <h2 className="font-bold mb-4" style={{ fontSize: `${(updated.fontSize || 16) * 1.5}px` }}>
                    {updated.title}
                  </h2>
                  <div className="whitespace-pre-wrap" style={{ fontSize: `${updated.fontSize || 16}px` }}>
                    {updated.content}
                  </div>
                </div>
              </div>
            </div>
          </TabsContent>
        </Tabs>
      </div>
    </Card>
  )
}
