-- Database Schema for Audio Notes and Linked Transcriptions

CREATE TABLE IF NOT EXISTS audio_media (
    audio_id VARCHAR(64) PRIMARY KEY,
    file_path VARCHAR(255) NOT NULL,
    duration_seconds FLOAT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS text_notes (
    note_id VARCHAR(64) PRIMARY KEY,
    parent_audio_ref VARCHAR(64) REFERENCES audio_media(audio_id) ON DELETE SET NULL,
    transcript_text TEXT NOT NULL,
    confidence_score FLOAT NOT NULL,
    needs_review BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS note_edges (
    edge_id SERIAL PRIMARY KEY,
    source_id VARCHAR(64) NOT NULL,
    target_id VARCHAR(64) NOT NULL,
    relationship_type VARCHAR(32) NOT NULL, -- e.g., 'TRANSCRIBED_FROM', 'LINKED_TO'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
