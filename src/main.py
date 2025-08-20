import os
import sys
import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Importar módulos do projeto
try:
    from data_processing import DataProcessor, generate_sample_data
    from visualization import EcommerceVisualizer, setup_visualization_style
    from business_analysis import BusinessAnalyzer
except ImportError as e:
    print(f"❌ Erro ao importar módulos: {e}")
    print("📁 Certifique-se de que todos os arquivos .py estão no mesmo diretório")
    sys.exit(1)

class EcommerceAnalysisProject:
    """Classe principal do projeto de análise de e-commerce"""
    
    def __init__(self, project_name="Análise de Vendas E-commerce"):
        self.project_name = project_name
        self.data_processor = None
        self.visualizer = None
        self.business_analyzer = None
        self.processed_data = None
        
        # Criar estrutura de diretórios
        self.create_project_structure()
        
        print("🚀 " + "="*60)
        print(f"   {self.project_name.upper()}")
        print("="*60)
        print("📊 Projeto de Data Science para análise estratégica de vendas")
        print(f"🕒 Iniciado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        print("-"*60)
    
    def create_project_structure(self):
        """Cria estrutura de diretórios do projeto"""
        directories = [
            'data/raw',
            'data/processed',
            'data/sample',
            'reports/figures',
            'reports/insights',
            'notebooks',
            'exports'
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
        
        print("📁 Estrutura de diretórios criada!")
    
    def load_data(self, file_path=None, use_sample_data=True, n_samples=5000):
        """
        Carrega dados para análise
        
        Parameters:
        -----------
        file_path : str, optional
            Caminho para arquivo de dados reais
        use_sample_data : bool, default True
            Se deve usar dados simulados
        n_samples : int, default 5000
            Número de registros de exemplo
        """
        print("\n📥 CARREGANDO DADOS")
        print("-" * 30)
        
        self.data_processor = DataProcessor()
        
        if file_path and os.path.exists(file_path):
            print(f"📂 Carregando dados de: {file_path}")
            raw_data = self.data_processor.load_data(file_path=file_path)
        elif use_sample_data:
            print(f"🎲 Gerando {n_samples:,} registros de dados simulados...")
            raw_data = generate_sample_data(n_samples)
            self.data_processor.load_data(data=raw_data)
            
            # Salvar dados de exemplo
            sample_path = 'data/sample/ecommerce_sample_data.xlsx'
            raw_data.to_excel(sample_path, index=False)
            print(f"💾 Dados de exemplo salvos em: {sample_path}")
        else:
            raise ValueError("É necessário fornecer um arquivo de dados ou usar dados simulados")
        
        return raw_data
    
    def process_data(self, remove_outliers=True):
        """
        Processa e limpa os dados
        
        Parameters:
        -----------
        remove_outliers : bool, default True
            Se deve remover outliers
        """
        print("\n🧹 PROCESSANDO DADOS")
        print("-" * 30)
        
        if self.data_processor is None:
            raise ValueError("Dados não carregados. Execute load_data() primeiro.")
        
        # Verificar qualidade dos dados
        quality_report = self.data_processor.data_quality_check()
        
        # Limpar e processar dados
        self.processed_data = self.data_processor.clean_data(remove_outliers=remove_outliers)
        
        # Salvar dados processados
        processed_path = 'data/processed/ecommerce_processed_data.xlsx'
        self.data_processor.export_processed_data(processed_path)
        print(f"💾 Dados processados salvos em: {processed_path}")
        
        # Estatísticas básicas
        stats = self.data_processor.get_basic_stats()
        print(f"\n📊 RESUMO DOS DADOS PROCESSADOS:")
        print(f"• Total de registros: {stats['total_records']:,}")
        if stats['date_range']['start']:
            print(f"• Período: {stats['date_range']['start']} a {stats['date_range']['end']}")
        print(f"• Produtos únicos: {stats['unique_counts']['produtos']:,}")
        print(f"• Clientes únicos: {stats['unique_counts']['clientes']:,}")
        print(f"• Receita total: R$ {stats['financial_summary']['receita_total']:,.2f}")
        print(f"• Ticket médio: R$ {stats['financial_summary']['ticket_medio']:.2f}")
        
        return self.processed_data
    
    def create_visualizations(self, save_charts=True):
        """
        Cria visualizações dos dados
        
        Parameters:
        -----------
        save_charts : bool, default True
            Se deve salvar gráficos em arquivos
        """
        print("\n📊 CRIANDO VISUALIZAÇÕES")
        print("-" * 30)
        
        if self.processed_data is None:
            raise ValueError("Dados não processados. Execute process_data() primeiro.")
        
        # Configurar estilo das visualizações
        setup_visualization_style()
        
        # Inicializar visualizador
        self.visualizer = EcommerceVisualizer(self.processed_data)
        
        print("📈 Gerando gráficos principais...")
        
        # 1. Dashboard executivo
        print("  → Dashboard Executivo")
        self.visualizer.create_executive_dashboard(
            save_path='reports/figures/executive_dashboard.png' if save_charts else None
        )
        
        # 2. Evolução da receita
        print("  → Evolução da Receita")
        self.visualizer.plot_revenue_evolution(period='month')
        
        # 3. Análise de produtos
        print("  → Top Produtos")
        self.visualizer.plot_top_products(metric='revenue', top_n=10)
        
        # 4. Análise de categorias
        print("  → Análise de Categorias")
        self.visualizer.plot_category_analysis()
        
        # 5. Análise geográfica
        print("  → Análise Geográfica")
        self.visualizer.plot_geographic_analysis()
        
        # 6. Análise de canais
        print("  → Análise de Canais")
        self.visualizer.plot_channel_analysis()
        
        # 7. Análise sazonal
        print("  → Análise Sazonal")
        self.visualizer.plot_seasonal_analysis()
        
        # 8. Análise de clientes
        print("  → Análise de Clientes")
        self.visualizer.plot_customer_analysis()
        
        if save_charts:
            print("💾 Exportando todos os gráficos...")
            self.visualizer.export_charts(output_dir='reports/figures/')
        
        print("✅ Visualizações criadas com sucesso!")
    
    def perform_business_analysis(self):
        """
        Executa análise de negócio completa
        """
        print("\n💼 ANÁLISE DE NEGÓCIO")
        print("-" * 30)
        
        if self.processed_data is None:
            raise ValueError("Dados não processados. Execute process_data() primeiro.")
        
        # Inicializar analisador de negócios
        self.business_analyzer = BusinessAnalyzer(self.processed_data)
        
        print("🔍 Executando análises estratégicas...")
        
        # Gerar insights completos
        insights = self.business_analyzer.generate_comprehensive_insights()
        
        # Exportar relatório de insights
        report_path = 'reports/insights/business_insights_report.txt'
        self.business_analyzer.export_insights_report(report_path)
        
        return insights
    
    def generate_summary_report(self):
        """
        Gera relatório resumo do projeto
        """
        print("\n📋 GERANDO RELATÓRIO RESUMO")
        print("-" * 30)
        
        if self.business_analyzer is None:
            raise ValueError("Análise de negócio não executada. Execute perform_business_analysis() primeiro.")
        
        report_path = 'reports/RELATORIO_EXECUTIVO_VENDAS.md'
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("# 📊 RELATÓRIO EXECUTIVO - ANÁLISE DE VENDAS E-COMMERCE\n\n")
            f.write(f"**Data:** {datetime.now().strftime('%d/%m/%Y')}\n")
            f.write(f"**Projeto:** {self.project_name}\n\n")
            
            f.write("---\n\n")
            
            # Resumo executivo
            f.write("## 🎯 RESUMO EXECUTIVO\n\n")
            
            metrics = self.business_analyzer.insights.get('metricas_principais', {})
            if metrics:
                f.write("### Métricas Principais\n\n")
                f.write(f"- **💰 Receita Total:** R$ {metrics.get('receita_total', 0):,.2f}\n")
                f.write(f"- **🎫 Ticket Médio:** R$ {metrics.get('ticket_medio', 0):.2f}\n")
                f.write(f"- **📦 Total de Pedidos:** {metrics.get('num_pedidos', 0):,}\n")
                f.write(f"- **👥 Clientes Únicos:** {metrics.get('num_clientes', 0):,}\n")
                f.write(f"- **🛍️ Produtos Únicos:** {metrics.get('num_produtos', 0):,}\n")
                f.write(f"- **📅 Período Analisado:** {metrics.get('periodo_dias', 0)} dias\n\n")
            
            # Principais descobertas
            estrategicos = self.business_analyzer.insights.get('estrategicos', {})
            if estrategicos:
                f.write("### 💡 Principais Descobertas\n\n")
                for descoberta in estrategicos.get('principais_descobertas', []):
                    f.write(f"- {descoberta}\n")
                f.write("\n")
            
            # Performance de produtos
            produtos = self.business_analyzer.insights.get('produtos', {})
            if produtos:
                f.write("## 🏆 ANÁLISE DE PRODUTOS\n\n")
                
                produto_destaque = produtos.get('produto_destaque', {})
                if produto_destaque:
                    f.write("### Produto Destaque\n")
                    f.write(f"- **Nome:** {produto_destaque.get('nome', 'N/A')}\n")
                    f.write(f"- **Receita:** R$ {produto_destaque.get('receita', 0):,.2f}\n")
                    f.write(f"- **Participação:** {produto_destaque.get('participacao_receita', 0):.1f}%\n\n")
                
                f.write("### Top 5 Produtos por Receita\n\n")
                top_receita = produtos.get('top_10_receita', {})
                for i, (produto, receita) in enumerate(list(top_receita.items())[:5], 1):
                    f.write(f"{i}. **{produto}:** R$ {receita:,.2f}\n")
                f.write("\n")
            
            # Análise de categorias
            categorias = self.business_analyzer.insights.get('categorias', {})
            if categorias:
                f.write("## 📊 ANÁLISE DE CATEGORIAS\n\n")
                
                cat_lider = categorias.get('categoria_lider', {})
                if cat_lider:
                    f.write("### Categoria Líder\n")
                    f.write(f"- **Nome:** {cat_lider.get('nome', 'N/A')}\n")
                    f.write(f"- **Receita:** R$ {cat_lider.get('receita', 0):,.2f}\n")
                    f.write(f"- **Participação:** {cat_lider.get('participacao', 0):.1f}%\n\n")
            
            # Análise geográfica
            geografia = self.business_analyzer.insights.get('geografia', {})
            if geografia:
                f.write("## 🗺️ ANÁLISE GEOGRÁFICA\n\n")
                
                estado_lider = geografia.get('estado_lider', {})
                if estado_lider:
                    f.write("### Estado Líder\n")
                    f.write(f"- **Estado:** {estado_lider.get('nome', 'N/A')}\n")
                    f.write(f"- **Receita:** R$ {estado_lider.get('receita', 0):,.2f}\n")
                    f.write(f"- **Participação:** {estado_lider.get('participacao', 0):.1f}%\n\n")
            
            # Análise de canais
            canais = self.business_analyzer.insights.get('canais', {})
            if canais:
                f.write("## 📱 ANÁLISE DE CANAIS\n\n")
                
                canal_lider = canais.get('canal_lider', {})
                if canal_lider:
                    f.write("### Canal Líder\n")
                    f.write(f"- **Canal:** {canal_lider.get('nome', 'N/A')}\n")
                    f.write(f"- **Receita:** R$ {canal_lider.get('receita', 0):,.2f}\n")
                    f.write(f"- **Participação:** {canal_lider.get('participacao', 0):.1f}%\n\n")
            
            # Recomendações
            if estrategicos:
                f.write("## 🚀 RECOMENDAÇÕES ESTRATÉGICAS\n\n")
                
                f.write("### Ações Imediatas\n\n")
                for rec in estrategicos.get('recomendacoes_imediatas', []):
                    f.write(f"- {rec}\n")
                f.write("\n")
                
                f.write("### Ações de Médio Prazo\n\n")
                for rec in estrategicos.get('recomendacoes_medio_prazo', []):
                    f.write(f"- {rec}\n")
                f.write("\n")
                
                f.write("### KPIs para Monitoramento\n\n")
                for kpi in estrategicos.get('kpis_monitoramento', []):
                    f.write(f"- {kpi}\n")
                f.write("\n")
            
            f.write("---\n\n")
            f.write("## 📁 ARQUIVOS GERADOS\n\n")
            f.write("- **Dados Processados:** `data/processed/ecommerce_processed_data.xlsx`\n")
            f.write("- **Gráficos:** `reports/figures/`\n")
            f.write("- **Insights Detalhados:** `reports/insights/business_insights_report.txt`\n")
            f.write("- **Dashboard Executivo:** `reports/figures/executive_dashboard.png`\n\n")
            
            f.write(f"**Relatório gerado em:** {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
        
        print(f"✅ Relatório executivo gerado: {report_path}")
        return report_path
    
    def run_complete_analysis(self, file_path=None, n_samples=5000):
        """
        Executa análise completa do projeto
        
        Parameters:
        -----------
        file_path : str, optional
            Caminho para arquivo de dados reais
        n_samples : int, default 5000
            Número de amostras para dados simulados
        """
        try:
            start_time = datetime.now()
            
            # 1. Carregar dados
            self.load_data(file_path=file_path, n_samples=n_samples)
            
            # 2. Processar dados
            self.process_data(remove_outliers=True)
            
            # 3. Criar visualizações
            self.create_visualizations(save_charts=True)
            
            # 4. Análise de negócio
            insights = self.perform_business_analysis()
            
            # 5. Relatório executivo
            report_path = self.generate_summary_report()
            
            # Tempo de execução
            execution_time = (datetime.now() - start_time).total_seconds()
            
            # Resumo final
            print("\n" + "="*60)
            print("✅ ANÁLISE COMPLETA FINALIZADA COM SUCESSO!")
            print("="*60)
            print(f"⏱️  Tempo de execução: {execution_time:.1f} segundos")
            print(f"📊 Total de registros analisados: {len(self.processed_data):,}")
            print(f"📈 Gráficos gerados: 8+ visualizações")
            print(f"💡 Insights identificados: {len(insights)} categorias de análise")
            print(f"📋 Relatório executivo: {report_path}")
            
            print("\n📁 ARQUIVOS PRINCIPAIS GERADOS:")
            print("  → data/processed/ecommerce_processed_data.xlsx")
            print("  → reports/figures/executive_dashboard.png")
            print("  → reports/insights/business_insights_report.txt")
            print("  → reports/RELATORIO_EXECUTIVO_VENDAS.md")
            
            print("\n🎯 PRÓXIMOS PASSOS SUGERIDOS:")
            print("  → Revisar insights no relatório executivo")
            print("  → Implementar recomendações estratégicas")
            print("  → Configurar monitoramento de KPIs")
            print("  → Apresentar resultados para stakeholders")
            print("-" * 60)
            
            return {
                'execution_time': execution_time,
                'records_analyzed': len(self.processed_data),
                'insights_generated': insights,
                'report_path': report_path
            }
            
        except Exception as e:
            print(f"\n❌ ERRO DURANTE A EXECUÇÃO: {str(e)}")
            print("🔧 Verifique os dados de entrada e tente novamente")
            raise e
    
    def create_jupyter_notebook_template(self):
        """
        Cria template de notebook Jupyter para análise interativa
        """
        notebook_content = '''# Análise de Vendas E-commerce - Notebook Interativo

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
'''
        
        notebook_path = 'notebooks/analise_vendas_interativa.md'
        with open(notebook_path, 'w', encoding='utf-8') as f:
            f.write(notebook_content)
        
        print(f"📓 Template de notebook criado: {notebook_path}")
        return notebook_path

def main():
    """Função principal para execução do projeto"""
    
    print("🎯 PROJETO DE ANÁLISE DE VENDAS E-COMMERCE")
    print("🚀 Iniciando análise completa...")
    
    # Criar instância do projeto
    project = EcommerceAnalysisProject("Análise Estratégica de Vendas E-commerce")
    
    # Executar análise completa
    try:
        # Para usar dados reais, substitua file_path pelo caminho do seu arquivo
        # project.run_complete_analysis(file_path='data/raw/seus_dados.xlsx')
        
        # Usando dados simulados (para demonstração)
        results = project.run_complete_analysis(n_samples=5000)
        
        # Criar template de notebook
        project.create_jupyter_notebook_template()
        
        print("\n🎉 PROJETO CONCLUÍDO COM SUCESSO!")
        print("📊 Todos os arquivos foram gerados e estão prontos para uso")
        
    except Exception as e:
        print(f"\n❌ Erro na execução: {str(e)}")
        print("🔧 Verifique os requisitos e tente novamente")

if __name__ == "__main__":
    main()