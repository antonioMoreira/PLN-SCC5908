export function recordAudio(stream: MediaStream): () => Promise<Blob> {
  // Create a MediaRecorder instance to record audio
  const mediaRecorder = new MediaRecorder(stream);

  // Array to store the recorded audio chunks
  const audioChunks: BlobPart[] = [];

  // Event handler for when data becomes available
  mediaRecorder.ondataavailable = (event: BlobEvent) => {
    if (event.data.size > 0) {
      audioChunks.push(event.data);
    }
  };

  // Start recording
  mediaRecorder.start();

  // Return a function that stops recording and returns the result
  return (): Promise<Blob> => {
    return new Promise((resolve) => {
      mediaRecorder.onstop = () => {
        // Combine all audio chunks into a single Blob
        const audioBlob = new Blob(audioChunks, { type: "audio/wav" });
        resolve(audioBlob);
      };

      // Stop recording
      mediaRecorder.stop();
    });
  };
}
