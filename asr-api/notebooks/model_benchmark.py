from datasets import load_dataset
from faster_whisper import WhisperModel
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
import numpy as np
from tqdm import tqdm
import torchaudio
import torch

WHISPER_MODEL_SIZE = "large-v3"

assert torch.cuda.is_available(), "CUDA is not available. Please check your PyTorch installation."

print(f"Loading Faster-Whisper model {WHISPER_MODEL_SIZE}...", flush=True)
model = WhisperModel(WHISPER_MODEL_SIZE, device="cuda", compute_type="float16")
print("Model loaded.", flush=True)

print("Loading dataset...", flush=True)
cv_17 = load_dataset("mozilla-foundation/common_voice_17_0", "pt", split="train")
print("Done.", flush=True)

# cv_17_sample = cv_17.select(range(100))

# Initialize lists to store results
references = []
hypotheses = []
bleu_scores = []
transcriptions = []

# Smoothing function for BLEU
smoother = SmoothingFunction().method1

def resample_audio(audio_array, original_sr, target_sr=16000):
    tensor = torch.FloatTensor(audio_array).unsqueeze(0)
    resampled = torchaudio.functional.resample(
        tensor, 
        orig_freq=original_sr, 
        new_freq=target_sr
    )
    return resampled.squeeze(0).cpu().detach().numpy()

for sample in tqdm(cv_17, desc="Processing samples"):
    audio = sample["audio"]
    ground_truth = sample["sentence"]
    
    # Resample if needed
    if audio["sampling_rate"] != 16000:
        audio_array = resample_audio(
            audio["array"], 
            audio["sampling_rate"], 
            target_sr=16000
        )
    else:
        audio_array = audio["array"]

    # Run Whisper inference
    segments, _ = model.transcribe(audio_array, language="pt")
    
    # Combine all segments into one transcription
    transcription = " ".join([segment.text for segment in segments])
    
    # Store reference and hypothesis
    references.append(ground_truth.split())
    hypotheses.append(transcription.split())
    transcriptions.append(transcription)
    
    # Calculate BLEU score for this sample
    bleu = sentence_bleu(
        [ground_truth.split()], 
        transcription.split(), 
        smoothing_function=smoother
    )
    bleu_scores.append(bleu)
    
# Calculate overall statistics
avg_bleu = np.mean(bleu_scores)
median_bleu = np.median(bleu_scores)
std_bleu = np.std(bleu_scores)

print("\nFinal Evaluation Results:", flush=True)
print(f"Average BLEU: {avg_bleu:.4f}")
print(f"Median BLEU: {median_bleu:.4f}")
print(f"BLEU Std Dev: {std_bleu:.4f}")

cv_17_df = cv_17.to_pandas()
cv_17_df['whisper_transcription'] = transcriptions
cv_17_df['bleu_score'] = bleu_scores
cv_17_df.to_csv("cv_17_processed.csv", index=False)

# Final Evaluation Results:
# Average BLEU: 0.3193
# Median BLEU: 0.1729
# BLEU Std Dev: 0.3315
# Em um teste com o whisper large-v3 em um sample menor (100 instâncias), tivemos:
# Average BLEU: 0.5