# Speech-to-Text Pipeline & Database Linking Demo

Proof-of-concept pipeline demonstrating speech transcription, confidence scoring, live microphone capture, and database schema linking for voice notes.

## Overview
- **Whisper Model Spike (`demo_whisper.py`):** Runs OpenAI's Whisper model locally on CPU to evaluate segment timestamps and confidence log-probabilities (`avg_logprob`).
- **Live Microphone Demo (`demo_live_mic.py`):** Captures real-time audio from the device microphone, transcribes the recording, flags low-confidence segments, and automatically writes the structured record into SQLite.
- **Native Mobile Pipeline (`demo_native_pipeline.py`):** Simulates on-device speech engine output (iOS `SFSpeechRecognizer` / Android `SpeechRecognizer`) to test data ingestion without loading heavy neural network weights into mobile RAM.
- **Schema & Graph Linking (`schema.sql`):** Persists audio files (`audio_media`) and transcriptions (`text_notes`) as independent entities connected by `TRANSCRIBED_FROM` graph edges (`note_edges`).

## Setup & Running

1. **Activate virtual environment:**
source venv/bin/activate

2. **Install dependencies:**
pip install openai-whisper sounddevice scipy
*(Note: Whisper also requires system ffmpeg installed).*

3. **Run Live Microphone Demo:**
python3 demo_live_mic.py
Records 5 seconds of audio from the MacBook microphone, runs transcription, evaluates confidence thresholds, and stores the linked records in SQLite.

4. **Run Native Mobile Pipeline Simulation:**
python3 demo_native_pipeline.py
Validates the incoming JSON payload from native mobile speech recognizers and verifies database graph edge insertion.

5. **Run Base File Transcription:**
python demo_whisper.py

## Database Schema (`schema.sql`)
- `audio_media`: Tracks the raw recorded audio asset path and duration.
- `text_notes`: Stores the generated transcript as an independent note with its confidence score and `needs_review` flag.
- `note_edges`: Links the parent audio entity to the independent text note using `TRANSCRIBED_FROM` relationship edges for graph queries.
