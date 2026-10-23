-- Esquema relacional (PostgreSQL) equivalente ao banco da página.
-- Mapa: phases -> artifact db "phases/{id}"; progress -> "data/users/{uid}/progress"

CREATE TABLE users (
  id         BIGSERIAL PRIMARY KEY,
  email      TEXT UNIQUE NOT NULL,
  name       TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE phases (
  id       BIGSERIAL PRIMARY KEY,
  position INT  NOT NULL,
  title    TEXT NOT NULL,
  duration TEXT,
  project  TEXT,
  resources TEXT,
  tip      TEXT
);

CREATE TABLE topic_groups (
  id       BIGSERIAL PRIMARY KEY,
  phase_id BIGINT NOT NULL REFERENCES phases(id) ON DELETE CASCADE,
  position INT  NOT NULL,
  name     TEXT NOT NULL
);

CREATE TABLE topics (
  id       BIGSERIAL PRIMARY KEY,
  group_id BIGINT NOT NULL REFERENCES topic_groups(id) ON DELETE CASCADE,
  position INT  NOT NULL,
  title    TEXT NOT NULL,
  code     TEXT UNIQUE
);

-- Progresso e anotações: um registro por usuário e tópico
CREATE TABLE progress (
  user_id     BIGINT NOT NULL REFERENCES users(id)  ON DELETE CASCADE,
  topic_id    BIGINT NOT NULL REFERENCES topics(id) ON DELETE CASCADE,
  status      TEXT CHECK (status IN ('z','r','e')),  -- z=do zero, r=falta terminar, e=concluído
  note        TEXT,
  review_date DATE,
  updated_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
  PRIMARY KEY (user_id, topic_id)
);

CREATE INDEX idx_groups_phase  ON topic_groups(phase_id, position);
CREATE INDEX idx_topics_group  ON topics(group_id, position);
CREATE INDEX idx_progress_due  ON progress(user_id, review_date) WHERE status <> 'e';

-- Percentual concluído por fase e usuário
CREATE VIEW phase_progress AS
SELECT pr.user_id, ph.id AS phase_id, ph.title,
       COUNT(*) AS total,
       COUNT(*) FILTER (WHERE p.status = 'e') AS done
FROM phases ph
JOIN topic_groups g ON g.phase_id = ph.id
JOIN topics t       ON t.group_id = g.id
CROSS JOIN (SELECT DISTINCT user_id FROM progress) pr
LEFT JOIN progress p ON p.topic_id = t.id AND p.user_id = pr.user_id
GROUP BY pr.user_id, ph.id, ph.title;
