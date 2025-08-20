# 📊 Análise de Vendas E-commerce - Projeto Data Science

## 🎯 Objetivo do Projeto
Este projeto demonstra uma análise completa de dados de vendas de um e-commerce, utilizando Python para extrair insights estratégicos que podem orientar decisões de negócio. O foco está na limpeza, exploração e visualização de dados para gerar recomendações acionáveis.

## 🚀 Tecnologias Utilizadas

### Core Libraries
- **Python 3.8+**
- **Pandas**: Manipulação e análise de dados
- **NumPy**: Computação numérica e álgebra linear
- **Matplotlib**: Visualizações estáticas
- **Seaborn**: Visualizações estatísticas avançadas

### Ambiente de Desenvolvimento
- **Jupyter Notebook**: Desenvolvimento interativo
- **Git**: Controle de versão

## 📁 Estrutura do Projeto

```
ecommerce-analysis/
│
├── data/
│   ├── raw/                    # Dados brutos (Excel/CSV)
│   ├── processed/              # Dados limpos e processados
│   └── sample/                 # Dados de exemplo
│
├── notebooks/
│   ├── 01_exploratory_analysis.ipynb    # Análise exploratória
│   ├── 02_data_cleaning.ipynb           # Limpeza de dados
│   └── 03_business_insights.ipynb      # Insights de negócio
│
├── src/
│   ├── data_processing.py      # Funções de processamento
│   ├── visualization.py        # Funções de visualização
│   └── analysis.py             # Funções de análise
│
├── reports/
│   ├── figures/                # Gráficos gerados
│   └── final_report.pdf        # Relatório final
│
├── requirements.txt            # Dependências do projeto
└── README.md                   # Este arquivo
```

## 📊 Dataset

### Estrutura dos Dados
O dataset contém informações de vendas com as seguintes colunas:

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `pedido_id` | string | Identificador único do pedido |
| `data_pedido` | datetime | Data de realização do pedido |
| `cliente_id` | int | Identificador do cliente |
| `produto` | string | Nome do produto |
| `categoria` | string | Categoria do produto |
| `quantidade` | int | Quantidade vendida |
| `preco_unitario` | float | Preço unitário do produto |
| `valor_total` | float | Valor total do pedido |
| `estado` | string | Estado do cliente |
| `canal_venda` | string | Canal de venda utilizado |

### Fonte dos Dados
- **Dados Simulados**: Para demonstração do projeto
- **Dados Reais**: Substitua pela importação de planilhas Excel/CSV reais

## 🔍 Análises Realizadas

### 1. Análise Exploratória (EDA)
- ✅ Estatísticas descritivas
- ✅ Identificação de valores nulos
- ✅ Detecção e tratamento de outliers
- ✅ Distribuição das variáveis numéricas

### 2. Métricas de Negócio
- 💰 **Receita Total**: Faturamento geral da empresa
- 🎫 **Ticket Médio**: Valor médio por pedido
- 📦 **Volume de Pedidos**: Quantidade total de transações
- 🏆 **Top Produtos**: Ranking por vendas e receita
- 📊 **Análise por Categoria**: Performance de cada segmento

### 3. Análise Temporal
- 📅 **Sazonalidade**: Identificação de padrões sazonais
- 📈 **Tendências**: Evolução das vendas ao longo do tempo
- 🔥 **Heatmap**: Vendas por dia da semana e mês

### 4. Análise Geográfica
- 🗺️ **Vendas por Estado**: Distribuição geográfica da receita
- 🎯 **Concentração Regional**: Identificação de mercados principais

### 5. Análise de Canais
- 📱 **Performance por Canal**: Online, Marketplace, Mobile
- 💹 **Comparativo de Eficiência**: Ticket médio por canal

### 6. Segmentação de Clientes
- 👥 **Análise RFV**: Recência, Frequência, Valor
- 🎖️ **Segmentação**: VIP, Premium, Ativo, Regular, Inativo
- 💎 **Top Clientes**: Identificação dos principais compradores

## 📈 Principais Insights

### Insights de Produto
- 🏆 Identificação dos produtos com maior potencial de receita
- 📊 Categorias com melhor performance financeira
- 🎯 Oportunidades de cross-selling e up-selling

### Insights de Marketing
- 📱 Canais de venda mais eficazes
- 🗺️ Regiões com maior potencial de expansão
- 📅 Períodos sazonais para campanhas

### Insights de Operação
- 📦 Padrões de demanda para gestão de estoque
- 🚚 Otimização logística por região
- 💰 Estratégias de precificação

## 🚀 Como Executar o Projeto

### 1. Clone o Repositório
```bash
git clone https://github.com/seu-usuario/ecommerce-analysis.git
cd ecommerce-analysis
```

### 2. Instale as Dependências
```bash
pip install -r requirements.txt
```

### 3. Execute a Análise
```bash
# Via Jupyter Notebook
jupyter notebook notebooks/01_exploratory_analysis.ipynb

# Via Python script
python src/main_analysis.py
```

### 4. Visualize os Resultados
Os gráficos e relatórios serão salvos na pasta `reports/figures/`

## 📋 Requirements.txt

```
pandas>=1.5.0
numpy>=1.21.0
matplotlib>=3.5.0
seaborn>=0.11.0
jupyter>=1.0.0
openpyxl>=3.0.0
xlrd>=2.0.0
```

## 🔄 Próximos Passos

### Análises Avançadas
- [ ] **Machine Learning**: Previsão de vendas
- [ ] **Análise de Coorte**: Comportamento de clientes ao longo do tempo
- [ ] **Market Basket Analysis**: Produtos frequentemente comprados juntos
- [ ] **Modelagem Preditiva**: Churn de clientes

### Melhorias Técnicas
- [ ] **Dashboard Interativo**: Streamlit ou Plotly Dash
- [ ] **Automatização**: Scripts para atualização automática
- [ ] **API**: Endpoint para consultas em tempo real
- [ ] **Deploy**: Hospedagem em nuvem

## 👨‍💻 Sobre o Autor

**Endriw Costa**
- 📧 Email: endriwcosta3@gmail.com
- 💼 LinkedIn: [linkedin.com/in/endriwcosta](www.linkedin.com/in/endriwcosta)
- 🌐 Portfolio: [github.com/costaendriw](https://github.com/costaendriw)


## 🤝 Contribuições

Contribuições são sempre bem-vindas! Para contribuir:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📊 Resultados do Projeto

Este projeto demonstra:
- ✅ **Competência Técnica**: Domínio de Python, Pandas e visualização
- ✅ **Pensamento Analítico**: Capacidade de extrair insights de dados
- ✅ **Visão de Negócio**: Conexão entre dados e decisões estratégicas
- ✅ **Comunicação**: Apresentação clara de resultados complexos

---

⭐ **Se este projeto foi útil para você, não esqueça de dar uma estrela!**@
