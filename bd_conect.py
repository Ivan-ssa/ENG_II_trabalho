import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2 import sql

# Configurações do banco
db_config = {
    "host": "localhost",
    "port": 5432,
    "user": "postgres",
    "password": "1234",
    "database": "reservas"
}

# Função genérica para executar consultas SELECT
def executar_consulta(query, params=None):
    try:
        with psycopg2.connect(**db_config) as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query, params)
                return cursor.fetchall()
    except Exception as e:
        print("Erro ao executar consulta:", e)
        return []

# Função genérica para executar INSERT, UPDATE e DELETE
def executar_comando(query, params=None):
    try:
        with psycopg2.connect(**db_config) as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                conn.commit()
                return cursor.rowcount
    except Exception as e:
        print("Erro ao executar comando:", e)
        return 0




""" (    source Scripts/activate ) debntro do venv

"""