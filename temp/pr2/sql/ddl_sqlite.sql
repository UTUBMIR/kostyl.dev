-- 3NF - дані атомарні, залежать лише від первинного ключа
CREATE TABLE authors (
    id          TEXT        PRIMARY KEY,
    first_name  VARCHAR(64) NOT NULL,
    last_name   VARCHAR(64) NOT NULL,
    bio         TEXT,
    image_path  VARCHAR(2048)
);

-- 3NF
CREATE TABLE genres (
    id          TEXT        PRIMARY KEY,
    name        VARCHAR(64) NOT NULL,
    description TEXT,
    
    CONSTRAINT genres_name_key
        UNIQUE (name)
);

-- 3NF
CREATE TABLE audiobooks (
    id               TEXT         PRIMARY KEY,
    author_id        TEXT         NOT NULL,
    genre_id         TEXT         NOT NULL,
    title            VARCHAR(255) NOT NULL,
    duration         INTEGER      NOT NULL,
    release_year     INTEGER      NOT NULL,
    description      TEXT,
    cover_image_path VARCHAR(2048),
    
    CONSTRAINT audiobooks_author_id_authors_id_fkey
    FOREIGN KEY (author_id)
    REFERENCES authors(id)
    ON DELETE CASCADE,

    CONSTRAINT audiobooks_genre_id_genres_id_fkey
    FOREIGN KEY (genre_id)
    REFERENCES genres(id)
    ON DELETE CASCADE,

    CONSTRAINT audiobooks_duration_positive_check
         CHECK (duration > 0),
    --CONSTRAINT audiobooks_release_year_check
         --CHECK (release_year >= 1900 AND release_year <= CAST(strftime('%Y', 'now') AS INTEGER) + 1)
);

CREATE INDEX audiobooks_author_id_idx ON audiobooks(author_id);
CREATE INDEX audiobooks_genre_id_idx  ON audiobooks(genre_id);

-- 3NF
CREATE TABLE users (
    id               TEXT          PRIMARY KEY,
    username         VARCHAR(64)   NOT NULL,
    passwrod_hash    VARCHAR(128)  NOT NULL,
    email            VARCHAR(376),
    avatar_path      VARCHAR(2048),

    CONSTRAINT users_username_key
        UNIQUE (username),
    CONSTRAINT users_username_not_empty_check
         CHECK (length(trim(username)) > 0),
);

CREATE INDEX users_email_idx ON users(email);

-- 3NF
CREATE TABLE collections (
    id               TEXT        PRIMARY KEY,
    user_id          TEXT,
    name             VARCHAR(128) NOT NULL,
    created_at       TIMESTAMP,

    CONSTRAINT collections_user_id_users_id_fkey
    FOREIGN KEY (user_id)
    REFERENCES users(id)
    ON DELETE CASCADE,

    CONSTRAINT collections_name_not_empty_check
         CHECK (length(trim(name)) > 0)
);

-- 2NF
CREATE TABLE audiobook_collection (
    collection_id   TEXT NOT NULL,
    audiobook_id    TEXT NOT NULL,
    PRIMARY KEY(collection_id, audiobook_id),
    
    CONSTRAINT audiobook_collection_collection_id_collections_id_fkey
    FOREIGN KEY (collection_id)
    REFERENCES collections(id)
    ON DELETE CASCADE,
    
    CONSTRAINT audiobook_collection_audiobook_id_audiobooks_id_fkey
    FOREIGN KEY (audiobook_id)
    REFERENCES audiobooks(id)
    ON DELETE CASCADE
);

-- 3NF
CREATE TABLE audiobook_files (
    id               TEXT             PRIMARY KEY,
    audiobook_id     TEXT             NOT NULL, 
    file_path        VARCHAR(2048)    NOT NULL,
    format           VARCHAR(10) NOT NULL,
    size             INTEGER,
                     
    CONSTRAINT audiobook_files_audiobook_id_audiobooks_id_fkey
    FOREIGN KEY (audiobook_id)
    REFERENCES audiobooks(id)
    ON DELETE CASCADE,

    CONSTRAINT audiobook_files_size_positive_check
         CHECK (size IS NULL OR size > 0),
    CONSTRAINT audiobook_files_file_path_not_empty_check
         CHECK (length(trim(file_path)) > 0)
);

CREATE INDEX audiobook_files_audiobook_id_idx ON audiobook_files(audiobook_id);

-- 3NF
CREATE TABLE listening_progresses (
    id               TEXT       PRIMARY KEY,
    user_id          TEXT,
    audiobook_id     TEXT       NOT NULL,
    position         INTEGER    NOT NULL,
    last_listened    TIMESTAMP,

    CONSTRAINT listening_progresses_user_id_users_id_fkey
    FOREIGN KEY (user_id)
    REFERENCES users(id)
    ON DELETE CASCADE,

    CONSTRAINT listening_progresses_audiobook_id_audiobooks_id_fkey
    FOREIGN KEY (audiobook_id)
    REFERENCES audiobooks(id)
    ON DELETE CASCADE,

    CONSTRAINT listening_progresses_position_positive_check
         CHECK (position > 0)
);

CREATE INDEX listening_progresses_user_id_idx       ON listening_progresses(user_id);
CREATE INDEX listening_progresses_audiobook_id_idx  ON listening_progresses(audiobook_id);