import PyInstaller.__main__

PyInstaller.__main__.run([
    'app.py',
    '--onefile',
    '--windowed',
    '--name=SistemaEstoqueDoacoes',
    '--add-data=estoque_doacoes.db:.',
    '--add-data=models.py:.',
    '--add-data=database.py:.'
])

