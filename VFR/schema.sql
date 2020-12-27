DROP TABLE IF EXISTS videos;
DROP TABLE IF EXISTS faces;

CREATE TABLE videos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    extension TEXT NOT NULL,
    duration INTEGER NOT NULL,
    FPS INTEGER NOT NULL,
    dimensions TEXT NOT NULL,
    step INTEGER NOT NULL
);

CREATE TABLE frames (
    video_id INTEGER NOT NULL,
    second INTEGER NOT NULL,
    frame INTEGER NOT NULL,
    faces INTEGER NOT NULL,
    FOREIGN KEY (video_id) REFERENCES videos(id)
);