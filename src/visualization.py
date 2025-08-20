import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Configuração global para visualizações
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")
plt.rcParams['font.size'] = 10
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['axes.labelsize'] = 10
plt.rcParams['xtick.labelsize'] = 9
plt.rcParams['ytick.labelsize'] = 9
plt.rcParams['legend.fontsize'] = 9

class EcommerceVisualizer:
    """Classe para criar visualizações de dados de e-commerce"""
    
    def __init__(self, data):
        """
        Inicializa o visualizador com os dados
        
        Parameters:
        -----------
        data : pd.DataFrame
            DataFrame com dados de vendas processados
        """
        self.data = data
        self.colors = {
            'primary': '#2E86AB',
            'secondary': '#A23B72',
            'accent': '#F18F01',
            'success': '#C73E1D',
            'info': '#6C5CE7',
            'warning': '#FDCB6E',
            'dark': '#2D3436',
            'light': '#DDD'
        }
    
    def plot_revenue_evolution(self, period='month', figsize=(12, 6)):
        """
        Plota evolução da receita ao longo do tempo
        
        Parameters:
        -----------
        period : str, default 'month'
            Período de agregação ('day', 'week', 'month', 'quarter')
        figsize : tuple, default (12, 6)
            Tamanho da figura
        """
        plt.figure(figsize=figsize)
        
        # Preparar dados
        if period == 'day':
            grouped = self.data.groupby(self.data['data_pedido'].dt.date)['valor_total'].sum()
            title = 'Evolução Diária da Receita'
            xlabel = 'Data'
        elif period == 'week':
            grouped = self.data.groupby(self.data['data_pedido'].dt.to_period('W'))['valor_total'].sum()
            title = 'Evolução Semanal da Receita'
            xlabel = 'Semana'
        elif period == 'month':
            grouped = self.data.groupby(self.data['data_pedido'].dt.to_period('M'))['valor_total'].sum()
            title = 'Evolução Mensal da Receita'
            xlabel = 'Mês'
        elif period == 'quarter':
            grouped = self.data.groupby(self.data['data_pedido'].dt.to_period('Q'))['valor_total'].sum()
            title = 'Evolução Trimestral da Receita'
            xlabel = 'Trimestre'
        
        # Criar gráfico de linha
        grouped.plot(kind='line', marker='o', linewidth=3, markersize=6, color=self.colors['primary'])
        
        # Adicionar linha de tendência
        x = range(len(grouped))
        z = np.polyfit(x, grouped.values, 1)
        p = np.poly1d(z)
        plt.plot(x, p(x), "--", color=self.colors['secondary'], alpha=0.8, linewidth=2)
        
        plt.title(title, fontsize=16, fontweight='bold', pad=20)
        plt.xlabel(xlabel)
        plt.ylabel('Receita (R$)')
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        
        # Formatar valores no eixo Y
        ax = plt.gca()
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'R$ {x/1000:.0f}K'))
        
        plt.tight_layout()
        plt.show()
    
    def plot_top_products(self, metric='revenue', top_n=10, figsize=(12, 8)):
        """
        Plota top produtos por receita ou quantidade
        
        Parameters:
        -----------
        metric : str, default 'revenue'
            Métrica para ranking ('revenue', 'quantity', 'orders')
        top_n : int, default 10
            Número de produtos no ranking
        """
        plt.figure(figsize=figsize)
        
        if metric == 'revenue':
            data_plot = self.data.groupby('produto')['valor_total'].sum().sort_values(ascending=False).head(top_n)
            title = f'Top {top_n} Produtos por Receita'
            xlabel = 'Receita (R$)'
        elif metric == 'quantity':
            data_plot = self.data.groupby('produto')['quantidade'].sum().sort_values(ascending=False).head(top_n)
            title = f'Top {top_n} Produtos por Quantidade Vendida'
            xlabel = 'Quantidade'
        elif metric == 'orders':
            data_plot = self.data.groupby('produto').size().sort_values(ascending=False).head(top_n)
            title = f'Top {top_n} Produtos por Número de Pedidos'
            xlabel = 'Número de Pedidos'
        
        # Criar gráfico de barras horizontais
        bars = plt.barh(range(len(data_plot)), data_plot.values, 
                       color=[self.colors['primary'] if i == 0 else self.colors['info'] 
                             for i in range(len(data_plot))])
        
        # Personalizar
        plt.yticks(range(len(data_plot)), data_plot.index)
        plt.xlabel(xlabel)
        plt.title(title, fontsize=16, fontweight='bold', pad=20)
        plt.gca().invert_yaxis()
        
        # Adicionar valores nas barras
        for i, (bar, value) in enumerate(zip(bars, data_plot.values)):
            if metric == 'revenue':
                plt.text(value + max(data_plot.values) * 0.01, i, f'R$ {value:,.0f}', 
                        va='center', fontweight='bold')
            else:
                plt.text(value + max(data_plot.values) * 0.01, i, f'{value:,.0f}', 
                        va='center', fontweight='bold')
        
        plt.tight_layout()
        plt.show()
    
    def plot_category_analysis(self, figsize=(15, 10)):
        """
        Plota análise completa por categoria
        """
        fig, axes = plt.subplots(2, 2, figsize=figsize)
        fig.suptitle('Análise Completa por Categoria', fontsize=18, fontweight='bold')
        
        # 1. Receita por categoria
        receita_cat = self.data.groupby('categoria')['valor_total'].sum().sort_values(ascending=False)
        receita_cat.plot(kind='bar', ax=axes[0,0], color=self.colors['primary'])
        axes[0,0].set_title('Receita por Categoria')
        axes[0,0].set_ylabel('Receita (R$)')
        axes[0,0].tick_params(axis='x', rotation=45)
        
        # 2. Ticket médio por categoria
        ticket_cat = self.data.groupby('categoria')['valor_total'].mean().sort_values(ascending=False)
        ticket_cat.plot(kind='bar', ax=axes[0,1], color=self.colors['secondary'])
        axes[0,1].set_title('Ticket Médio por Categoria')
        axes[0,1].set_ylabel('Ticket Médio (R$)')
        axes[0,1].tick_params(axis='x', rotation=45)
        
        # 3. Número de pedidos por categoria
        pedidos_cat = self.data.groupby('categoria').size().sort_values(ascending=False)
        pedidos_cat.plot(kind='bar', ax=axes[1,0], color=self.colors['accent'])
        axes[1,0].set_title('Número de Pedidos por Categoria')
        axes[1,0].set_ylabel('Número de Pedidos')
        axes[1,0].tick_params(axis='x', rotation=45)
        
        # 4. Quantidade vendida por categoria
        qtd_cat = self.data.groupby('categoria')['quantidade'].sum().sort_values(ascending=False)
        qtd_cat.plot(kind='bar', ax=axes[1,1], color=self.colors['success'])
        axes[1,1].set_title('Quantidade Vendida por Categoria')
        axes[1,1].set_ylabel('Quantidade')
        axes[1,1].tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        plt.show()
    
    def plot_geographic_analysis(self, figsize=(15, 6)):
        """
        Plota análise geográfica das vendas
        """
        fig, axes = plt.subplots(1, 2, figsize=figsize)
        fig.suptitle('Análise Geográfica das Vendas', fontsize=16, fontweight='bold')
        
        # 1. Receita por estado
        receita_estado = self.data.groupby('estado')['valor_total'].sum().sort_values(ascending=False)
        receita_estado.plot(kind='bar', ax=axes[0], color=self.colors['primary'])
        axes[0].set_title('Receita por Estado')
        axes[0].set_ylabel('Receita (R$)')
        axes[0].tick_params(axis='x', rotation=45)
        
        # 2. Número de clientes únicos por estado
        clientes_estado = self.data.groupby('estado')['cliente_id'].nunique().sort_values(ascending=False)
        clientes_estado.plot(kind='bar', ax=axes[1], color=self.colors['info'])
        axes[1].set_title('Clientes Únicos por Estado')
        axes[1].set_ylabel('Número de Clientes')
        axes[1].tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        plt.show()
    
    def plot_channel_analysis(self, figsize=(12, 8)):
        """
        Plota análise de canais de venda
        """
        fig, axes = plt.subplots(2, 2, figsize=figsize)
        fig.suptitle('Análise de Canais de Venda', fontsize=16, fontweight='bold')
        
        # 1. Distribuição de receita por canal (Pizza)
        receita_canal = self.data.groupby('canal_venda')['valor_total'].sum()
        colors = [self.colors['primary'], self.colors['secondary'], self.colors['accent']]
        axes[0,0].pie(receita_canal.values, labels=receita_canal.index, autopct='%1.1f%%', 
                     colors=colors, startangle=90)
        axes[0,0].set_title('Distribuição de Receita por Canal')
        
        # 2. Ticket médio por canal
        ticket_canal = self.data.groupby('canal_venda')['valor_total'].mean()
        ticket_canal.plot(kind='bar', ax=axes[0,1], color=colors)
        axes[0,1].set_title('Ticket Médio por Canal')
        axes[0,1].set_ylabel('Ticket Médio (R$)')
        axes[0,1].tick_params(axis='x', rotation=45)
        
        # 3. Número de pedidos por canal
        pedidos_canal = self.data.groupby('canal_venda').size()
        pedidos_canal.plot(kind='bar', ax=axes[1,0], color=colors)
        axes[1,0].set_title('Número de Pedidos por Canal')
        axes[1,0].set_ylabel('Número de Pedidos')
        axes[1,0].tick_params(axis='x', rotation=45)
        
        # 4. Evolução mensal por canal
        pivot_canal = self.data.groupby([self.data['data_pedido'].dt.to_period('M'), 'canal_venda'])['valor_total'].sum().unstack()
        pivot_canal.plot(kind='line', ax=axes[1,1], marker='o', linewidth=2)
        axes[1,1].set_title('Evolução Mensal por Canal')
        axes[1,1].set_ylabel('Receita (R$)')
        axes[1,1].legend(title='Canal')
        
        plt.tight_layout()
        plt.show()
    
    def plot_seasonal_analysis(self, figsize=(15, 10)):
        """
        Plota análise sazonal das vendas
        """
        fig, axes = plt.subplots(2, 2, figsize=figsize)
        fig.suptitle('Análise Sazonal das Vendas', fontsize=16, fontweight='bold')
        
        # 1. Vendas por mês
        vendas_mes = self.data.groupby(self.data['data_pedido'].dt.month)['valor_total'].sum()
        meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 
                'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
        vendas_mes.index = [meses[i-1] for i in vendas_mes.index]
        vendas_mes.plot(kind='line', ax=axes[0,0], marker='o', color=self.colors['primary'], linewidth=3)
        axes[0,0].set_title('Vendas por Mês')
        axes[0,0].set_ylabel('Receita (R$)')
        axes[0,0].grid(True, alpha=0.3)
        
        # 2. Vendas por trimestre
        vendas_trimestre = self.data.groupby(self.data['data_pedido'].dt.quarter)['valor_total'].sum()
        trimestres = ['Q1', 'Q2', 'Q3', 'Q4']
        vendas_trimestre.index = [trimestres[i-1] for i in vendas_trimestre.index]
        vendas_trimestre.plot(kind='bar', ax=axes[0,1], color=self.colors['secondary'])
        axes[0,1].set_title('Vendas por Trimestre')
        axes[0,1].set_ylabel('Receita (R$)')
        axes[0,1].tick_params(axis='x', rotation=0)
        
        # 3. Vendas por dia da semana
        dias = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']
        vendas_dia = self.data.groupby(self.data['data_pedido'].dt.day_name())['valor_total'].sum()
        # Reordenar para começar na segunda-feira
        order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        vendas_dia = vendas_dia.reindex(order)
        vendas_dia.index = dias
        vendas_dia.plot(kind='bar', ax=axes[1,0], color=self.colors['accent'])
        axes[1,0].set_title('Vendas por Dia da Semana')
        axes[1,0].set_ylabel('Receita (R$)')
        axes[1,0].tick_params(axis='x', rotation=45)
        
        # 4. Heatmap: Vendas por dia da semana vs mês
        pivot_sazonal = self.data.groupby([self.data['data_pedido'].dt.day_name(), 
                                          self.data['data_pedido'].dt.month])['valor_total'].sum().unstack()
        pivot_sazonal = pivot_sazonal.reindex(order)
        pivot_sazonal.index = ['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sab', 'Dom']
        pivot_sazonal.columns = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun',
                                'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'][:len(pivot_sazonal.columns)]
        
        sns.heatmap(pivot_sazonal, annot=False, cmap='YlOrRd', ax=axes[1,1], cbar_kws={'label': 'Receita'})
        axes[1,1].set_title('Heatmap: Vendas por Dia vs Mês')
        axes[1,1].set_xlabel('Mês')
        axes[1,1].set_ylabel('Dia da Semana')
        
        plt.tight_layout()
        plt.show()
    
    def plot_customer_analysis(self, figsize=(15, 10)):
        """
        Plota análise de clientes (RFV e segmentação)
        """
        # Preparar dados de clientes
        hoje = self.data['data_pedido'].max()
        clientes = self.data.groupby('cliente_id').agg({
            'data_pedido': lambda x: (hoje - x.max()).days,  # Recência
            'pedido_id': 'count',  # Frequência
            'valor_total': 'sum'   # Valor
        })
        clientes.columns = ['Recencia', 'Frequencia', 'Valor']
        
        # Segmentação básica
        def segmentar_cliente(row):
            if row['Valor'] >= clientes['Valor'].quantile(0.8) and row['Frequencia'] >= 3:
                return 'VIP'
            elif row['Valor'] >= clientes['Valor'].quantile(0.6) or row['Frequencia'] >= 2:
                return 'Premium'
            elif row['Recencia'] <= 30:
                return 'Ativo'
            elif row['Recencia'] <= 90:
                return 'Regular'
            else:
                return 'Inativo'
        
        clientes['Segmento'] = clientes.apply(segmentar_cliente, axis=1)
        
        fig, axes = plt.subplots(2, 2, figsize=figsize)
        fig.suptitle('Análise de Clientes', fontsize=16, fontweight='bold')
        
        # 1. Distribuição de segmentos
        segmentos = clientes['Segmento'].value_counts()
        colors = [self.colors['success'], self.colors['primary'], self.colors['accent'], 
                 self.colors['secondary'], self.colors['warning']][:len(segmentos)]
        axes[0,0].pie(segmentos.values, labels=segmentos.index, autopct='%1.1f%%', 
                     colors=colors, startangle=90)
        axes[0,0].set_title('Distribuição de Segmentos de Clientes')
        
        # 2. Valor médio por segmento
        valor_segmento = clientes.groupby('Segmento')['Valor'].mean().sort_values(ascending=False)
        valor_segmento.plot(kind='bar', ax=axes[0,1], color=colors)
        axes[0,1].set_title('Valor Médio por Segmento')
        axes[0,1].set_ylabel('Valor Médio (R$)')
        axes[0,1].tick_params(axis='x', rotation=45)
        
        # 3. Scatter plot: Frequência vs Valor
        for segmento in clientes['Segmento'].unique():
            data_seg = clientes[clientes['Segmento'] == segmento]
            axes[1,0].scatter(data_seg['Frequencia'], data_seg['Valor'], 
                             label=segmento, alpha=0.7, s=50)
        axes[1,0].set_xlabel('Frequência de Compras')
        axes[1,0].set_ylabel('Valor Total (R$)')
        axes[1,0].set_title('Dispersão: Frequência vs Valor')
        axes[1,0].legend()
        axes[1,0].grid(True, alpha=0.3)
        
        # 4. Distribuição de recência
        axes[1,1].hist(clientes['Recencia'], bins=30, color=self.colors['info'], alpha=0.7, edgecolor='black')
        axes[1,1].set_xlabel('Dias desde a última compra')
        axes[1,1].set_ylabel('Número de Clientes')
        axes[1,1].set_title('Distribuição de Recência')
        axes[1,1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
    
    def create_executive_dashboard(self, save_path=None, figsize=(20, 15)):
        """
        Cria um dashboard executivo completo
        
        Parameters:
        -----------
        save_path : str, optional
            Caminho para salvar o dashboard
        """
        fig = plt.figure(figsize=figsize)
        gs = fig.add_gridspec(4, 4, hspace=0.3, wspace=0.3)
        
        # Título principal
        fig.suptitle('📊 DASHBOARD EXECUTIVO - ANÁLISE DE VENDAS E-COMMERCE', 
                    fontsize=20, fontweight='bold', y=0.98)
        
        # 1. KPIs principais (top)
        ax_kpi = fig.add_subplot(gs[0, :])
        ax_kpi.axis('off')
        
        # Calcular KPIs
        receita_total = self.data['valor_total'].sum()
        ticket_medio = self.data['valor_total'].mean()
        num_pedidos = len(self.data)
        num_clientes = self.data['cliente_id'].nunique()
        
        # Criar caixas de KPI
        kpis = [
            ('💰 RECEITA TOTAL', f'R$ {receita_total:,.0f}', self.colors['success']),
            ('🎫 TICKET MÉDIO', f'R$ {ticket_medio:.0f}', self.colors['primary']),
            ('📦 PEDIDOS', f'{num_pedidos:,}', self.colors['accent']),
            ('👥 CLIENTES', f'{num_clientes:,}', self.colors['secondary'])
        ]
        
        for i, (label, value, color) in enumerate(kpis):
            x = i * 0.25 + 0.125
            # Caixa do KPI
            bbox = dict(boxstyle="round,pad=0.3", facecolor=color, alpha=0.2, edgecolor=color)
            ax_kpi.text(x, 0.7, label, ha='center', va='center', fontsize=14, fontweight='bold',
                       transform=ax_kpi.transAxes)
            ax_kpi.text(x, 0.3, value, ha='center', va='center', fontsize=18, fontweight='bold',
                       color=color, transform=ax_kpi.transAxes, bbox=bbox)
        
        # 2. Evolução da receita
        ax1 = fig.add_subplot(gs[1, :2])
        vendas_mensais = self.data.groupby(self.data['data_pedido'].dt.to_period('M'))['valor_total'].sum()
        vendas_mensais.plot(kind='line', ax=ax1, marker='o', linewidth=3, markersize=6, color=self.colors['primary'])
        ax1.set_title('📈 Evolução Mensal da Receita', fontweight='bold')
        ax1.set_ylabel('Receita (R$)')
        ax1.grid(True, alpha=0.3)
        ax1.tick_params(axis='x', rotation=45)
        
        # 3. Top produtos
        ax2 = fig.add_subplot(gs[1, 2:])
        top_produtos = self.data.groupby('produto')['valor_total'].sum().sort_values(ascending=False).head(5)
        bars = ax2.barh(range(len(top_produtos)), top_produtos.values, color=self.colors['info'])
        ax2.set_yticks(range(len(top_produtos)))
        ax2.set_yticklabels([p[:25] + '...' if len(p) > 25 else p for p in top_produtos.index])
        ax2.set_title('🏆 Top 5 Produtos por Receita', fontweight='bold')
        ax2.set_xlabel('Receita (R$)')
        ax2.invert_yaxis()
        
        # 4. Análise por categoria
        ax3 = fig.add_subplot(gs[2, :2])
        receita_categoria = self.data.groupby('categoria')['valor_total'].sum().sort_values(ascending=False)
        receita_categoria.plot(kind='bar', ax=ax3, color=self.colors['accent'])
        ax3.set_title('📊 Receita por Categoria', fontweight='bold')
        ax3.set_ylabel('Receita (R$)')
        ax3.tick_params(axis='x', rotation=45)
        
        # 5. Canais de venda
        ax4 = fig.add_subplot(gs[2, 2:])
        canal_receita = self.data.groupby('canal_venda')['valor_total'].sum()
        colors_pie = [self.colors['primary'], self.colors['secondary'], self.colors['accent']]
        ax4.pie(canal_receita.values, labels=canal_receita.index, autopct='%1.1f%%',
               colors=colors_pie, startangle=90)
        ax4.set_title('📱 Distribuição por Canal', fontweight='bold')
        
        # 6. Geografia
        ax5 = fig.add_subplot(gs[3, :2])
        top_estados = self.data.groupby('estado')['valor_total'].sum().sort_values(ascending=False).head(8)
        top_estados.plot(kind='bar', ax=ax5, color=self.colors['success'])
        ax5.set_title('🗺️ Top Estados por Receita', fontweight='bold')
        ax5.set_ylabel('Receita (R$)')
        ax5.tick_params(axis='x', rotation=45)
        
        # 7. Sazonalidade
        ax6 = fig.add_subplot(gs[3, 2:])
        vendas_trimestre = self.data.groupby(self.data['data_pedido'].dt.quarter)['valor_total'].sum()
        trimestres = ['Q1', 'Q2', 'Q3', 'Q4']
        vendas_trimestre.index = [trimestres[i-1] for i in vendas_trimestre.index if i <= 4]
        vendas_trimestre.plot(kind='bar', ax=ax6, color=self.colors['warning'])
        ax6.set_title('📅 Vendas por Trimestre', fontweight='bold')
        ax6.set_ylabel('Receita (R$)')
        ax6.tick_params(axis='x', rotation=0)
        
        # Adicionar nota de rodapé
        fig.text(0.5, 0.02, f'Dashboard gerado em {datetime.now().strftime("%d/%m/%Y %H:%M")} | Dados: {len(self.data):,} registros', 
                ha='center', fontsize=10, style='italic')
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✅ Dashboard salvo em: {save_path}")
        
        plt.show()
    
    def export_charts(self, output_dir='reports/figures/'):
        """
        Exporta todos os gráficos individuais
        
        Parameters:
        -----------
        output_dir : str, default 'reports/figures/'
            Diretório para salvar os gráficos
        """
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        print("📊 Exportando gráficos...")
        
        # Lista de gráficos para exportar
        charts = [
            ('revenue_evolution', lambda: self.plot_revenue_evolution(period='month')),
            ('top_products_revenue', lambda: self.plot_top_products(metric='revenue')),
            ('category_analysis', lambda: self.plot_category_analysis()),
            ('geographic_analysis', lambda: self.plot_geographic_analysis()),
            ('channel_analysis', lambda: self.plot_channel_analysis()),
            ('seasonal_analysis', lambda: self.plot_seasonal_analysis()),
            ('customer_analysis', lambda: self.plot_customer_analysis()),
            ('executive_dashboard', lambda: self.create_executive_dashboard())
        ]
        
        for chart_name, chart_func in charts:
            try:
                chart_func()
                plt.savefig(f'{output_dir}{chart_name}.png', dpi=300, bbox_inches='tight')
                plt.close()
                print(f"✅ {chart_name}.png exportado")
            except Exception as e:
                print(f"❌ Erro ao exportar {chart_name}: {str(e)}")
        
        print(f"🎯 Gráficos exportados para: {output_dir}")

# Função de utilidade para configuração rápida
def setup_visualization_style():
    """Configura estilo padrão para todas as visualizações"""
    plt.style.use('seaborn-v0_8-whitegrid')
    sns.set_palette("husl")
    plt.rcParams.update({
        'figure.figsize': (12, 6),
        'font.size': 10,
        'axes.titlesize': 14,
        'axes.labelsize': 12,
        'xtick.labelsize': 10,
        'ytick.labelsize': 10,
        'legend.fontsize': 10,
        'figure.titlesize': 16
    })
    print("🎨 Estilo de visualização configurado!")

# Exemplo de uso
if __name__ == "__main__":
    # Simular dados para teste
    from data_processing import generate_sample_data
    
    # Gerar dados de exemplo
    sample_data = generate_sample_data(2000)
    
    # Criar visualizador
    viz = EcommerceVisualizer(sample_data)
    
    # Criar dashboard executivo
    viz.create_executive_dashboard()
    
    print("✅ Exemplo de visualização executado com sucesso!")