import sqlite3
from datetime import datetime, timedelta

DATABASE = 'estoque_doacoes.db'

def get_db_connection(db_file):
    conn = sqlite3.connect(db_file)
    conn.row_factory = sqlite3.Row  # Permite acessar colunas por nome
    return conn

class BaseModel:
    def __init__(self, table_name, conn):
        self.table_name = table_name
        self.conn = conn
        # Mapeamento manual para IDs, pois o plural pode ser irregular
        self.id_column_map = {
            'doadores': 'id_doador',
            'beneficiarios': 'id_beneficiario',
            'itens': 'id_item',
            'doacoes_recebidas': 'id_doacao_recebida',
            'doacoes_realizadas': 'id_doacao_realizada',
        }
        self.id_column_name = self.id_column_map.get(table_name, f'id_{table_name[:-1]}')

    def save(self, data):
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?' for _ in data.values()])
        sql = f"INSERT INTO {self.table_name} ({columns}) VALUES ({placeholders})"
        cursor = self.conn.cursor()
        try:
            cursor.execute(sql, tuple(data.values()))
            self.conn.commit()
            return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Erro ao salvar em {self.table_name}: {e}")
            return None

    def get_all(self):
        cursor = self.conn.cursor()
        try:
            cursor.execute(f"SELECT * FROM {self.table_name}")
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        except sqlite3.Error as e:
            print(f"Erro ao buscar todos de {self.table_name}: {e}")
            return []

    def get_by_id(self, id_value):
        cursor = self.conn.cursor()
        try:
            sql = f"SELECT * FROM {self.table_name} WHERE {self.id_column_name} = ?"
            cursor.execute(sql, (id_value,))
            row = cursor.fetchone()
            return dict(row) if row else None
        except sqlite3.Error as e:
            print(f"Erro ao buscar por ID em {self.table_name}: {e}")
            return None

    def update(self, id_value, data):
        set_clause = ', '.join([f"{key} = ?" for key in data.keys()])
        sql = f"UPDATE {self.table_name} SET {set_clause} WHERE {self.id_column_name} = ?"
        cursor = self.conn.cursor()
        try:
            cursor.execute(sql, tuple(list(data.values()) + [id_value]))
            self.conn.commit()
            return cursor.rowcount
        except sqlite3.Error as e:
            print(f"Erro ao atualizar em {self.table_name}: {e}")
            return None

    def delete(self, id_value):
        sql = f"DELETE FROM {self.table_name} WHERE {self.id_column_name} = ?"
        cursor = self.conn.cursor()
        try:
            cursor.execute(sql, (id_value,))
            self.conn.commit()
            return cursor.rowcount
        except sqlite3.Error as e:
            print(f"Erro ao deletar de {self.table_name}: {e}")
            return None

class Doador(BaseModel):
    def __init__(self, conn):
        super().__init__('doadores', conn)

class Beneficiario(BaseModel):
    def __init__(self, conn):
        super().__init__('beneficiarios', conn)

class Item(BaseModel):
    def __init__(self, conn):
        super().__init__('itens', conn)

    def get_by_name_brand_unit(self, nome_item, marca, unidade):
        cursor = self.conn.cursor()
        try:
            cursor.execute("SELECT * FROM itens WHERE nome_item = ? AND marca = ? AND unidade = ?",
                           (nome_item, marca, unidade))
            row = cursor.fetchone()
            return dict(row) if row else None
        except sqlite3.Error as e:
            print(f"Erro ao buscar item por nome, marca e unidade: {e}")
            return None

    def get_by_name_brand(self, nome_item, marca):
        cursor = self.conn.cursor()
        try:
            cursor.execute("SELECT * FROM itens WHERE nome_item = ? AND marca = ?",
                           (nome_item, marca))
            row = cursor.fetchone()
            return dict(row) if row else None
        except sqlite3.Error as e:
            print(f"Erro ao buscar item por nome e marca: {e}")
            return None

