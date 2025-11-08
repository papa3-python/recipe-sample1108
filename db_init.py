# db_init.py（1回実行用の初期化スクリプト）
import os
from sqlalchemy import create_engine, text

DATABASE_URL = os.environ.get("postgresql://recipes_db_9h5d_user:yBOuoGHM2MkQtPKy8hPTcp2SFgG5Yuwx@dpg-d47jo6ili9vc738ph7q0-a.singapore-postgres.render.com/recipes_db_9h5d")  # RenderのExternal Database URLを入れる
if not DATABASE_URL:
    raise RuntimeError("環境変数 DATABASE_URL に接続文字列を設定してください。")

# RenderのPostgresはSSL必須
engine = create_engine(DATABASE_URL, connect_args={"sslmode": "require"})

schema_sql = """
CREATE TABLE IF NOT EXISTS recipes (
  id          SERIAL PRIMARY KEY,
  title       TEXT NOT NULL,
  body        TEXT,
  created_at  TIMESTAMPTZ DEFAULT now()
);
"""

seed_sql = """
INSERT INTO recipes (title, body) VALUES
(:t1, :b1), (:t2, :b2)
ON CONFLICT DO NOTHING;
"""

with engine.begin() as conn:
    conn.execute(text(schema_sql))
    conn.execute(text(seed_sql), dict(
        t1="卵焼き", b1="卵・砂糖・塩を混ぜて焼く",
        t2="味噌汁", b2="出汁・味噌・豆腐・わかめ",
    ))

print("OK: schema & seed complete.")
