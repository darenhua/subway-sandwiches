import React, { useEffect, useRef, useState } from "react";

export default function Recorder() {
  const [recording, setRecording] = useState(false);
  const [permission, setPermission] = useState(false);
  const [transcript, setTranscript] = useState<string | null>(null);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const chunksRef = useRef<Blob[]>([]);

  useEffect(() => {
    navigator.mediaDevices
      .getUserMedia({ audio: true })
      .then(() => setPermission(true))
      .catch(() => setPermission(false));
  }, []);

  const start = async () => {
    if (!permission) return alert("Microphone permission is required");
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    const mr = new MediaRecorder(stream);
    mediaRecorderRef.current = mr;
    chunksRef.current = [];
    mr.ondataavailable = (e) => chunksRef.current.push(e.data);
    mr.onstop = async () => {
      const blob = new Blob(chunksRef.current, { type: "audio/webm" });
      // send to backend
      const fd = new FormData();
      fd.append("file", blob, "recording.webm");
      try {
        const res = await fetch("/api/transcribe", {
          method: "POST",
          body: fd,
        });
        if (!res.ok) throw new Error(await res.text());
        const json = await res.json();
        setTranscript(json.text || JSON.stringify(json));
      } catch (e: any) {
        setTranscript("Error: " + (e.message || String(e)));
      }
    };
    mr.start();
    setRecording(true);
  };

  const stop = () => {
    if (!mediaRecorderRef.current) return;
    mediaRecorderRef.current.stop();
    setRecording(false);
  };

  return (
    <div style={{ padding: 16, border: "1px solid #ddd", borderRadius: 8 }}>
      <h3>Recorder</h3>
      <p>Microphone permission: {permission ? "granted" : "denied"}</p>
      <div>
        {!recording ? (
          <button onClick={start}>Start Recording</button>
        ) : (
          <button onClick={stop}>Stop Recording</button>
        )}
      </div>
      <div style={{ marginTop: 12 }}>
        <strong>Transcription:</strong>
        <pre style={{ whiteSpace: "pre-wrap" }}>
          {transcript ?? "(none yet)"}
        </pre>
      </div>
    </div>
  );
}
