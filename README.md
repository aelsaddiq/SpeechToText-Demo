# Whisper Speech-to-Text Pipeline Demo

Proof-of-concept pipeline demonstrating local speech transcription, timestamp extraction, and confidence scoring using OpenAI's Whisper model.

## Overview
- Local Model Execution: Uses the Whisper base model to transcribe short audio memos locally on CPU.
- Segment Timestamps: Captures exact start and end timestamps for audio synchronization.
- Confidence Flagging: Evaluates segment log-probabilities (avg_logprob) to flag low-confidence text for human review.
- Independent Object Linking: Formats transcribed output as an autonomous data object referencing parent media.

## Setup & Running
1. Create and activate virtual environment:
   python3 -m venv venv
   source venv/bin/activate

2. Install dependencies (requires system ffmpeg):
   pip install openai-whisper

3. Run demo:
   python demo_whisper.py
