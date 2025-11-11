# FlowBank — instruções rápidas para venv e imports

Passos rápidos (PowerShell - Windows):

1. Criar a virtual environment (na raiz do projeto `flowbank`):

```powershell
python -m venv .venv
```

2. Ativar a venv (PowerShell):

```powershell
.\.venv\Scripts\Activate.ps1
```

3. Atualizar pip e instalar dependências:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

4. Verificar import errors com o Django check:

```powershell
python manage.py check
```

Notas:
- O arquivo `.vscode/settings.json` sugere o caminho do interpretador para o VS Code: `${workspaceFolder}/.venv/Scripts/python.exe`.
- Se você usar outro nome para a venv, atualize o caminho em `.vscode/settings.json`.
- Se o VS Code ainda mostrar import errors, certifique-se de selecionar o interpretador (Command Palette -> Python: Select Interpreter) apontando para a venv criada.
