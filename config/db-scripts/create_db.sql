-- Tworzenie użytkowników
CREATE TABLE users (
    id SERIAL PRIMARY KEY,                    -- Unikalny identyfikator użytkownika
    username VARCHAR(50) NOT NULL UNIQUE,     -- Nazwa użytkownika (unikalny)
    email VARCHAR(100) NOT NULL UNIQUE,       -- Adres e-mail (unikalny)
    phone_number VARCHAR(15) NOT NULL UNIQUE, -- Numer telefonu (unikalny)
    password_hash VARCHAR(255) NOT NULL,      -- Hasz hasła
    first_name VARCHAR(50) NOT NULL,          -- Imię użytkownika
    last_name VARCHAR(50) NOT NULL,           -- Nazwisko użytkownika
    profile_picture TEXT DEFAULT NULL,        -- Zdjęcie profilowe
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Data utworzenia
    modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Data ostatniej modyfikacji
);

-- Typ ENUM dla statusu użytkownika
CREATE TYPE status_enum AS ENUM ('online', 'offline');

-- Tabela statusów użytkowników
CREATE TABLE user_status (
    user_id INT PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE, -- Identyfikator użytkownika (klucz obcy)
    status status_enum NOT NULL DEFAULT 'offline', -- Możliwe wartości: online, offline
    last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Czas ostatniej aktywności
);

-- Tworzenie konwersacji (tylko dla dwóch użytkowników)
CREATE TABLE conversations (
    id SERIAL PRIMARY KEY,                -- Unikalny identyfikator konwersacji
    user1_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE, -- Pierwszy uczestnik
    user2_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE, -- Drugi uczestnik
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Data utworzenia
--     CONSTRAINT unique_users_pair UNIQUE (user1_id, user2_id) -- Unikalne pary użytkowników
    sorted_user_ids TEXT GENERATED ALWAYS AS (
        LEAST(user1_id, user2_id) || '-' || GREATEST(user1_id, user2_id) -- Posortowane ID użytkowników
    ) STORED,                                                      -- Wartość jest zapisywana w tabeli
    CONSTRAINT unique_users_pair UNIQUE (sorted_user_ids)      -- Wymuszenie unikalności kombinacji
);

-- Tworzenie wiadomości
CREATE TABLE messages (
    id SERIAL PRIMARY KEY,                -- Unikalny identyfikator wiadomości
    conversation_id INT NOT NULL REFERENCES conversations(id) ON DELETE CASCADE, -- Konwersacja
    sender_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE, -- Nadawca
    content TEXT NOT NULL,                -- Treść wiadomości
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Data wysłania
    is_read BOOLEAN DEFAULT FALSE         -- Flaga oznaczająca przeczytanie wiadomości
);

-- Indeksy dla optymalizacji
CREATE INDEX idx_messages_conversation ON messages(conversation_id);
CREATE INDEX idx_messages_sender ON messages(sender_id);
CREATE INDEX idx_messages_created_at ON messages(created_at);

-- Funkcja do automatycznego aktualizowania modified_at
CREATE OR REPLACE FUNCTION update_modified_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.modified_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger do automatycznego aktualizowania modified_at w tabeli users
CREATE TRIGGER trigger_update_modified_at
BEFORE UPDATE ON users
FOR EACH ROW
EXECUTE FUNCTION update_modified_at();