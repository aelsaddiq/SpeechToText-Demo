import json
import sqlite3
import numpy as np
import sounddevice as sd
from scipy.io.wavfile import write
import whisper

SAMPLE_RATE = 16000
DURATION = 5  # seconds to record
OUTPUT_FILENAME = "mic_recording.wav"

print(f"\n[+] Preparing to record from MacBook microphone for {DURATION} seconds...")
print("[*] Speak now...")

# Record audio from default Mac microphone
recording = sd.rec(int(DURATION * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1, dtype="int16")
sd.wait()

print("[+] Recording complete. Saving to", OUTPUT_FILENAME)
write(OUTPUT_FILENAME, SAMPLE_RATE, recording)

print("[+] Loading Whisper model to transcribe live audio...")
model = whisper.load_model("tiny")
result = model.transcribe(OUTPUT_FILENAME, fp16=False)

full_transcript = result.get("text", "").strip()
segments = result.get("segments", [])

avg_logprob = segments[0].get("avg_logprob", 0.0) if segments else -1.0
needs_review = avg_logprob < -0.60

print("\n--- Live Transcription Result ---")
print(f"Transcript: \"{full_transcript}\"")
print(f"Log-probability (Confidence): {avg_logprob:.2f}")
print(f"Needs Review Flag: {needs_review}")

# Insert directly into SQLite schema
conn = sqlite3.connect(":memory:")
cursor = conn.cursor()

with open("schema.sql", "r") as f:
    cursor.executescript(f.read())

audio_id = "audio_live_mic_001"
note_id = "note_live_101"

cursor.execute(
    "INSERT INTO audio_media (audio_id, file_path, duration_seconds) VALUES (?, ?, ?)",
    (audio_id, OUTPUT_FILENAME, float(DURATION))
)

cursor.execute(
    "INSERT INTO text_notes (note_id, parent_audio_ref, transcript_text, confidence_score, needs_review) VALUES (?, ?, ?, ?, ?)",
    (note_id, audio_id, full_transcript, float(avg_logprob), needs_review)
)

cursor.execute(
    "INSERT INTO note_edges (source_id, target_id, relationship_type) VALUES (?, ?, ?)",
    (audio_id, note_id, "TRANSCRIBED_FROM")
)
conn.commit()

print("\n--- Verified In-Memory Database Record ---")
cursor.execute("SELECT note_id, parent_audio_ref, transcript_text, confidence_score, needs_review FROM text_notes")
print("Persisted Text Note:", cursor.fetchone())

cursor.execute("SELECT source_id, target_id, relationship_type FROM note_edges")
print("Graph Link Edge:", cursor.fetchone())
print("\n[+] Success: Live voice note transcribed and linked to schema successfully!\n")
