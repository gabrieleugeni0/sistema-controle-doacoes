# Sistema de Gerenciamento de Estoque de Doações - Sociedade São Vicente de Paula

Este é um sistema simples para gerenciar o estoque de doações de alimentos para a ONG Sociedade São Vicente de Paula. Ele permite o cadastramento de doadores e beneficiários, o registro de doações recebidas e realizadas, a visualização do estoque atual e um sistema de alerta para itens próximos do vencimento.

## Funcionalidades

- **Cadastramento de Pessoas Doadoras:** Registro de informações de contato dos doadores, com validação de telefone (somente números, formato DDD+número) e e-mail.
- **Cadastramento de Pessoas que Precisam de Doações (Beneficiários):** Registro de informações de contato dos beneficiários, com validação de telefone (somente números, formato DDD+número) e e-mail, e inclusão de 3 campos para os tipos de alimentos que o beneficiário mais necessita.
- **Cadastramento de Doações Recebidas:** Registro detalhado de cada item recebido. Ao invés de solicitar o ID do doador, o sistema fornece uma lista com todos os doadores e uma ferramenta de pesquisa por nome. O "Nome do Item" foi alterado para "Tipo de Alimento" e o campo "Marca" agora oferecem listas com opções já cadastradas, permitindo também a entrada de novos valores. A "Data de Validade" agora é no formato DD/MM/YYYY.
- **Cadastramento de Doações Realizadas:** Registro detalhado de cada item doado. Ao invés de solicitar o ID do beneficiário, o sistema fornece uma lista com todos os beneficiários e uma ferramenta de pesquisa por nome. O "Tipo de Alimento" e a "Marca" são selecionados de listas de itens já existentes no estoque (não permitindo o registro de doações de itens não cadastrados). A "Data de Validade" é no formato DD/MM/YYYY. O sistema valida o estoque antes de permitir a doação, alertando o usuário se o estoque for insuficiente.
- **Exibição do Estoque Atual:** Visualização completa de todos os itens em estoque, agrupados por tipo de alimento, com a quantidade total agrupada por tipo, independente da marca.
- **Registro de Entradas (Doações Recebidas):** Nova aba que exibe o histórico detalhado de todas as doações recebidas.
- **Registro de Saídas (Doações Realizadas):** Nova aba que exibe o histórico detalhado de todas as doações realizadas.
- **Sistema de Alerta para Prazos de Vencimento:** Alertas visuais para itens que estão próximos da data de vencimento (30 dias ou menos).

## Estrutura do Projeto

O projeto é composto pelos seguintes arquivos:

- `database.py`: Contém a lógica para criação e conexão com o banco de dados SQLite.
- `models.py`: Define as classes de modelo para as entidades do sistema (Doador, Beneficiario, Item, DoacaoRecebida, DoacaoRealizada) e a lógica de interação com o banco de dados (CRUD).
- `app.py`: Implementa a interface gráfica do usuário (GUI) utilizando Tkinter e integra as funcionalidades do sistema.
- `test_models.py`: Contém os testes unitários para as classes de modelo e a interação com o banco de dados.
- `README.md`: Este arquivo, contendo informações sobre o projeto, funcionalidades e instruções de uso.
- `manual_usuario.md`: Manual do usuário detalhado.
- `documentacao_tecnica.md`: Documentação técnica do sistema.

## Requisitos

- Python 3.x
- `tkinter` (geralmente já incluído na instalação padrão do Python, mas pode precisar ser instalado separadamente em algumas distribuições Linux ou ambientes específicos).

## Instalação e Uso

1.  **Clone o repositório (se aplicável) ou baixe os arquivos:**
    ```bash
    # Se estiver em um ambiente de desenvolvimento com git
    git clone <URL_DO_REPOSITORIO>
    cd <NOME_DO_REPOSITORIO>
    ```
    Ou baixe os arquivos `database.py`, `models.py`, `app.py`, `test_models.py` para uma pasta.

2.  **Instale o Tkinter (se necessário):**
    
    **No Linux (Debian/Ubuntu):**
    ```bash
    sudo apt-get update
    sudo apt-get install python3-tk
    ```
    **No Windows/macOS:** O Tkinter geralmente vem pré-instalado com o Python. Se você tiver problemas, pode tentar reinstalar o Python ou procurar por instruções específicas para sua plataforma.

3.  **Crie o banco de dados:**
    Execute o script `database.py` para criar o arquivo do banco de dados `estoque_doacoes.db` e as tabelas necessárias.
    ```bash
    python3 database.py
    ```

4.  **Execute a aplicação:**
    Inicie a aplicação principal.
    ```bash
    python3 app.py
    ```

    A interface gráfica do sistema será aberta, permitindo que você comece a gerenciar o estoque de doações.

## Executando os Testes

Para garantir que o sistema está funcionando corretamente, você pode executar os testes unitários:

```bash
python3 test_models.py
```

Todos os testes devem passar (OK).

## Contribuição

Se você deseja contribuir com este projeto, sinta-se à vontade para abrir issues ou pull requests.

## Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.





"# sistema-controle-doacoes" 
