import tkinter as tk
from tkinter import ttk, messagebox
from models import Doador, Beneficiario, Item, DoacaoRecebida, DoacaoRealizada, get_db_connection
from database import create_tables
from datetime import datetime, timedelta
import re # Para validação de regex

class EstoqueApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Gerenciamento de Estoque de Doações")
        self.geometry("1200x800") # Aumenta o tamanho da janela

        # Conexão com o banco de dados
        self.db_conn = get_db_connection("estoque_doacoes.db")
        create_tables(self.db_conn) # Garante que as tabelas existam

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)

        # Passa a conexão para as instâncias dos modelos
        self.doador_model = Doador(conn=self.db_conn)
        self.beneficiario_model = Beneficiario(conn=self.db_conn)
        self.item_model = Item(conn=self.db_conn)
        self.doacao_recebida_model = DoacaoRecebida(conn=self.db_conn)
        self.doacao_realizada_model = DoacaoRealizada(conn=self.db_conn)

        self.create_donor_tab()
        self.create_beneficiary_tab()
        self.create_received_donation_tab()
        self.create_distributed_donation_tab()
        self.create_stock_tab()
        self.create_entries_tab() # Nova aba para Entradas
        self.create_exits_tab() # Nova aba para Saídas
        self.create_alerts_tab()

        # Garante que a conexão seja fechada ao sair da aplicação
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        if self.db_conn:
            self.db_conn.close()
        self.destroy()

    # Funções de validação
    def validate_phone(self, phone):
        # Remove caracteres não numéricos para validação do comprimento
        phone_digits = re.sub(r'\D', '', phone)
        # Regex para (DD)NNNNN-NNNN ou NNNNN-NNNN (com ou sem parênteses no DDD)
        # Permite espaços e hífens, mas valida apenas dígitos
        # O número deve ter 10 ou 11 dígitos (com DDD)
        return re.fullmatch(r'\(?\d{2}\)?\s?\d{4,5}-?\d{4}', phone) is not None and (len(phone_digits) == 10 or len(phone_digits) == 11)

    def validate_email(self, email):
        # Regex para validação de email mais robusta
        return re.fullmatch(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email) is not None

    def create_donor_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Doadores")

        # Formulário de Cadastro de Doadores
        form_frame = ttk.LabelFrame(frame, text="Cadastrar Novo Doador")
        form_frame.pack(padx=20, pady=20, fill="x")

        tk.Label(form_frame, text="Nome:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.donor_name_entry = tk.Entry(form_frame, width=40)
        self.donor_name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        tk.Label(form_frame, text="Telefone (somente números, com DDD, ex: (11)98765-4321 ou 11987654321): ").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.donor_phone_entry = tk.Entry(form_frame, width=40)
        self.donor_phone_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        tk.Label(form_frame, text="Email:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.donor_email_entry = tk.Entry(form_frame, width=40)
        self.donor_email_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        tk.Label(form_frame, text="Endereço:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.donor_address_entry = tk.Entry(form_frame, width=40)
        self.donor_address_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        ttk.Button(form_frame, text="Salvar Doador", command=self.save_donor).grid(row=4, column=0, columnspan=2, pady=10)

        # Tabela de Doadores
        donor_list_frame = ttk.LabelFrame(frame, text="Doadores Cadastrados")
        donor_list_frame.pack(padx=20, pady=10, fill="both", expand=True)

        columns = ("#1", "#2", "#3", "#4", "#5")
        self.donor_tree = ttk.Treeview(donor_list_frame, columns=columns, show="headings")
        self.donor_tree.heading("#1", text="ID")
        self.donor_tree.heading("#2", text="Nome")
        self.donor_tree.heading("#3", text="Telefone")
        self.donor_tree.heading("#4", text="Email")
        self.donor_tree.heading("#5", text="Endereço")

        self.donor_tree.column("#1", width=50, anchor="center")
        self.donor_tree.column("#2", width=150)
        self.donor_tree.column("#3", width=100)
        self.donor_tree.column("#4", width=150)
        self.donor_tree.column("#5", width=200)

        self.donor_tree.pack(expand=True, fill="both")
        self.load_donors()

    def save_donor(self):
        name = self.donor_name_entry.get()
        phone = self.donor_phone_entry.get()
        email = self.donor_email_entry.get()
        address = self.donor_address_entry.get()

        if not name:
            messagebox.showerror("Erro", "O nome do doador é obrigatório!")
            return
        if phone and not self.validate_phone(phone):
            messagebox.showerror("Erro", "Telefone inválido. Deve conter somente números e ter DDD+número (10 ou 11 dígitos).")
            return
        if email and not self.validate_email(email):
            messagebox.showerror("Erro", "Email inválido.")
            return

        data = {"nome": name, "telefone": phone, "email": email, "endereco": address}
        if self.doador_model.save(data):
            messagebox.showinfo("Sucesso", "Doador cadastrado com sucesso!")
            self.clear_donor_form()
            self.load_donors()
            self.load_donor_combobox() # Atualiza combobox de doadores
        else:
            messagebox.showerror("Erro", "Não foi possível cadastrar o doador.")

    def clear_donor_form(self):
        self.donor_name_entry.delete(0, tk.END)
        self.donor_phone_entry.delete(0, tk.END)
        self.donor_email_entry.delete(0, tk.END)
        self.donor_address_entry.delete(0, tk.END)

    def load_donors(self):
        for i in self.donor_tree.get_children():
            self.donor_tree.delete(i)
        
        donors = self.doador_model.get_all()
        for donor in donors:
            self.donor_tree.insert("", "end", values=(donor["id_doador"], donor["nome"], donor["telefone"], donor["email"], donor["endereco"]))

    def create_beneficiary_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Beneficiários")

        # Formulário de Cadastro de Beneficiários
        form_frame = ttk.LabelFrame(frame, text="Cadastrar Novo Beneficiário")
        form_frame.pack(padx=20, pady=20, fill="x")

        tk.Label(form_frame, text="Nome:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.beneficiary_name_entry = tk.Entry(form_frame, width=40)
        self.beneficiary_name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        tk.Label(form_frame, text="Telefone (somente números, com DDD, ex: (11)98765-4321 ou 11987654321): ").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.beneficiary_phone_entry = tk.Entry(form_frame, width=40)
        self.beneficiary_phone_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        tk.Label(form_frame, text="Email:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.beneficiary_email_entry = tk.Entry(form_frame, width=40)
        self.beneficiary_email_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        tk.Label(form_frame, text="Endereço:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.beneficiary_address_entry = tk.Entry(form_frame, width=40)
        self.beneficiary_address_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        # Novos campos para tipos de alimentos necessários
        tk.Label(form_frame, text="Alimento Necessário 1:").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.beneficiary_food_needed1_entry = tk.Entry(form_frame, width=40)
        self.beneficiary_food_needed1_entry.grid(row=4, column=1, padx=5, pady=5, sticky="ew")

        tk.Label(form_frame, text="Alimento Necessário 2:").grid(row=5, column=0, padx=5, pady=5, sticky="w")
        self.beneficiary_food_needed2_entry = tk.Entry(form_frame, width=40)
        self.beneficiary_food_needed2_entry.grid(row=5, column=1, padx=5, pady=5, sticky="ew")

        tk.Label(form_frame, text="Alimento Necessário 3:").grid(row=6, column=0, padx=5, pady=5, sticky="w")
        self.beneficiary_food_needed3_entry = tk.Entry(form_frame, width=40)
        self.beneficiary_food_needed3_entry.grid(row=6, column=1, padx=5, pady=5, sticky="ew")

        ttk.Button(form_frame, text="Salvar Beneficiário", command=self.save_beneficiary).grid(row=7, column=0, columnspan=2, pady=10)

        # Tabela de Beneficiários
        beneficiary_list_frame = ttk.LabelFrame(frame, text="Beneficiários Cadastrados")
        beneficiary_list_frame.pack(padx=20, pady=10, fill="both", expand=True)

        columns = ("#1", "#2", "#3", "#4", "#5", "#6", "#7", "#8")
        self.beneficiary_tree = ttk.Treeview(beneficiary_list_frame, columns=columns, show="headings")
        self.beneficiary_tree.heading("#1", text="ID")
        self.beneficiary_tree.heading("#2", text="Nome")
        self.beneficiary_tree.heading("#3", text="Telefone")
        self.beneficiary_tree.heading("#4", text="Email")
        self.beneficiary_tree.heading("#5", text="Endereço")
        self.beneficiary_tree.heading("#6", text="Necessidade 1")
        self.beneficiary_tree.heading("#7", text="Necessidade 2")
        self.beneficiary_tree.heading("#8", text="Necessidade 3")

        self.beneficiary_tree.column("#1", width=50, anchor="center")
        self.beneficiary_tree.column("#2", width=120)
        self.beneficiary_tree.column("#3", width=90)
        self.beneficiary_tree.column("#4", width=120)
        self.beneficiary_tree.column("#5", width=150)
        self.beneficiary_tree.column("#6", width=100)
        self.beneficiary_tree.column("#7", width=100)
        self.beneficiary_tree.column("#8", width=100)

        self.beneficiary_tree.pack(expand=True, fill="both")
        self.load_beneficiaries()

    def save_beneficiary(self):
        name = self.beneficiary_name_entry.get()
        phone = self.beneficiary_phone_entry.get()
        email = self.beneficiary_email_entry.get()
        address = self.beneficiary_address_entry.get()
        food_needed1 = self.beneficiary_food_needed1_entry.get()
        food_needed2 = self.beneficiary_food_needed2_entry.get()
        food_needed3 = self.beneficiary_food_needed3_entry.get()

        if not name:
            messagebox.showerror("Erro", "O nome do beneficiário é obrigatório!")
            return
        if phone and not self.validate_phone(phone):
            messagebox.showerror("Erro", "Telefone inválido. Deve conter somente números e ter DDD+número (10 ou 11 dígitos).")
            return
        if email and not self.validate_email(email):
            messagebox.showerror("Erro", "Email inválido.")
            return

        data = {"nome": name, "telefone": phone, "email": email, "endereco": address,
                "alimento_necessidade_1": food_needed1, "alimento_necessidade_2": food_needed2,
                "alimento_necessidade_3": food_needed3}
        if self.beneficiario_model.save(data):
            messagebox.showinfo("Sucesso", "Beneficiário cadastrado com sucesso!")
            self.clear_beneficiary_form()
            self.load_beneficiaries()
        else:
            messagebox.showerror("Erro", "Não foi possível cadastrar o beneficiário.")

    def clear_beneficiary_form(self):
        self.beneficiary_name_entry.delete(0, tk.END)
        self.beneficiary_phone_entry.delete(0, tk.END)
        self.beneficiary_email_entry.delete(0, tk.END)
        self.beneficiary_address_entry.delete(0, tk.END)
        self.beneficiary_food_needed1_entry.delete(0, tk.END)
        self.beneficiary_food_needed2_entry.delete(0, tk.END)
        self.beneficiary_food_needed3_entry.delete(0, tk.END)

    def load_beneficiaries(self):
        for i in self.beneficiary_tree.get_children():
            self.beneficiary_tree.delete(i)
        
        beneficiaries = self.beneficiario_model.get_all()
        for beneficiary in beneficiaries:
            self.beneficiary_tree.insert("", "end", values=(
                beneficiary["id_beneficiario"], beneficiary["nome"], beneficiary["telefone"],
                beneficiary["email"], beneficiary["endereco"], beneficiary["alimento_necessidade_1"],
                beneficiary["alimento_necessidade_2"], beneficiary["alimento_necessidade_3"]
            ))

    def create_received_donation_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Doações Recebidas")

        form_frame = ttk.LabelFrame(frame, text="Registrar Doação Recebida")
        form_frame.pack(padx=20, pady=20, fill="x")

        # Doador com Combobox e busca
        tk.Label(form_frame, text="Doador:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.received_donor_combobox = ttk.Combobox(form_frame, width=37)
        self.received_donor_combobox.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.received_donor_combobox.bind("<KeyRelease>", self.update_donor_list)
        self.load_donor_combobox()

        # Tipo de Alimento com Combobox e entrada livre
        tk.Label(form_frame, text="Tipo de Alimento:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.received_item_name_combobox = ttk.Combobox(form_frame, width=37)
        self.received_item_name_combobox.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        self.received_item_name_combobox.bind("<KeyRelease>", self.update_item_name_list)
        self.load_item_name_combobox()

        # Marca com Combobox e entrada livre
        tk.Label(form_frame, text="Marca:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.received_item_brand_combobox = ttk.Combobox(form_frame, width=37)
        self.received_item_brand_combobox.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        self.received_item_brand_combobox.bind("<KeyRelease>", self.update_item_brand_list)
        self.load_item_brand_combobox()

        tk.Label(form_frame, text="Unidade (ex: kg, litro):").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.received_item_unit_entry = tk.Entry(form_frame, width=40)
        self.received_item_unit_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        tk.Label(form_frame, text="Quantidade:").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.received_quantity_entry = tk.Entry(form_frame, width=20)
        self.received_quantity_entry.grid(row=4, column=1, padx=5, pady=5, sticky="ew")

        tk.Label(form_frame, text="Data de Validade (DD/MM/YYYY):").grid(row=5, column=0, padx=5, pady=5, sticky="w")
        self.received_validity_date_entry = tk.Entry(form_frame, width=20)
        self.received_validity_date_entry.grid(row=5, column=1, padx=5, pady=5, sticky="ew")
        self.received_validity_date_entry.insert(0, datetime.now().strftime("%d/%m/%Y"))

        ttk.Button(form_frame, text="Registrar Doação Recebida", command=self.save_received_donation).grid(row=6, column=0, columnspan=2, pady=10)

    def update_donor_list(self, event):
        search_term = self.received_donor_combobox.get().lower()
        donors = self.doador_model.get_all()
        filtered_donors = [f"{d['nome']} (ID: {d['id_doador']})" for d in donors if search_term in d['nome'].lower()]
        self.received_donor_combobox['values'] = filtered_donors

    def load_donor_combobox(self):
        donors = self.doador_model.get_all()
        self.received_donor_combobox['values'] = [f"{d['nome']} (ID: {d['id_doador']})" for d in donors]

    def update_item_name_list(self, event):
        search_term = self.received_item_name_combobox.get().lower()
        items = self.item_model.get_all()
        filtered_items = sorted(list(set([i['nome_item'] for i in items if search_term in i['nome_item'].lower()])))
        self.received_item_name_combobox['values'] = filtered_items

    def load_item_name_combobox(self):
        items = self.item_model.get_all()
        unique_item_names = sorted(list(set([i['nome_item'] for i in items])))
        self.received_item_name_combobox['values'] = unique_item_names

    def update_item_brand_list(self, event):
        search_term = self.received_item_brand_combobox.get().lower()
        items = self.item_model.get_all()
        filtered_brands = sorted(list(set([i['marca'] for i in items if i['marca'] and search_term in i['marca'].lower()])))
        self.received_item_brand_combobox['values'] = filtered_brands

    def load_item_brand_combobox(self):
        items = self.item_model.get_all()
        unique_item_brands = sorted(list(set([i['marca'] for i in items if i['marca']])))
        self.received_item_brand_combobox['values'] = unique_item_brands

    def save_received_donation(self):
        selected_donor_text = self.received_donor_combobox.get()
        item_name = self.received_item_name_combobox.get().strip()
        item_brand = self.received_item_brand_combobox.get().strip()
        item_unit = self.received_item_unit_entry.get().strip()
        quantity_str = self.received_quantity_entry.get().strip()
        validity_date_str = self.received_validity_date_entry.get().strip()

        if not selected_donor_text or not item_name or not item_unit or not quantity_str or not validity_date_str:
            messagebox.showerror("Erro", "Todos os campos são obrigatórios!")
            return

        # Extrair ID do doador
        try:
            donor_id = int(selected_donor_text.split("ID: ")[1].replace(")", ""))
        except (IndexError, ValueError):
            messagebox.showerror("Erro", "Selecione um doador válido da lista.")
            return

        # Validação de Quantidade
        try:
            quantity = float(quantity_str)
            if quantity <= 0:
                messagebox.showerror("Erro", "A quantidade deve ser um número positivo.")
                return
        except ValueError:
            messagebox.showerror("Erro", "Quantidade inválida. Digite um número.")
            return

        # Validação e conversão da Data de Validade (DD/MM/YYYY para YYYY-MM-DD)
        try:
            validity_date = datetime.strptime(validity_date_str, "%d/%m/%Y").strftime("%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Erro", "Formato de Data de Validade inválido. Use DD/MM/YYYY.")
            return

        # Verificar se o item já existe ou criar um novo
        existing_item = self.item_model.get_by_name_brand_unit(item_name, item_brand, item_unit)
        if existing_item:
            item_id = existing_item["id_item"]
        else:
            item_data = {"nome_item": item_name, "marca": item_brand, "unidade": item_unit}
            item_id = self.item_model.save(item_data)
            if not item_id:
                messagebox.showerror("Erro", "Não foi possível cadastrar o item.")
                return

        donation_data = {
            "id_doador": donor_id,
            "id_item": item_id,
            "quantidade": quantity,
            "data_recebimento": datetime.now().strftime("%Y-%m-%d"),
            "data_validade": validity_date
        }

        print(f"Attempting to save received donation with data: {donation_data}") # Debug print

        if self.doacao_recebida_model.save(donation_data):
            messagebox.showinfo("Sucesso", "Doação recebida registrada com sucesso!")
            self.clear_received_donation_form()
            self.load_stock_data()
            self.load_entries_data()
            self.load_alerts_data()
            self.load_item_name_combobox() # Recarrega para incluir novos tipos/marcas
            self.load_item_brand_combobox()
        else:
            messagebox.showerror("Erro", "Não foi possível registrar a doação recebida.")

    def clear_received_donation_form(self):
        self.received_donor_combobox.set("")
        self.received_item_name_combobox.set("")
        self.received_item_brand_combobox.set("")
        self.received_item_unit_entry.delete(0, tk.END)
        self.received_quantity_entry.delete(0, tk.END)
        self.received_validity_date_entry.delete(0, tk.END)
        self.received_validity_date_entry.insert(0, datetime.now().strftime("%d/%m/%Y"))

    def create_distributed_donation_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Doações Realizadas")

        form_frame = ttk.LabelFrame(frame, text="Registrar Doação Realizada")
        form_frame.pack(padx=20, pady=20, fill="x")

        # Beneficiário com Combobox e busca
        tk.Label(form_frame, text="Beneficiário:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.distributed_beneficiary_combobox = ttk.Combobox(form_frame, width=37)
        self.distributed_beneficiary_combobox.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.distributed_beneficiary_combobox.bind("<KeyRelease>", self.update_beneficiary_list)
        self.load_beneficiary_combobox()

        # Tipo de Alimento com Combobox (apenas existentes no estoque)
        tk.Label(form_frame, text="Tipo de Alimento:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.distributed_item_name_combobox = ttk.Combobox(form_frame, width=37)
        self.distributed_item_name_combobox.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        self.distributed_item_name_combobox.bind("<<ComboboxSelected>>", self.on_distributed_item_selected)
        

        # Marca com Combobox (apenas existentes no estoque e para o tipo selecionado)
        tk.Label(form_frame, text="Marca:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.distributed_item_brand_combobox = ttk.Combobox(form_frame, width=37)
        self.distributed_item_brand_combobox.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        self.distributed_item_brand_combobox.bind("<<ComboboxSelected>>", self.on_distributed_brand_selected)
        # self.load_distributed_item_brand_combobox() # Será carregado dinamicamente

        tk.Label(form_frame, text="Unidade (ex: kg, litro):").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.distributed_item_unit_label = tk.Label(form_frame, text="") # Será preenchido automaticamente
        self.distributed_item_unit_label.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        tk.Label(form_frame, text="Quantidade:").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.distributed_quantity_entry = tk.Entry(form_frame, width=20)
        self.distributed_quantity_entry.grid(row=4, column=1, padx=5, pady=5, sticky="ew")

        tk.Label(form_frame, text="Data de Validade (DD/MM/YYYY):").grid(row=5, column=0, padx=5, pady=5, sticky="w")
        self.distributed_validity_date_label = tk.Label(form_frame, text="") # Será preenchido automaticamente
        self.distributed_validity_date_label.grid(row=5, column=1, padx=5, pady=5, sticky="ew")

        ttk.Button(form_frame, text="Registrar Doação Realizada", command=self.save_distributed_donation).grid(row=6, column=0, columnspan=2, pady=10)
        
        # Move a chamada para load_distributed_item_name_combobox para depois da definição de todos os widgets
        self.load_distributed_item_name_combobox()

    def update_beneficiary_list(self, event):
        search_term = self.distributed_beneficiary_combobox.get().lower()
        beneficiaries = self.beneficiario_model.get_all()
        filtered_beneficiaries = [f"{b['nome']} (ID: {b['id_beneficiario']})" for b in beneficiaries if search_term in b['nome'].lower()]
        self.distributed_beneficiary_combobox['values'] = filtered_beneficiaries

    def load_beneficiary_combobox(self):
        beneficiaries = self.beneficiario_model.get_all()
        self.distributed_beneficiary_combobox['values'] = [f"{b['nome']} (ID: {b['id_beneficiario']})" for b in beneficiaries]

    def load_distributed_item_name_combobox(self):
        # Carrega apenas os tipos de alimentos que têm estoque
        stock_items = self.doacao_recebida_model.get_all_stock_items()
        unique_item_names = sorted(list(set([item['nome_item'] for item in stock_items])))
        self.distributed_item_name_combobox['values'] = unique_item_names
        self.distributed_item_name_combobox.set("") # Limpa a seleção
        self.distributed_item_brand_combobox.set("")
        self.distributed_item_brand_combobox['values'] = []
        self.distributed_item_unit_label.config(text="")
        self.distributed_validity_date_label.config(text="")

    def on_distributed_item_selected(self, event):
        selected_item_name = self.distributed_item_name_combobox.get()
        if selected_item_name:
            # Carrega as marcas disponíveis para o tipo de alimento selecionado
            stock_items = self.doacao_recebida_model.get_all_stock_items()
            available_brands = sorted(list(set([item['marca'] for item in stock_items if item['nome_item'] == selected_item_name and item['marca']])))
            self.distributed_item_brand_combobox['values'] = available_brands
            self.distributed_item_brand_combobox.set("") # Limpa a seleção da marca
            self.distributed_item_unit_label.config(text="")
            self.distributed_validity_date_label.config(text="")
        else:
            self.distributed_item_brand_combobox['values'] = []
            self.distributed_item_brand_combobox.set("")
            self.distributed_item_unit_label.config(text="")
            self.distributed_validity_date_label.config(text="")

    def on_distributed_brand_selected(self, event):
        selected_item_name = self.distributed_item_name_combobox.get()
        selected_brand = self.distributed_item_brand_combobox.get()
        if selected_item_name and selected_brand:
            # Encontra o item específico para preencher unidade e data de validade
            stock_items = self.doacao_recebida_model.get_all_stock_items()
            found_item = None
            for item in stock_items:
                if item['nome_item'] == selected_item_name and item['marca'] == selected_brand:
                    found_item = item
                    break
            if found_item:
                self.distributed_item_unit_label.config(text=found_item['unidade'])
                # Formata a data de validade para DD/MM/YYYY
                validity_date_obj = datetime.strptime(found_item['data_validade'], "%Y-%m-%d")
                self.distributed_validity_date_label.config(text=validity_date_obj.strftime("%d/%m/%Y"))
            else:
                self.distributed_item_unit_label.config(text="")
                self.distributed_validity_date_label.config(text="")
        else:
            self.distributed_item_unit_label.config(text="")
            self.distributed_validity_date_label.config(text="")

    def save_distributed_donation(self):
        selected_beneficiary_text = self.distributed_beneficiary_combobox.get()
        item_name = self.distributed_item_name_combobox.get().strip()
        item_brand = self.distributed_item_brand_combobox.get().strip()
        quantity_str = self.distributed_quantity_entry.get().strip()

        if not selected_beneficiary_text or not item_name or not item_brand or not quantity_str:
            messagebox.showerror("Erro", "Todos os campos são obrigatórios!")
            return

        # Extrair ID do beneficiário
        try:
            beneficiary_id = int(selected_beneficiary_text.split("ID: ")[1].replace(")", ""))
        except (IndexError, ValueError):
            messagebox.showerror("Erro", "Selecione um beneficiário válido da lista.")
            return

        # Validação de Quantidade
        try:
            quantity = float(quantity_str)
            if quantity <= 0:
                messagebox.showerror("Erro", "A quantidade deve ser um número positivo.")
                return
        except ValueError:
            messagebox.showerror("Erro", "Quantidade inválida. Digite um número.")
            return

        # Obter item_id com base no nome e marca selecionados
        item_info = self.item_model.get_by_name_brand(item_name, item_brand)
        if not item_info:
            messagebox.showerror("Erro", "Item não encontrado no estoque. Selecione um item válido.")
            return
        item_id = item_info["id_item"]

        # Verificar estoque
        current_stock = self.doacao_recebida_model.get_stock_by_item(item_id)
        if current_stock < quantity:
            messagebox.showerror("Erro", f"Estoque insuficiente para {item_name} ({item_brand}). Disponível: {current_stock:.2f}")
            return

        donation_data = {
            "id_beneficiario": beneficiary_id,
            "id_item": item_id,
            "quantidade": quantity,
            "data_doacao": datetime.now().strftime("%Y-%m-%d")
        }

        if self.doacao_realizada_model.save(donation_data):
            messagebox.showinfo("Sucesso", "Doação realizada registrada com sucesso!")
            self.clear_distributed_donation_form()
            self.load_stock_data()
            self.load_exits_data()
            self.load_distributed_item_name_combobox() # Recarrega para refletir mudanças no estoque
        else:
            messagebox.showerror("Erro", "Não foi possível registrar a doação realizada.")

    def clear_distributed_donation_form(self):
        self.distributed_beneficiary_combobox.set("")
        self.distributed_item_name_combobox.set("")
        self.distributed_item_brand_combobox.set("")
        self.distributed_quantity_entry.delete(0, tk.END)
        self.distributed_item_unit_label.config(text="")
        self.distributed_validity_date_label.config(text="")

    def create_stock_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Estoque Atual")

        columns = ("#1", "#2", "#3")
        self.stock_tree = ttk.Treeview(frame, columns=columns, show="headings")
        self.stock_tree.heading("#1", text="Tipo de Alimento")
        self.stock_tree.heading("#2", text="Unidade")
        self.stock_tree.heading("#3", text="Quantidade Total")

        self.stock_tree.column("#1", width=200)
        self.stock_tree.column("#2", width=100)
        self.stock_tree.column("#3", width=150, anchor="center")

        self.stock_tree.pack(expand=True, fill="both", padx=10, pady=10)
        self.load_stock_data()

    def load_stock_data(self):
        for i in self.stock_tree.get_children():
            self.stock_tree.delete(i)
        
        grouped_stock = self.doacao_recebida_model.get_grouped_stock()
        for item in grouped_stock:
            # Correção da f-string: usar aspas diferentes para o f-string e para a chave do dicionário
            self.stock_tree.insert("", "end", values=(item["nome_item"], item["unidade"], f"{item['quantidade_total']:.2f}"))

    def create_entries_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Entradas (Doações Recebidas)")

        columns = ("#1", "#2", "#3", "#4", "#5", "#6", "#7", "#8")
        self.entries_tree = ttk.Treeview(frame, columns=columns, show="headings")
        self.entries_tree.heading("#1", text="ID Doação")
        self.entries_tree.heading("#2", text="Doador")
        self.entries_tree.heading("#3", text="Tipo de Alimento")
        self.entries_tree.heading("#4", text="Marca")
        self.entries_tree.heading("#5", text="Unidade")
        self.entries_tree.heading("#6", text="Quantidade")
        self.entries_tree.heading("#7", text="Data Recebimento")
        self.entries_tree.heading("#8", text="Data Validade")

        self.entries_tree.column("#1", width=80, anchor="center")
        self.entries_tree.column("#2", width=150)
        self.entries_tree.column("#3", width=120)
        self.entries_tree.column("#4", width=100)
        self.entries_tree.column("#5", width=80)
        self.entries_tree.column("#6", width=80, anchor="center")
        self.entries_tree.column("#7", width=100, anchor="center")
        self.entries_tree.column("#8", width=100, anchor="center")

        self.entries_tree.pack(expand=True, fill="both", padx=10, pady=10)
        self.load_entries_data()

    def load_entries_data(self):
        for i in self.entries_tree.get_children():
            self.entries_tree.delete(i)
        
        entries = self.doacao_recebida_model.get_all_with_details()
        for entry in entries:
            # Formata a data de validade para DD/MM/YYYY
            validity_date_obj = datetime.strptime(entry['data_validade'], "%Y-%m-%d")
            formatted_validity_date = validity_date_obj.strftime("%d/%m/%Y")
            
            # Formata a data de recebimento para DD/MM/YYYY
            received_date_obj = datetime.strptime(entry['data_recebimento'], "%Y-%m-%d")
            formatted_received_date = received_date_obj.strftime("%d/%m/%Y")

            self.entries_tree.insert("", "end", values=(
                entry["id_doacao_recebida"],
                entry["doador_nome"],
                entry["nome_item"],
                entry["marca"],
                entry["unidade"],
                f"{entry['quantidade']:.2f}", # Formata quantidade
                formatted_received_date,
                formatted_validity_date
            ))

    def create_exits_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Saídas (Doações Realizadas)")

        columns = ("#1", "#2", "#3", "#4", "#5", "#6", "#7")
        self.exits_tree = ttk.Treeview(frame, columns=columns, show="headings")
        self.exits_tree.heading("#1", text="ID Doação")
        self.exits_tree.heading("#2", text="Beneficiário")
        self.exits_tree.heading("#3", text="Tipo de Alimento")
        self.exits_tree.heading("#4", text="Marca")
        self.exits_tree.heading("#5", text="Unidade")
        self.exits_tree.heading("#6", text="Quantidade")
        self.exits_tree.heading("#7", text="Data Doação")

        self.exits_tree.column("#1", width=80, anchor="center")
        self.exits_tree.column("#2", width=150)
        self.exits_tree.column("#3", width=120)
        self.exits_tree.column("#4", width=100)
        self.exits_tree.column("#5", width=80)
        self.exits_tree.column("#6", width=80, anchor="center")
        self.exits_tree.column("#7", width=100, anchor="center")

        self.exits_tree.pack(expand=True, fill="both", padx=10, pady=10)
        self.load_exits_data()

    def load_exits_data(self):
        for i in self.exits_tree.get_children():
            self.exits_tree.delete(i)
        
        exits = self.doacao_realizada_model.get_all_with_details()
        for exit_item in exits:
            # Formata a data de doação para DD/MM/YYYY
            donation_date_obj = datetime.strptime(exit_item['data_doacao'], "%Y-%m-%d")
            formatted_donation_date = donation_date_obj.strftime("%d/%m/%Y")

            self.exits_tree.insert("", "end", values=(
                exit_item["id_doacao_realizada"],
                exit_item["beneficiario_nome"],
                exit_item["nome_item"],
                exit_item["marca"],
                exit_item["unidade"],
                f"{exit_item['quantidade']:.2f}", # Formata quantidade
                formatted_donation_date
            ))

    def create_alerts_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Alertas de Vencimento")

        columns = ("#1", "#2", "#3", "#4", "#5", "#6")
        self.alerts_tree = ttk.Treeview(frame, columns=columns, show="headings")
        self.alerts_tree.heading("#1", text="ID Doação Recebida")
        self.alerts_tree.heading("#2", text="Tipo de Alimento")
        self.alerts_tree.heading("#3", text="Marca")
        self.alerts_tree.heading("#4", text="Unidade")
        self.alerts_tree.heading("#5", text="Quantidade")
        self.alerts_tree.heading("#6", text="Data Validade")

        self.alerts_tree.column("#1", width=120, anchor="center")
        self.alerts_tree.column("#2", width=150)
        self.alerts_tree.column("#3", width=100)
        self.alerts_tree.column("#4", width=80)
        self.alerts_tree.column("#5", width=80, anchor="center")
        self.alerts_tree.column("#6", width=100, anchor="center")

        self.alerts_tree.pack(expand=True, fill="both", padx=10, pady=10)
        self.load_alerts_data()

        # Atualiza os alertas a cada 60 segundos (1 minuto)
        self.after(60000, self.load_alerts_data)

    def load_alerts_data(self):
        for i in self.alerts_tree.get_children():
            self.alerts_tree.delete(i)
        
        # Alertas para itens com 30 dias ou menos para vencer
        expiring_items = self.doacao_recebida_model.get_expiring_items(30)
        for item in expiring_items:
            # Formata a data de validade para DD/MM/YYYY
            validity_date_obj = datetime.strptime(item['data_validade'], "%Y-%m-%d")
            formatted_validity_date = validity_date_obj.strftime("%d/%m/%Y")

            self.alerts_tree.insert("", "end", values=(
                item["id_doacao_recebida"],
                item["nome_item"],
                item["marca"],
                item["unidade"],
                f"{item['quantidade']:.2f}", # Formata quantidade
                formatted_validity_date
            ))


if __name__ == "__main__":
    app = EstoqueApp()
    app.mainloop()


