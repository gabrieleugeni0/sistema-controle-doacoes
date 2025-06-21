import sqlite3

def create_connection(db_file):
    """ Cria uma conexão com o banco de dados SQLite especificado por db_file """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)
    return conn

def create_tables(conn):
    """ Cria as tabelas do banco de dados """
    try:
        cursor = conn.cursor()
        # Tabela Doadores
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS doadores (
                id_doador INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                telefone TEXT,
                email TEXT,
                endereco TEXT
            );
        """)
        # Tabela Beneficiarios
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS beneficiarios (
                id_beneficiario INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                telefone TEXT,
                email TEXT,
                endereco TEXT
            );
        """)
        # Adicionar novas colunas à tabela beneficiarios se não existirem
        cursor.execute("""
            ALTER TABLE beneficiarios ADD COLUMN alimento_necessidade_1 TEXT;
        """)
        cursor.execute("""
            ALTER TABLE beneficiarios ADD COLUMN alimento_necessidade_2 TEXT;
        """)
        cursor.execute("""
            ALTER TABLE beneficiarios ADD COLUMN alimento_necessidade_3 TEXT;
        """)
        # Tabela Itens
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS itens (
                id_item INTEGER PRIMARY KEY AUTOINCREMENT,
                nome_item TEXT NOT NULL,
                marca TEXT,
                unidade TEXT NOT NULL
            );
        """)
        # Tabela DoacoesRecebidas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS doacoes_recebidas (
                id_doacao_recebida INTEGER PRIMARY KEY AUTOINCREMENT,
                id_doador INTEGER NOT NULL,
                id_item INTEGER NOT NULL,
                quantidade REAL NOT NULL,
                data_recebimento TEXT NOT NULL,
                data_validade TEXT NOT NULL,
                FOREIGN KEY (id_doador) REFERENCES doadores (id_doador),
                FOREIGN KEY (id_item) REFERENCES itens (id_item)
            );
        """)
        # Tabela DoacoesRealizadas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS doacoes_realizadas (
                id_doacao_realizada INTEGER PRIMARY KEY AUTOINCREMENT,
                id_beneficiario INTEGER NOT NULL,
                id_item INTEGER NOT NULL,
                quantidade REAL NOT NULL,
                data_doacao TEXT NOT NULL,
                FOREIGN KEY (id_beneficiario) REFERENCES beneficiarios (id_beneficiario),
                FOREIGN KEY (id_item) REFERENCES itens (id_item)
            );
        """)
        conn.commit()
    except sqlite3.Error as e:
        # Ignorar erros se a coluna já existe
        if "duplicate column name" not in str(e):
            print(e)

if __name__ == '__main__':
    database = "estoque_doacoes.db"
    conn = create_connection(database)
    if conn:
        create_tables(conn)
        conn.close()
        print(f"Banco de dados \'{database}\' e tabelas criadas com sucesso.")
    else:
        print("Erro! Não foi possível criar a conexão com o banco de dados.")


