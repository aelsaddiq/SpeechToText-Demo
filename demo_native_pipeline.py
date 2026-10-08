import json
import sqlite3

# 1. Mock payload coming from iOS SFSpeechRecognizer / @react-native-voice/voice
native_speech_payload = {
    "parent_audio_ref": "audio_ios_rec_001",
    "engine": "Apple Speech.framework (SFSpeechRecognizer)",
    "transcript": "Meeting with advisor regarding database linking",
    "confidence": 0.88,
    "segments": [
        {"text": "Meeting with advisor", "start": 0.0, "end": 1.2, "confidence": 0.92},
        {"text": "regarding database linking", "start": 1.3, "end": 2.8, "confidence": 0.84}
    ]
}

print("\n--- 1. Native Mobile S2T Output Received ---")
print(json.dumps(native_speech_payload, indent=2))

# 2. Simulate inserting into our local database schema (schema.sql)
conn = sqlite3.connect(":memory:")
cursor = conn.cursor()

# Execute our schema
with open("schema.sql", "r") as f:
    cursor.executescript(f.read())

# Insert parent audio media
cursor.execute(
    "INSERT INTO audio_media (audio_id, file_path, duration_seconds) VALUES (?, ?, ?)",
    (native_speech_payload["parent_audio_ref"], "/storage/audio_001.m4a", 2.8)
)

# Insert independent text note linked to parent audio
needs_review = native_speech_payload["confidence"] < 0.60
cursor.execute(
    "INSERT INTO text_notes (note_id, parent_audio_ref, transcript_text, confidence_score, needs_review) VALUES (?, ?, ?, ?, ?)",
    ("note_txt_101", native_speech_payload["parent_audio_ref"], native_speech_payload["transcript"], native_speech_payload["confidence"], needs_review)
)

# Insert graph relationship edge
cursor.execute(
    "INSERT INTO note_edges (source_id, target_id, relationship_type) VALUES (?, ?, ?)",
    ("audio_ios_rec_001", "note_txt_101", "TRANSCRIBED_FROM")
)
conn.commit()

print("\n--- 2. Database Insertion Verified ---")
cursor.execute("SELECT note_id, parent_audio_ref, transcript_text, confidence_score, needs_review FROM text_notes")
print("Persisted Text Note:", cursor.fetchone())

cursor.execute("SELECT source_id, target_id, relationship_type FROM note_edges")
print("Graph Link Edge:", cursor.fetchone())
print("\n[+] Success: Native speech output successfully linked to schema!\n")