class DoacaoRecebida(BaseModel):
    def __init__(self, conn):
        super().__init__('doacoes_recebidas', conn)

    def get_all_with_details(self):
        cursor = self.conn.cursor()
        try:
            cursor.execute("""
                SELECT
                    dr.id_doacao_recebida,
                    d.nome AS doador_nome,
                    i.nome_item,
                    i.marca,
                    i.unidade,
                    dr.quantidade,
                    dr.data_recebimento,
                    dr.data_validade
                FROM doacoes_recebidas dr
                JOIN doadores d ON dr.id_doador = d.id_doador
                JOIN itens i ON dr.id_item = i.id_item
            """)
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        except sqlite3.Error as e:
            print(f"Erro ao buscar doações recebidas com detalhes: {e}")
            return []

    def get_expiring_items(self, days_threshold):
        cursor = self.conn.cursor()
        try:
            today = datetime.now().strftime('%Y-%m-%d')
            future_date = (datetime.now() + timedelta(days=days_threshold)).strftime('%Y-%m-%d')
            sql = """
                SELECT
                    dr.id_doacao_recebida,
                    d.nome AS doador_nome,
                    i.nome_item,
                    i.marca,
                    i.unidade,
                    dr.quantidade,
                    dr.data_recebimento,
                    dr.data_validade
                FROM doacoes_recebidas dr
                JOIN doadores d ON dr.id_doador = d.id_doador
                JOIN itens i ON dr.id_item = i.id_item
                WHERE date(dr.data_validade) > date(?) AND date(dr.data_validade) <= date(?)
                ORDER BY dr.data_validade ASC
            """
            cursor.execute(sql, (today, future_date))
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        except sqlite3.Error as e:
            print(f"Erro ao buscar itens vencendo: {e}")
            return []

    def get_stock_by_item(self, item_id):
        cursor = self.conn.cursor()
        try:
            # Quantidade total recebida para o item
            cursor.execute("SELECT SUM(quantidade) FROM doacoes_recebidas WHERE id_item = ?", (item_id,))
            received_qty = cursor.fetchone()[0] or 0

            # Quantidade total realizada para o item
            cursor.execute("SELECT SUM(quantidade) FROM doacoes_realizadas WHERE id_item = ?", (item_id,))
            realized_qty = cursor.fetchone()[0] or 0

            return received_qty - realized_qty
        except sqlite3.Error as e:
            print(f"Erro ao calcular estoque para o item {item_id}: {e}")
            return 0

    def get_grouped_stock(self):
        cursor = self.conn.cursor()
        try:
            sql = """
                SELECT
                    i.nome_item,
                    i.unidade,
                    SUM(dr.quantidade) AS total_recebido
                FROM doacoes_recebidas dr
                JOIN itens i ON dr.id_item = i.id_item
                GROUP BY i.nome_item, i.unidade
            """
            cursor.execute(sql)
            received_items = cursor.fetchall()

            sql = """
                SELECT
                    i.nome_item,
                    i.unidade,
                    SUM(dr.quantidade) AS total_realizado
                FROM doacoes_realizadas dr
                JOIN itens i ON dr.id_item = i.id_item
                GROUP BY i.nome_item, i.unidade
            """
            cursor.execute(sql)
            realized_items = cursor.fetchall()

            stock = {}
            for item in received_items:
                key = (item['nome_item'], item['unidade'])
                stock[key] = stock.get(key, 0) + item['total_recebido']
            
            for item in realized_items:
                key = (item['nome_item'], item['unidade'])
                stock[key] = stock.get(key, 0) - item['total_realizado']
            
            # Filtrar itens com estoque zero ou negativo e formatar
            result = []
            for (nome_item, unidade), quantidade in stock.items():
                if quantidade > 0:
                    result.append({
                        'nome_item': nome_item,
                        'unidade': unidade,
                        'quantidade_total': quantidade
                    })
            return result
        except sqlite3.Error as e:
            print(f"Erro ao buscar estoque agrupado: {e}")
            return []

    def get_all_stock_items(self):
        cursor = self.conn.cursor()
        try:
            # Retorna todos os itens que já foram recebidos e ainda têm estoque positivo
            sql = """
                SELECT
                    i.id_item,
                    i.nome_item,
                    i.marca,
                    i.unidade,
                    dr.data_validade
                FROM itens i
                JOIN doacoes_recebidas dr ON i.id_item = dr.id_item
                GROUP BY i.id_item, i.nome_item, i.marca, i.unidade, dr.data_validade
                HAVING SUM(dr.quantidade) - COALESCE((SELECT SUM(quantidade) FROM doacoes_realizadas WHERE id_item = i.id_item), 0) > 0
            """
            cursor.execute(sql)
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        except sqlite3.Error as e:
            print(f"Erro ao buscar todos os itens em estoque: {e}")
            return []


class DoacaoRealizada(BaseModel):
    def __init__(self, conn):
        super().__init__('doacoes_realizadas', conn)

    def get_all_with_details(self):
        cursor = self.conn.cursor()
        try:
            cursor.execute("""
                SELECT
                    dr.id_doacao_realizada,
                    b.nome AS beneficiario_nome,
                    i.nome_item,
                    i.marca,
                    i.unidade,
                    dr.quantidade,
                    dr.data_doacao
                FROM doacoes_realizadas dr
                JOIN beneficiarios b ON dr.id_beneficiario = b.id_beneficiario
                JOIN itens i ON dr.id_item = i.id_item
            """
            )
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        except sqlite3.Error as e:
            print(f"Erro ao buscar doações realizadas com detalhes: {e}")
            return []




