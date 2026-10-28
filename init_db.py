from app.db.db import engine
from sqlalchemy import text

print("Начинаю жесткое удаление старых таблиц...")

# Подключаемся к базе и убиваем таблицы напрямую через SQL
with engine.connect() as conn:
    conn.execute(text("DROP TABLE IF EXISTS transactions CASCADE;"))
    conn.execute(text("DROP TABLE IF EXISTS users CASCADE;"))
    conn.commit()

print("Старые таблицы удалены!")

# Теперь импортируем модели и создаем новые
from app.db.db import Base
from app.models.user import User
from app.models.transactions import Transaction

Base.metadata.create_all(bind=engine)
print("Новые таблицы созданы! Колонка email теперь на месте.")