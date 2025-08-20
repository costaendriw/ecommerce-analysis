# Análise de Vendas E-commerce - Notebook Interativo

## 1. Importação de Bibliotecas e Configuração
```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Importar módulos do projeto
from data_processing import DataProcessor, generate_sample_data
from visualization import EcommerceVisualizer, setup_visualization_style
from business_analysis import BusinessAnalyzer

# Configurar visualizações
setup_visualization_style()
plt.rcParams['figure.figsize'] = (12, 6)
```

## 2. Carregamento e Processamento de Dados
```python
# Carregar dados
processor = DataProcessor()

# Opção 1: Usar dados simulados
data = generate_sample_data(5000)
processor.load_data(data=data)

# Opção 2: Carregar dados reais (descomente a linha abaixo)
# processor.load_data(file_path='caminho/para/seus/dados.xlsx')

# Processar dados
processed_data = processor.clean_data()
print(f"Dados processados: {len(processed_data):,} registros")
```

## 3. Análise Exploratória
```python
# Estatísticas básicas
stats = processor.get_basic_stats()
print("Estatísticas Básicas:")
for key, value in stats['financial_summary'].items():
    if value:
        print(f"{key}: {value:,.2f}")
```

## 4. Visualizações
```python
# Criar visualizador
viz = EcommerceVisualizer(processed_data)

# Dashboard executivo
viz.create_executive_dashboard()

# Análises específicas
viz.plot_revenue_evolution(period='month')
viz.plot_top_products(metric='revenue', top_n=10)
viz.plot_category_analysis()
```

## 5. Análise de Negócio
```python
# Análise estratégica
analyzer = BusinessAnalyzer(processed_data)
insights = analyzer.generate_comprehensive_insights()

# Exportar insights
analyzer.export_insights_report('insights_report.txt')
```

## 6. Insights e Conclusões
Adicione suas análises e conclusões aqui baseadas nos resultados obtidos.
