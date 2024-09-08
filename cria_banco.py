import sqlite3

connection = sqlite3.connect('banco.db')
cursor = connection.cursor()

cria_tabela = "CREATE TABLE IF NOT EXISTS hoteis (hotel_id text PRIMARY KEY, \
    nome text, estrelas real, diaria real, cidade text)"

cria_hotel = "INSERT INTO hoteis VALUES (1, 'otel do Edu', 5.0, 570, 'Porto de Galinhas')"


cursor.execute(cria_tabela)
cursor.execute(cria_hotel)

connection.commit()
connection.close()