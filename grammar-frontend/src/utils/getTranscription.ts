export async function getTranscription(
  base64: string
): Promise<string | Error> {
  const response = await fetch("/api/transcribe", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ audio: base64 }),
  });

  if (!response.ok) {
    return new Error("Failed to transcribe audio");
  }

  const data = await response.json();
  return data.transcription;
}
