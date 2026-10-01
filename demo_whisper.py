import os
import json
import whisper

def run_demo(audio_path: str):
    if not os.path.exists(audio_path):
        print(f"Error: Could not find audio file at '{audio_path}'")
        return

    print("=" * 60)
    print("1. Loading Whisper 'base' model...")
    # 'base' or 'tiny' are ideal for quick laptop CPU execution
    model = whisper.load_model("base")

    print(f"2. Transcribing audio file: {audio_path}")
    # verbose=False keeps the console clean for our custom summary
    result = model.transcribe(audio_path, verbose=False)

    print("\n" + "=" * 60)
    print("DEMO RESULTS: SPEECH-TO-TEXT PIPELINE")
    print("=" * 60)
    print(f"Detected Language : {result.get('language', 'unknown').upper()}")
    print(f"Full Transcription: \"{result['text'].strip()}\"\n")

    print("-" * 60)
    print("SEGMENT BREAKDOWN (TIMESTAMPS & CONFIDENCE)")
    print("-" * 60)
    
    # Simulate low-confidence threshold flagging for your research
    LOW_CONFIDENCE_THRESHOLD = -0.60

    for i, segment in enumerate(result.get("segments", []), start=1):
        start = segment["start"]
        end = segment["end"]
        text = segment["text"].strip()
        avg_logprob = segment.get("avg_logprob", 0.0)

        # Flag segments that might need human review
        flag = " [NEEDS REVIEW]" if avg_logprob < LOW_CONFIDENCE_THRESHOLD else " [OK]"

        print(f"[{start:05.2f}s -> {end:05.2f}s] {text}")
        print(f"   ↳ avg_logprob: {avg_logprob:.3f}{flag}")

    # Simulate generating the linked independent Text Object for your database
    print("\n" + "-" * 60)
    print("SIMULATED DATABASE PAYLOAD (INDEPENDENT TEXT OBJECT)")
    print("-" * 60)
    payload = {
        "object_type": "text_transcription",
        "parent_audio_ref": os.path.basename(audio_path),
        "transcript": result["text"].strip(),
        "language": result.get("language"),
        "confidence_ok": all(s.get("avg_logprob", 0.0) >= LOW_CONFIDENCE_THRESHOLD for s in result.get("segments", []))
    }
    print(json.dumps(payload, indent=2))
    print("=" * 60)

if __name__ == "__main__":
    # Point this to any short .mp3, .wav, or .m4a voice memo file
    sample_file = "test_memo.mp4"
    run_demo(sample_file)