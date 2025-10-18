// src/lib/cubby.ts
import { createClient, type CubbyClient } from "@cubby/js";

/**
 * Cubby client configured via env vars.
 * Make sure to set:
 *  - CUBBY_CLIENT_ID
 *  - CUBBY_CLIENT_SECRET
 */
export const cubby: CubbyClient = createClient({
  baseUrl: "https://api.cubby.sh",
  clientId: process.env.CUBBY_CLIENT_ID!,
  clientSecret: process.env.CUBBY_CLIENT_SECRET!,
});

/**
 * Pick a device to read from.
 * By default, chooses the first available device unless you pass an explicit deviceId.
 */
export async function selectDevice(deviceId?: string) {
  const { devices } = await cubby.listDevices();
  if (!devices?.length) {
    throw new Error("No Cubby devices found. Is the Cubby agent running on your machine?");
  }
  const chosen = deviceId ? devices.find(d => d.id === deviceId) ?? devices[0] : devices[0];
  cubby.setDeviceId(chosen.id);
  return chosen;
}

/**
 * Stream live mic transcriptions from the selected device and hand each transcript
 * to your app's AI processing function.
 *
 * Usage:
 *   await startCubbyTranscriptionStream(async (text) => {
 *     // Call your AI model here (OpenAI, local, etc.)
 *     await processTranscriptWithAI(text);
 *   });
 */
export async function startCubbyTranscriptionStream(
  onTranscript: (text: string) => Promise<void> | void,
  opts: { deviceId?: string } = {}
) {
  const device = await selectDevice(opts.deviceId);

  // Stream live transcription events
  for await (const event of cubby.streamTranscriptions()) {
    const text = event?.text?.trim();
    if (!text) continue;

    try {
      await onTranscript(text);
    } catch (err) {
      console.error("[Cubby] onTranscript handler failed:", err);
    }
  }

  return device;
}

/**
 * Simple helper to search historical transcripts (OCR or audio).
 */
export async function searchTranscripts(query: string, limit = 10) {
  await selectDevice(); // ensure a device is set
  return cubby.search({ q: query, content_type: "ocr", limit });
}

/**
 * Example: adapter you can implement in your app to send the transcript
 * to your AI model endpoint. Replace the fetch URL with your own route.
 */
export async function processTranscriptWithAI(text: string) {
  // Replace this with your own model call (OpenAI, local model, etc.)
  // Example assumes you expose a server route at /api/ai/process
  const res = await fetch(`${process.env.AI_PROCESS_URL ?? "http://localhost:3000"}/api/ai/process`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text }),
  });

  if (!res.ok) {
    const body = await res.text().catch(() => "");
    throw new Error(`AI processor returned ${res.status} ${res.statusText}: ${body}`);
  }

  return res.json().catch(() => ({}));
}
