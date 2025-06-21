import unittest
import os
from datetime import datetime, timedelta
from models import Doador, Beneficiario, Item, DoacaoRecebida, DoacaoRealizada, get_db_connection
from database import create_tables # Importar create_tables
import sqlite3

class TestDatabaseAndModels(unittest.TestCase):

    def setUp(self):
        # Configura um banco de dados de teste em memória para cada teste
        self.test_db = ":memory:"
        self.conn = get_db_connection(self.test_db)

        # Cria as tabelas para o teste usando a função create_tables
        create_tables(self.conn)

        # Inicializa os modelos passando a conexão
        self.doador_model = Doador(conn=self.conn)
        self.beneficiario_model = Beneficiario(conn=self.conn)
        self.item_model = Item(conn=self.conn)
        self.doacao_recebida_model = DoacaoRecebida(conn=self.conn)
        self.doacao_realizada_model = DoacaoRealizada(conn=self.conn)

    def tearDown(self):
        # Fecha a conexão do banco de dados de teste
        self.conn.close()

    def test_doador_crud(self):
        # Teste de criação
        doador_id = self.doador_model.save({"nome": "Doador Teste", "telefone": "1111-1111", "email": "doador@teste.com", "endereco": "Rua A"})
        self.assertIsNotNone(doador_id)
        self.assertIsInstance(doador_id, int)

        # Teste de leitura (get_by_id)
        doador = self.doador_model.get_by_id(doador_id)
        self.assertIsNotNone(doador)
        self.assertEqual(doador["nome"], "Doador Teste")

        # Teste de atualização
        updated_rows = self.doador_model.update(doador_id, {"nome": "Doador Atualizado", "telefone": "2222-2222"})
        self.assertEqual(updated_rows, 1)
        doador_updated = self.doador_model.get_by_id(doador_id)
        self.assertEqual(doador_updated["nome"], "Doador Atualizado")

        # Teste de leitura (get_all)
        all_doadores = self.doador_model.get_all()
        self.assertGreater(len(all_doadores), 0)

        # Teste de exclusão
        deleted_rows = self.doador_model.delete(doador_id)
        self.assertEqual(deleted_rows, 1)
        doador_deleted = self.doador_model.get_by_id(doador_id)
        self.assertIsNone(doador_deleted)

    def test_beneficiario_crud(self):
        beneficiario_id = self.beneficiario_model.save({"nome": "Beneficiario Teste", "telefone": "3333-3333", "email": "benef@teste.com", "endereco": "Rua B"})
        self.assertIsNotNone(beneficiario_id)
        beneficiario = self.beneficiario_model.get_by_id(beneficiario_id)
        self.assertEqual(beneficiario["nome"], "Beneficiario Teste")

    def test_item_crud(self):
        item_id = self.item_model.save({"nome_item": "Arroz", "marca": "Tio Joao", "unidade": "5kg"})
        self.assertIsNotNone(item_id)
        item = self.item_model.get_by_id(item_id)
        self.assertEqual(item["nome_item"], "Arroz")

    def test_doacao_recebida_crud(self):
        doador_id = self.doador_model.save({"nome": "Doador DR", "telefone": "", "email": "", "endereco": ""})
        item_id = self.item_model.save({"nome_item": "Feijao", "marca": "Camil", "unidade": "1kg"})
        
        doacao_id = self.doacao_recebida_model.save({
            "id_doador": doador_id,
            "id_item": item_id,
            "quantidade": 10.0,
            "data_recebimento": "2025-06-19",
            "data_validade": "2025-12-31"
        })
        self.assertIsNotNone(doacao_id)

        doacao = self.doacao_recebida_model.get_by_id(doacao_id)
        self.assertEqual(doacao["quantidade"], 10.0)

        all_doacoes = self.doacao_recebida_model.get_all_with_details()
        self.assertGreater(len(all_doacoes), 0)
        self.assertEqual(all_doacoes[0]["doador_nome"], "Doador DR")
        self.assertEqual(all_doacoes[0]["nome_item"], "Feijao")

    def test_doacao_realizada_crud(self):
        beneficiario_id = self.beneficiario_model.save({"nome": "Beneficiario DR", "telefone": "", "email": "", "endereco": ""})
        item_id = self.item_model.save({"nome_item": "Macarrao", "marca": "Adria", "unidade": "500g"})

        doacao_id = self.doacao_realizada_model.save({
            "id_beneficiario": beneficiario_id,
            "id_item": item_id,
            "quantidade": 5.0,
            "data_doacao": "2025-06-19"
        })
        self.assertIsNotNone(doacao_id)

        doacao = self.doacao_realizada_model.get_by_id(doacao_id)
        self.assertEqual(doacao["quantidade"], 5.0)

        all_doacoes = self.doacao_realizada_model.get_all_with_details()
        self.assertGreater(len(all_doacoes), 0)
        self.assertEqual(all_doacoes[0]["beneficiario_nome"], "Beneficiario DR")
        self.assertEqual(all_doacoes[0]["nome_item"], "Macarrao")

    def test_get_expiring_items(self):
        doador_id = self.doador_model.save({"nome": "Doador Exp", "telefone": "", "email": "", "endereco": ""})
        item_id_1 = self.item_model.save({"nome_item": "Leite", "marca": "", "unidade": "1L"})
        item_id_2 = self.item_model.save({"nome_item": "Biscoito", "marca": "", "unidade": "Pct"})
        item_id_3 = self.item_model.save({"nome_item": "Cafe", "marca": "", "unidade": "500g"})

        # Usar uma data fixa para hoje para garantir consistência nos testes
        fixed_today = datetime(2025, 6, 19) 
        
        # Item vencendo em 5 dias
        validade_5_dias = (fixed_today + timedelta(days=5)).strftime("%Y-%m-%d")
        self.doacao_recebida_model.save({"id_doador": doador_id, "id_item": item_id_1, "quantidade": 2.0, "data_recebimento": fixed_today.strftime("%Y-%m-%d"), "data_validade": validade_5_dias})

        # Item vencendo em 12 dias
        validade_12_dias = (fixed_today + timedelta(days=12)).strftime("%Y-%m-%d")
        self.doacao_recebida_model.save({"id_doador": doador_id, "id_item": item_id_2, "quantidade": 3.0, "data_recebimento": fixed_today.strftime("%Y-%m-%d"), "data_validade": validade_12_dias})

        # Item vencendo em 25 dias
        validade_25_dias = (fixed_today + timedelta(days=25)).strftime("%Y-%m-%d")
        self.doacao_recebida_model.save({"id_doador": doador_id, "id_item": item_id_3, "quantidade": 1.0, "data_recebimento": fixed_today.strftime("%Y-%m-%d"), "data_validade": validade_25_dias})

        # Teste para 10 dias
        expiring_10 = self.doacao_recebida_model.get_expiring_items(10)
        self.assertEqual(len(expiring_10), 1) # Apenas o item de 5 dias
        self.assertEqual(expiring_10[0]["nome_item"], "Leite")

        # Teste para 15 dias
        expiring_15 = self.doacao_recebida_model.get_expiring_items(15)
        self.assertEqual(len(expiring_15), 2) # Itens de 5 e 12 dias
        self.assertEqual(expiring_15[0]["nome_item"], "Leite")
        self.assertEqual(expiring_15[1]["nome_item"], "Biscoito")

        # Teste para 30 dias
        expiring_30 = self.doacao_recebida_model.get_expiring_items(30)
        self.assertEqual(len(expiring_30), 3) # Itens de 5, 12 e 25 dias

if __name__ == '__main__':
    unittest.main(argv=["first-arg-is-ignored"], exit=False)


