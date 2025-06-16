import sqlite3

# DATABASE_FILE="./database/tde.db"
DATABASE_FILE="tde.db"

# conectando...
conn = sqlite3.connect(DATABASE_FILE)

# definindo um cursor
cursor = conn.cursor()
# cursor.execute("update usuarios set tipo='DOADOR' where tipo=2")
# cursor.execute("insert into usuarios (cpf, telefone, email, nome, tipo, hash_senha, primeiro_acesso) values '12345678947', '(75)4477-4774', 'admin@unifan.br', 'Administrador do Sistema', 'ADMIN', '12345678', 0)")
cursor.execute("select * from usuarios")
lista = cursor.fetchall()
print(lista)

cursor.execute("select * from campanhas")
lista = cursor.fetchall()
print(lista)

cursor.execute("select * from doacoes")
lista = cursor.fetchall()
print(lista)


# criando as tabelas
# cursor.execute("""
# CREATE TABLE usuarios (
#   id INTEGER PRIMARY KEY AUTOINCREMENT,
#   cpf VARCHAR(11) NOT NULL,
#   telefone VARCHAR(15),
#   email VARCHAR(30) NOT NULL,
#   nome VARCHAR(50) NOT NULL,
#   tipo VARCHAR(10) NOT NULL,
#   hash_senha VARCHAR(20) NOT NULL, 
#   primeiro_acesso BOOLEAN NOT NULL
# );
# """)
# print('Tabela usuarios criada com sucesso.')

# cursor.execute("""
# CREATE TABLE campanhas (
#   id INTEGER PRIMARY KEY AUTOINCREMENT,
#   nome VARCHAR(50) NOT NULL,
#   descricao VARCHAR(100) NOT NULL,
#   dt_inicio TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
#   dt_fim TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
#   meta_arrecadacao REAL NOT NULL 
# );
# """)
# print('Tabela campanhas criada com sucesso.')

# cursor.execute("""
# CREATE TABLE doacoes (
#   id INTEGER PRIMARY KEY AUTOINCREMENT,
#   numero_cartao VARCHAR(20) NOT NULL,
#   nome_cartao VARCHAR(500) NOT NULL,
#   dt_validade_cartao TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
#   codigo_seguranca_cartao INTEGER NOT NULL,
#   valor_doado REAL NOT NULL,
#   id_doador INTEGER NOT NULL,
#   id_campanha INTEGER NOT NULL,
#   FOREIGN KEY (id_doador) REFERENCES usuarios(id),
#   FOREIGN KEY (id_campanha) REFERENCES campanhas(id)
# );
# """)
# print('Tabela doação criada com sucesso.')
# conn.commit()
# cursor.execute("insert into usuarios (cpf, telefone, email, nome, tipo, hash_senha, primeiro_acesso) values ('12345678947', '(75)4477-4774', 'admin@unifan.br', 'Administrador do Sistema', 'ADMIN', '12345678', 0)")

# conn.commit()
# desconectando...
conn.close()
