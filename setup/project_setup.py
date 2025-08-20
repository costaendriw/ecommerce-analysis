import os
import subprocess
import sys
from pathlib import Path

def create_virtual_environment():
    """Cria ambiente virtual para o projeto"""
    print("🔧 Criando ambiente virtual...")
    try:
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        print("✅ Ambiente virtual criado: ./venv/")
        
        # Instruções de ativação
        if os.name == 'nt':  # Windows
            print("💡 Para ativar: venv\\Scripts\\activate")
        else:  # Linux/Mac
            print("💡 Para ativar: source venv/bin/activate")
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao criar ambiente virtual: {e}")

def install_requirements():
    """Instala dependências do projeto"""
    print("\n📦 Instalando dependências...")
    requirements = """
pandas>=1.5.0
numpy>=1.21.0
matplotlib>=3.5.0
seaborn>=0.11.0
jupyter>=1.0.0
openpyxl>=3.0.0
xlrd>=2.0.0
scipy>=1.7.0
python-dateutil>=2.8.0
    """.strip()
    
    # Criar arquivo requirements.txt
    with open('requirements.txt', 'w') as f:
        f.write(requirements)
    
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        print("✅ Dependências instaladas com sucesso!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao instalar dependências: {e}")

def create_directory_structure():
    """Cria estrutura de diretórios do projeto"""
    print("\n📁 Criando estrutura de diretórios...")
    
    directories = [
        'data/raw',
        'data/processed', 
        'data/sample',
        'notebooks',
        'src',
        'reports/figures',
        'reports/insights',
        'exports',
        'tests'
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"  📂 {directory}/")
    
    print("✅ Estrutura de diretórios criada!")

def create_gitignore():
    """Cria arquivo .gitignore"""
    print("\n📝 Criando .gitignore...")
    
    gitignore_content = """
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Virtual Environment
venv/
env/
ENV/

# Jupyter Notebook
.ipynb_checkpoints

# Data files
*.csv
*.xlsx
*.xls
data/raw/*
!data/raw/.gitkeep
data/processed/*
!data/processed/.gitkeep

# Reports
reports/figures/*.png
reports/figures/*.jpg
reports/figures/*.pdf
reports/insights/*.txt
reports/insights/*.md

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/
    """.strip()
    
    with open('.gitignore', 'w') as f:
        f.write(gitignore_content)
    
    print("✅ .gitignore criado!")

def create_readme_sample():
    """Cria README básico se não existir"""
    if not os.path.exists('README.md'):
        print("\n📄 Criando README.md...")
        
        readme_content = """# 📊 Análise de Vendas E-commerce

Projeto de Data Science para análise estratégica de vendas de e-commerce.

## 🚀 Quick Start

1. **Clonar repositório:**
```bash
git clone [url-do-repositorio]
cd ecommerce-analysis
```

2. **Configurar ambiente:**
```bash
python setup.py
```

3. **Executar análise:**
```bash
python main.py
```

## 📊 Resultados

- Dashboard executivo em `reports/figures/`
- Insights detalhados em `reports/insights/`
- Dados processados em `data/processed/`

## 🛠️ Tecnologias

- Python 3.8+
- Pandas, NumPy
- Matplotlib, Seaborn
- Jupyter Notebook

## 📧 Contato

[Seu Nome] - [seu.email@exemplo.com]
"""
        
        with open('README.md', 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        print("✅ README.md criado!")

def create_gitkeep_files():
    """Cria arquivos .gitkeep para manter diretórios vazios no Git"""
    gitkeep_dirs = [
        'data/raw',
        'data/processed',
        'reports/figures',
        'reports/insights'
    ]
    
    for directory in gitkeep_dirs:
        gitkeep_path = Path(directory) / '.gitkeep'
        gitkeep_path.touch()
    
    print("📌 Arquivos .gitkeep criados para manter estrutura no Git")

def setup_project():
    """Executa setup completo do projeto"""
    print("🎯 SETUP DO PROJETO - ANÁLISE DE VENDAS E-COMMERCE")
    print("="*60)
    
    # Criar estrutura de diretórios
    create_directory_structure()
    
    # Criar arquivos de configuração
    create_gitignore()
    create_readme_sample()
    create_gitkeep_files()
    
    # Ambiente virtual (opcional)
    response = input("\n❓ Deseja criar ambiente virtual? (y/n): ").lower()
    if response in ['y', 'yes', 'sim', 's']:
        create_virtual_environment()
    
    # Instalar dependências
    response = input("❓ Deseja instalar dependências? (y/n): ").lower()
    if response in ['y', 'yes', 'sim', 's']:
        install_requirements()
    
    print("\n" + "="*60)
    print("✅ SETUP CONCLUÍDO COM SUCESSO!")
    print("="*60)
    print("\n🚀 PRÓXIMOS PASSOS:")
    print("1. 📊 Execute: python main.py")
    print("2. 📓 Ou abra: notebooks/analise_vendas_interativa.md")
    print("3. 🎯 Personalize com seus dados em data/raw/")
    print("4. 📈 Visualize resultados em reports/")
    print("\n💡 DICA: Use 'python -m jupyter notebook' para análise interativa")
    print("-"*60)

if __name__ == "__main__":
    setup_project()