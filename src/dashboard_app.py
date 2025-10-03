import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import sys
import os

# Importar módulos do projeto
from data_processing import DataProcessor, generate_sample_data
from business_analysis import BusinessAnalyzer

# Configuração da página
st.set_page_config(
    page_title="E-commerce Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #2E86AB;
        text-align: center;
        padding: 1rem 0;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #2E86AB;
    }
    .insight-box {
        background-color: #e8f4f8;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Cache para dados processados
@st.cache_data
def load_and_process_data(file_path=None, use_sample=True, n_samples=5000):
    """Carrega e processa dados com cache"""
    processor = DataProcessor()
    
    if file_path:
        processor.load_data(file_path=file_path)
    elif use_sample:
        sample_data = generate_sample_data(n_samples)
        processor.load_data(data=sample_data)
    
    processed_data = processor.clean_data(remove_outliers=True)
    return processed_data, processor

@st.cache_data
def analyze_business(_data):
    """Análise de negócio com cache"""
    analyzer = BusinessAnalyzer(_data)
    insights = analyzer.generate_comprehensive_insights()
    return insights, analyzer

# Cabeçalho
st.markdown('<div class="main-header">📊 Dashboard de Análise de Vendas E-commerce</div>', unsafe_allow_html=True)
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("⚙️ Configurações")
    
    # Opções de fonte de dados
    data_source = st.radio(
        "Fonte de Dados:",
        ["Dados Simulados", "Upload de Arquivo", "Arquivo Existente"]
    )
    
    uploaded_file = None
    existing_file = None
    n_samples = 5000
    
    if data_source == "Dados Simulados":
        n_samples = st.slider("Número de registros:", 1000, 10000, 5000, 500)
        st.info(f"Gerando {n_samples:,} registros simulados")
        
    elif data_source == "Upload de Arquivo":
        uploaded_file = st.file_uploader(
            "Upload CSV ou Excel:",
            type=['csv', 'xlsx', 'xls']
        )
        
    elif data_source == "Arquivo Existente":
        # Buscar arquivos em data/processed ou data/sample
        file_options = []
        for folder in ['data/processed', 'data/sample', 'data/raw']:
            if os.path.exists(folder):
                files = [f for f in os.listdir(folder) if f.endswith(('.csv', '.xlsx', '.xls'))]
                file_options.extend([os.path.join(folder, f) for f in files])
        
        if file_options:
            existing_file = st.selectbox("Selecione o arquivo:", file_options)
        else:
            st.warning("Nenhum arquivo encontrado em data/")
    
    st.markdown("---")
    
    # Filtros
    st.header("🔍 Filtros")
    apply_filters = st.checkbox("Aplicar filtros", value=False)

# Carregar dados
try:
    if data_source == "Upload de Arquivo" and uploaded_file is not None:
        # Salvar temporariamente
        temp_path = f"data/temp_{uploaded_file.name}"
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        data, processor = load_and_process_data(file_path=temp_path, use_sample=False)
        os.remove(temp_path)
        
    elif data_source == "Arquivo Existente" and existing_file:
        data, processor = load_and_process_data(file_path=existing_file, use_sample=False)
        
    else:  # Dados simulados
        data, processor = load_and_process_data(use_sample=True, n_samples=n_samples)
    
    # Aplicar filtros se necessário
    filtered_data = data.copy()
    
    if apply_filters:
        with st.sidebar:
            if 'categoria' in data.columns:
                categorias = st.multiselect(
                    "Categorias:",
                    options=data['categoria'].unique(),
                    default=data['categoria'].unique()
                )
                filtered_data = filtered_data[filtered_data['categoria'].isin(categorias)]
            
            if 'canal_venda' in data.columns:
                canais = st.multiselect(
                    "Canais:",
                    options=data['canal_venda'].unique(),
                    default=data['canal_venda'].unique()
                )
                filtered_data = filtered_data[filtered_data['canal_venda'].isin(canais)]
            
            if 'data_pedido' in data.columns:
                date_range = st.date_input(
                    "Período:",
                    value=(data['data_pedido'].min(), data['data_pedido'].max())
                )
                if len(date_range) == 2:
                    filtered_data = filtered_data[
                        (filtered_data['data_pedido'] >= pd.to_datetime(date_range[0])) &
                        (filtered_data['data_pedido'] <= pd.to_datetime(date_range[1]))
                    ]
    
    # Análise de negócio
    insights, analyzer = analyze_business(filtered_data)
    
    # KPIs Principais
    st.header("📈 Métricas Principais")
    
    metrics = insights.get('metricas_principais', {})
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "💰 Receita Total",
            f"R$ {metrics.get('receita_total', 0):,.0f}",
            delta=None
        )
    
    with col2:
        st.metric(
            "🎫 Ticket Médio",
            f"R$ {metrics.get('ticket_medio', 0):.2f}",
            delta=None
        )
    
    with col3:
        st.metric(
            "📦 Total Pedidos",
            f"{metrics.get('num_pedidos', 0):,}",
            delta=None
        )
    
    with col4:
        st.metric(
            "👥 Clientes Únicos",
            f"{metrics.get('num_clientes', 0):,}",
            delta=None
        )
    
    st.markdown("---")
    
    # Tabs para diferentes análises
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📊 Visão Geral",
        "🏆 Produtos",
        "📂 Categorias",
        "🗺️ Geografia",
        "📱 Canais",
        "👥 Clientes"
    ])
    
    with tab1:
        st.subheader("Evolução da Receita")
        
        # Gráfico de evolução mensal
        if 'data_pedido' in filtered_data.columns:
            vendas_mensais = filtered_data.groupby(
                filtered_data['data_pedido'].dt.to_period('M')
            )['valor_total'].sum().reset_index()
            vendas_mensais['data_pedido'] = vendas_mensais['data_pedido'].astype(str)
            
            fig = px.line(
                vendas_mensais,
                x='data_pedido',
                y='valor_total',
                title='Receita Mensal',
                labels={'valor_total': 'Receita (R$)', 'data_pedido': 'Mês'}
            )
            fig.update_traces(line_color='#2E86AB', line_width=3)
            st.plotly_chart(fig, use_container_width=True)
        
        # Duas colunas para gráficos adicionais
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Distribuição por Categoria")
            if 'categoria' in filtered_data.columns:
                cat_data = filtered_data.groupby('categoria')['valor_total'].sum().reset_index()
                fig = px.pie(
                    cat_data,
                    values='valor_total',
                    names='categoria',
                    title='Receita por Categoria'
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Distribuição por Canal")
            if 'canal_venda' in filtered_data.columns:
                canal_data = filtered_data.groupby('canal_venda')['valor_total'].sum().reset_index()
                fig = px.pie(
                    canal_data,
                    values='valor_total',
                    names='canal_venda',
                    title='Receita por Canal'
                )
                st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("🏆 Análise de Produtos")
        
        produtos_insights = insights.get('produtos', {})
        
        # Top produtos
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Top 10 Produtos por Receita**")
            top_receita = produtos_insights.get('top_10_receita', {})
            if top_receita:
                df_top = pd.DataFrame(list(top_receita.items()), columns=['Produto', 'Receita'])
                df_top = df_top.sort_values('Receita', ascending=False).head(10)
                
                fig = px.bar(
                    df_top,
                    y='Produto',
                    x='Receita',
                    orientation='h',
                    title='Top 10 Produtos'
                )
                fig.update_traces(marker_color='#2E86AB')
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("**Top 10 Produtos por Quantidade**")
            top_qtd = produtos_insights.get('top_10_quantidade', {})
            if top_qtd:
                df_top_qtd = pd.DataFrame(list(top_qtd.items()), columns=['Produto', 'Quantidade'])
                df_top_qtd = df_top_qtd.sort_values('Quantidade', ascending=False).head(10)
                
                fig = px.bar(
                    df_top_qtd,
                    y='Produto',
                    x='Quantidade',
                    orientation='h',
                    title='Top 10 por Volume'
                )
                fig.update_traces(marker_color='#A23B72')
                st.plotly_chart(fig, use_container_width=True)
        
        # Produto destaque
        destaque = produtos_insights.get('produto_destaque', {})
        if destaque:
            st.markdown(f"""
            <div class="insight-box">
                <h4>⭐ Produto Destaque</h4>
                <p><strong>{destaque.get('nome', 'N/A')}</strong></p>
                <p>Receita: R$ {destaque.get('receita', 0):,.2f}</p>
                <p>Participação: {destaque.get('participacao_receita', 0):.1f}% da receita total</p>
            </div>
            """, unsafe_allow_html=True)
    
    with tab3:
        st.subheader("📂 Análise de Categorias")
        
        cat_insights = insights.get('categorias', {})
        resumo_cat = cat_insights.get('resumo_categorias', {})
        
        if resumo_cat:
            df_cat = pd.DataFrame(resumo_cat).T
            df_cat = df_cat.sort_values('receita_total', ascending=False)
            
            # Gráfico de barras
            fig = px.bar(
                df_cat.reset_index(),
                x='index',
                y='receita_total',
                title='Receita por Categoria',
                labels={'index': 'Categoria', 'receita_total': 'Receita (R$)'}
            )
            fig.update_traces(marker_color='#F18F01')
            st.plotly_chart(fig, use_container_width=True)
            
            # Tabela detalhada
            st.markdown("**Detalhamento por Categoria**")
            st.dataframe(
                df_cat[['receita_total', 'ticket_medio', 'num_pedidos', 'participacao_receita']].style.format({
                    'receita_total': 'R$ {:,.2f}',
                    'ticket_medio': 'R$ {:,.2f}',
                    'num_pedidos': '{:,.0f}',
                    'participacao_receita': '{:.1f}%'
                }),
                use_container_width=True
            )
    
    with tab4:
        st.subheader("🗺️ Análise Geográfica")
        
        geo_insights = insights.get('geografia', {})
        performance_estados = geo_insights.get('performance_estados', {})
        
        if performance_estados:
            df_geo = pd.DataFrame(performance_estados).T
            df_geo = df_geo.sort_values('receita_total', ascending=False)
            
            # Mapa de calor
            fig = px.bar(
                df_geo.reset_index().head(10),
                x='index',
                y='receita_total',
                title='Top 10 Estados por Receita',
                labels={'index': 'Estado', 'receita_total': 'Receita (R$)'}
            )
            fig.update_traces(marker_color='#C73E1D')
            st.plotly_chart(fig, use_container_width=True)
            
            # Métricas por estado
            col1, col2 = st.columns(2)
            
            with col1:
                fig = px.bar(
                    df_geo.reset_index().head(10),
                    x='index',
                    y='ticket_medio',
                    title='Ticket Médio por Estado',
                    labels={'index': 'Estado', 'ticket_medio': 'Ticket Médio (R$)'}
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                fig = px.bar(
                    df_geo.reset_index().head(10),
                    x='index',
                    y='clientes_unicos',
                    title='Clientes Únicos por Estado',
                    labels={'index': 'Estado', 'clientes_unicos': 'Clientes'}
                )
                st.plotly_chart(fig, use_container_width=True)
    
    with tab5:
        st.subheader("📱 Análise de Canais")
        
        canais_insights = insights.get('canais', {})
        performance_canais = canais_insights.get('performance_canais', {})
        
        if performance_canais:
            df_canais = pd.DataFrame(performance_canais).T
            
            col1, col2 = st.columns(2)
            
            with col1:
                fig = px.pie(
                    df_canais.reset_index(),
                    values='receita_total',
                    names='index',
                    title='Distribuição de Receita por Canal'
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                fig = px.bar(
                    df_canais.reset_index(),
                    x='index',
                    y='ticket_medio',
                    title='Ticket Médio por Canal',
                    labels={'index': 'Canal', 'ticket_medio': 'Ticket Médio (R$)'}
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Tabela de performance
            st.markdown("**Performance Detalhada por Canal**")
            st.dataframe(
                df_canais[['receita_total', 'ticket_medio', 'num_pedidos', 'participacao_receita']].style.format({
                    'receita_total': 'R$ {:,.2f}',
                    'ticket_medio': 'R$ {:,.2f}',
                    'num_pedidos': '{:,.0f}',
                    'participacao_receita': '{:.1f}%'
                }),
                use_container_width=True
            )
    
    with tab6:
        st.subheader("👥 Análise de Clientes")
        
        clientes_insights = insights.get('clientes', {})
        
        # Métricas de clientes
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Total de Clientes",
                f"{clientes_insights.get('total_clientes', 0):,}"
            )
        
        with col2:
            st.metric(
                "Clientes Ativos (30d)",
                f"{clientes_insights.get('clientes_ativos_30d', 0):,}"
            )
        
        with col3:
            st.metric(
                "Clientes Alto Valor",
                f"{clientes_insights.get('clientes_alto_valor', 0):,}"
            )
        
        # Segmentação RFV
        segmentacao = clientes_insights.get('segmentacao', {})
        if segmentacao:
            df_seg = pd.DataFrame(segmentacao).T
            df_seg = df_seg.sort_values('num_clientes', ascending=False)
            
            col1, col2 = st.columns(2)
            
            with col1:
                fig = px.pie(
                    df_seg.reset_index(),
                    values='num_clientes',
                    names='index',
                    title='Distribuição de Clientes por Segmento'
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                fig = px.bar(
                    df_seg.reset_index(),
                    x='index',
                    y='valor_medio',
                    title='Valor Médio por Segmento',
                    labels={'index': 'Segmento', 'valor_medio': 'Valor Médio (R$)'}
                )
                st.plotly_chart(fig, use_container_width=True)
    
    # Insights Estratégicos
    st.markdown("---")
    st.header("💡 Insights Estratégicos")
    
    estrategicos = insights.get('estrategicos', {})
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎯 Principais Descobertas")
        descobertas = estrategicos.get('principais_descobertas', [])
        for descoberta in descobertas:
            st.markdown(f"- {descoberta}")
        
        st.subheader("🚀 Oportunidades")
        oportunidades = estrategicos.get('oportunidades', [])
        for oportunidade in oportunidades:
            st.markdown(f"- {oportunidade}")
    
    with col2:
        st.subheader("⚠️ Riscos Identificados")
        riscos = estrategicos.get('riscos', [])
        for risco in riscos:
            st.markdown(f"- {risco}")
        
        st.subheader("📋 Recomendações Imediatas")
        recomendacoes = estrategicos.get('recomendacoes_imediatas', [])
        for rec in recomendacoes[:5]:
            st.markdown(f"- {rec}")
    
    # Exportar dados
    st.markdown("---")
    st.header("📥 Exportar Dados")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("💾 Exportar CSV"):
            csv = filtered_data.to_csv(index=False)
            st.download_button(
                "Download CSV",
                csv,
                "dados_processados.csv",
                "text/csv"
            )
    
    with col2:
        if st.button("📊 Exportar Excel"):
            # Criar arquivo Excel em memória
            from io import BytesIO
            buffer = BytesIO()
            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                filtered_data.to_excel(writer, sheet_name='Dados', index=False)
            
            st.download_button(
                "Download Excel",
                buffer.getvalue(),
                "dados_processados.xlsx",
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
    
    with col3:
        if st.button("📄 Exportar Relatório"):
            # Gerar relatório em texto
            report = f"""
RELATÓRIO DE ANÁLISE - {datetime.now().strftime('%d/%m/%Y')}

MÉTRICAS PRINCIPAIS:
- Receita Total: R$ {metrics.get('receita_total', 0):,.2f}
- Ticket Médio: R$ {metrics.get('ticket_medio', 0):.2f}
- Total de Pedidos: {metrics.get('num_pedidos', 0):,}
- Clientes Únicos: {metrics.get('num_clientes', 0):,}

PRINCIPAIS DESCOBERTAS:
{chr(10).join(['- ' + d for d in descobertas])}

RECOMENDAÇÕES:
{chr(10).join(['- ' + r for r in recomendacoes])}
"""
            st.download_button(
                "Download Relatório",
                report,
                "relatorio_analise.txt",
                "text/plain"
            )

except Exception as e:
    st.error(f"❌ Erro ao processar dados: {str(e)}")
    st.info("Verifique se os arquivos necessários estão presentes e tente novamente.")

# Rodapé
st.markdown("---")
st.markdown(
    f"<div style='text-align: center; color: #666;'>Dashboard gerado em {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</div>",
    unsafe_allow_html=True
)