CREATE TABLE IF NOT EXISTS questions
(
    question_id INTEGER PRIMARY KEY,
    text        TEXT,
    answer      TEXT,
    difficulty  INTEGER default 0,
    created_at  TIMESTAMP
);
