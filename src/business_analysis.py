import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class BusinessAnalyzer:
    """Classe para análise estratégica de dados de e-commerce"""
    
    def __init__(self, data):
        """
        Inicializa o analisador de negócios
        
        Parameters:
        -----------
        data : pd.DataFrame
            DataFrame com dados de vendas processados
        """
        self.data = data
        self.insights = {}
        
    def calculate_key_metrics(self):
        """
        Calcula métricas principais do negócio
        
        Returns:
        --------
        dict: Dicionário com métricas principais
        """
        metrics = {
            'receita_total': self.data['valor_total'].sum(),
            'ticket_medio': self.data['valor_total'].mean(),
            'ticket_mediano': self.data['valor_total'].median(),
            'num_pedidos': len(self.data),
            'num_produtos': self.data['produto'].nunique(),
            'num_categorias': self.data['categoria'].nunique(),
            'num_clientes': self.data['cliente_id'].nunique(),
            'qtd_total_vendida': self.data['quantidade'].sum(),
            'data_inicio': self.data['data_pedido'].min(),
            'data_fim': self.data['data_pedido'].max(),
            'periodo_dias': (self.data['data_pedido'].max() - self.data['data_pedido'].min()).days,
            'receita_diaria_media': self.data['valor_total'].sum() / (self.data['data_pedido'].max() - self.data['data_pedido'].min()).days,
            'pedidos_por_cliente': len(self.data) / self.data['cliente_id'].nunique()
        }
        
        self.insights['metricas_principais'] = metrics
        return metrics
    
    def analyze_products_performance(self):
        """
        Análise detalhada de performance de produtos
        
        Returns:
        --------
        dict: Análise de produtos
        """
        # Top produtos por diferentes métricas
        top_produtos_receita = self.data.groupby('produto')['valor_total'].sum().sort_values(ascending=False)
        top_produtos_quantidade = self.data.groupby('produto')['quantidade'].sum().sort_values(ascending=False)
        top_produtos_pedidos = self.data.groupby('produto').size().sort_values(ascending=False)
        
        # Análise de ticket médio por produto
        ticket_medio_produto = self.data.groupby('produto')['valor_total'].mean().sort_values(ascending=False)
        
        # Produtos com maior margem (assumindo que produtos mais caros têm maior margem)
        produtos_premium = ticket_medio_produto.head(10)
        
        # Análise de concentração (Pareto)
        receita_acumulada = top_produtos_receita.cumsum()
        receita_percentual = (receita_acumulada / receita_acumulada.iloc[-1]) * 100
        produtos_80_percent = receita_percentual[receita_percentual <= 80].index.tolist()
        
        analysis = {
            'top_10_receita': top_produtos_receita.head(10).to_dict(),
            'top_10_quantidade': top_produtos_quantidade.head(10).to_dict(),
            'top_10_pedidos': top_produtos_pedidos.head(10).to_dict(),
            'produtos_premium': produtos_premium.to_dict(),
            'concentracao_80_20': {
                'num_produtos_80_percent': len(produtos_80_percent),
                'percentual_produtos': len(produtos_80_percent) / self.data['produto'].nunique() * 100,
                'produtos': produtos_80_percent
            },
            'produto_destaque': {
                'nome': top_produtos_receita.index[0],
                'receita': top_produtos_receita.iloc[0],
                'participacao_receita': top_produtos_receita.iloc[0] / self.data['valor_total'].sum() * 100
            }
        }
        
        self.insights['produtos'] = analysis
        return analysis
    
    def analyze_categories_performance(self):
        """
        Análise de performance por categoria
        
        Returns:
        --------
        dict: Análise de categorias
        """
        cat_analysis = self.data.groupby('categoria').agg({
            'valor_total': ['sum', 'mean', 'median', 'count'],
            'quantidade': 'sum',
            'cliente_id': 'nunique'
        }).round(2)
        
        # Flatten column names
        cat_analysis.columns = [f"{col[1]}_{col[0]}" if col[1] else col[0] for col in cat_analysis.columns]
        cat_analysis.columns = ['receita_total', 'ticket_medio', 'ticket_mediano', 'num_pedidos', 'qtd_vendida', 'clientes_unicos']
        
        # Calcular participação de mercado
        cat_analysis['participacao_receita'] = (cat_analysis['receita_total'] / cat_analysis['receita_total'].sum() * 100).round(1)
        cat_analysis['receita_por_cliente'] = (cat_analysis['receita_total'] / cat_analysis['clientes_unicos']).round(2)
        
        # Rankear categorias
        cat_analysis = cat_analysis.sort_values('receita_total', ascending=False)
        
        analysis = {
            'resumo_categorias': cat_analysis.to_dict('index'),
            'categoria_lider': {
                'nome': cat_analysis.index[0],
                'receita': cat_analysis.iloc[0]['receita_total'],
                'participacao': cat_analysis.iloc[0]['participacao_receita']
            },
            'categoria_maior_ticket': {
                'nome': cat_analysis.sort_values('ticket_medio', ascending=False).index[0],
                'ticket_medio': cat_analysis.sort_values('ticket_medio', ascending=False).iloc[0]['ticket_medio']
            },
            'categoria_mais_popular': {
                'nome': cat_analysis.sort_values('num_pedidos', ascending=False).index[0],
                'num_pedidos': cat_analysis.sort_values('num_pedidos', ascending=False).iloc[0]['num_pedidos']
            }
        }
        
        self.insights['categorias'] = analysis
        return analysis
    
    def analyze_customer_behavior(self):
        """
        Análise de comportamento de clientes (RFV)
        
        Returns:
        --------
        dict: Análise de clientes
        """
        # Data de referência para cálculo de recência
        data_referencia = self.data['data_pedido'].max()
        
        # Análise RFV por cliente
        rfv_analysis = self.data.groupby('cliente_id').agg({
            'data_pedido': lambda x: (data_referencia - x.max()).days,  # Recência
            'pedido_id': 'count',  # Frequência  
            'valor_total': 'sum'   # Valor
        })
        rfv_analysis.columns = ['recencia', 'frequencia', 'valor_total']
        
        # Scores RFV (1-5, onde 5 é melhor)
        rfv_analysis['score_recencia'] = pd.qcut(rfv_analysis['recencia'], 5, labels=[5,4,3,2,1])
        rfv_analysis['score_frequencia'] = pd.qcut(rfv_analysis['frequencia'].rank(method='first'), 5, labels=[1,2,3,4,5])
        rfv_analysis['score_valor'] = pd.qcut(rfv_analysis['valor_total'].rank(method='first'), 5, labels=[1,2,3,4,5])
        
        # Score RFV combinado
        rfv_analysis['score_rfv'] = (rfv_analysis['score_recencia'].astype(int) + 
                                    rfv_analysis['score_frequencia'].astype(int) + 
                                    rfv_analysis['score_valor'].astype(int))
        
        # Segmentação de clientes
        def segmentar_cliente(score):
            if score >= 13:
                return 'Champions'
            elif score >= 11:
                return 'Loyal Customers'
            elif score >= 9:
                return 'Potential Loyalists'
            elif score >= 7:
                return 'At Risk'
            elif score >= 5:
                return 'Cannot Lose Them'
            else:
                return 'Hibernating'
        
        rfv_analysis['segmento'] = rfv_analysis['score_rfv'].apply(segmentar_cliente)
        
        # Estatísticas por segmento
        segmento_stats = rfv_analysis.groupby('segmento').agg({
            'recencia': 'mean',
            'frequencia': 'mean', 
            'valor_total': 'mean',
            'score_rfv': 'count'
        }).round(2)
        segmento_stats.columns = ['recencia_media', 'frequencia_media', 'valor_medio', 'num_clientes']
        segmento_stats['percentual'] = (segmento_stats['num_clientes'] / len(rfv_analysis) * 100).round(1)
        
        analysis = {
            'total_clientes': len(rfv_analysis),
            'clientes_ativos_30d': len(rfv_analysis[rfv_analysis['recencia'] <= 30]),
            'clientes_frequentes': len(rfv_analysis[rfv_analysis['frequencia'] >= 3]),
            'clientes_alto_valor': len(rfv_analysis[rfv_analysis['valor_total'] >= rfv_analysis['valor_total'].quantile(0.8)]),
            'segmentacao': segmento_stats.to_dict('index'),
            'top_10_clientes': rfv_analysis.sort_values('valor_total', ascending=False).head(10)[['frequencia', 'valor_total', 'recencia']].to_dict('index'),
            'rfv_medias': {
                'recencia_media': rfv_analysis['recencia'].mean(),
                'frequencia_media': rfv_analysis['frequencia'].mean(),
                'valor_medio_cliente': rfv_analysis['valor_total'].mean()
            }
        }
        
        self.insights['clientes'] = analysis
        return analysis
    
    def analyze_geographic_performance(self):
        """
        Análise de performance geográfica
        
        Returns:
        --------
        dict: Análise geográfica
        """
        geo_analysis = self.data.groupby('estado').agg({
            'valor_total': ['sum', 'mean', 'count'],
            'cliente_id': 'nunique',
            'quantidade': 'sum'
        })
        
        # Flatten columns
        geo_analysis.columns = ['receita_total', 'ticket_medio', 'num_pedidos', 'clientes_unicos', 'qtd_vendida']
        
        # Métricas adicionais
        geo_analysis['receita_por_cliente'] = (geo_analysis['receita_total'] / geo_analysis['clientes_unicos']).round(2)
        geo_analysis['pedidos_por_cliente'] = (geo_analysis['num_pedidos'] / geo_analysis['clientes_unicos']).round(2)
        geo_analysis['participacao_receita'] = (geo_analysis['receita_total'] / geo_analysis['receita_total'].sum() * 100).round(1)
        
        geo_analysis = geo_analysis.sort_values('receita_total', ascending=False)
        
        analysis = {
            'performance_estados': geo_analysis.to_dict('index'),
            'estado_lider': {
                'nome': geo_analysis.index[0],
                'receita': geo_analysis.iloc[0]['receita_total'],
                'participacao': geo_analysis.iloc[0]['participacao_receita']
            },
            'estado_maior_ticket': {
                'nome': geo_analysis.sort_values('ticket_medio', ascending=False).index[0],
                'ticket_medio': geo_analysis.sort_values('ticket_medio', ascending=False).iloc[0]['ticket_medio']
            },
            'concentracao_geografica': {
                'top_3_estados_receita': geo_analysis.head(3)['participacao_receita'].sum(),
                'estados_representam_80_receita': len(geo_analysis[geo_analysis['receita_total'].cumsum() / geo_analysis['receita_total'].sum() <= 0.8])
            }
        }
        
        self.insights['geografia'] = analysis
        return analysis
    
    def analyze_channel_performance(self):
        """
        Análise de performance por canal de venda
        
        Returns:
        --------
        dict: Análise de canais
        """
        channel_analysis = self.data.groupby('canal_venda').agg({
            'valor_total': ['sum', 'mean', 'count'],
            'cliente_id': 'nunique',
            'quantidade': 'sum'
        })
        
        # Flatten columns
        channel_analysis.columns = ['receita_total', 'ticket_medio', 'num_pedidos', 'clientes_unicos', 'qtd_vendida']
        
        # Métricas adicionais
        channel_analysis['participacao_receita'] = (channel_analysis['receita_total'] / channel_analysis['receita_total'].sum() * 100).round(1)
        channel_analysis['receita_por_cliente'] = (channel_analysis['receita_total'] / channel_analysis['clientes_unicos']).round(2)
        channel_analysis['conversao_relativa'] = (channel_analysis['num_pedidos'] / channel_analysis['clientes_unicos']).round(2)
        
        channel_analysis = channel_analysis.sort_values('receita_total', ascending=False)
        
        # Análise de crescimento por canal (se temos dados temporais suficientes)
        crescimento_canais = {}
        try:
            # Últimos 2 períodos para comparação
            data_corte = self.data['data_pedido'].max() - timedelta(days=30)
            periodo_atual = self.data[self.data['data_pedido'] > data_corte]
            periodo_anterior = self.data[self.data['data_pedido'] <= data_corte]
            
            for canal in self.data['canal_venda'].unique():
                receita_atual = periodo_atual[periodo_atual['canal_venda'] == canal]['valor_total'].sum()
                receita_anterior = periodo_anterior[periodo_anterior['canal_venda'] == canal]['valor_total'].sum()
                
                if receita_anterior > 0:
                    crescimento = ((receita_atual - receita_anterior) / receita_anterior * 100)
                    crescimento_canais[canal] = crescimento
        except:
            crescimento_canais = {}
        
        analysis = {
            'performance_canais': channel_analysis.to_dict('index'),
            'canal_lider': {
                'nome': channel_analysis.index[0],
                'receita': channel_analysis.iloc[0]['receita_total'],
                'participacao': channel_analysis.iloc[0]['participacao_receita']
            },
            'canal_maior_ticket': {
                'nome': channel_analysis.sort_values('ticket_medio', ascending=False).index[0],
                'ticket_medio': channel_analysis.sort_values('ticket_medio', ascending=False).iloc[0]['ticket_medio']
            },
            'crescimento_canais': crescimento_canais,
            'diversificacao': {
                'num_canais': len(channel_analysis),
                'concentracao_canal_principal': channel_analysis.iloc[0]['participacao_receita']
            }
        }
        
        self.insights['canais'] = analysis
        return analysis
    
    def analyze_seasonal_patterns(self):
        """
        Análise de padrões sazonais
        
        Returns:
        --------
        dict: Análise sazonal
        """
        # Análise por trimestre
        trimestre_analysis = self.data.groupby(self.data['data_pedido'].dt.quarter).agg({
            'valor_total': ['sum', 'mean', 'count'],
            'quantidade': 'sum'
        })
        trimestre_analysis.columns = ['receita_total', 'ticket_medio', 'num_pedidos', 'qtd_vendida']
        
        # Análise por mês
        mes_analysis = self.data.groupby(self.data['data_pedido'].dt.month).agg({
            'valor_total': ['sum', 'mean', 'count'],
            'quantidade': 'sum'
        })
        mes_analysis.columns = ['receita_total', 'ticket_medio', 'num_pedidos', 'qtd_vendida']
        
        # Análise por dia da semana
        dia_analysis = self.data.groupby(self.data['data_pedido'].dt.day_name()).agg({
            'valor_total': ['sum', 'mean', 'count'],
            'quantidade': 'sum'
        })
        dia_analysis.columns = ['receita_total', 'ticket_medio', 'num_pedidos', 'qtd_vendida']
        
        # Identificar padrões
        melhor_trimestre = trimestre_analysis.sort_values('receita_total', ascending=False).index[0]
        melhor_mes = mes_analysis.sort_values('receita_total', ascending=False).index[0]
        melhor_dia = dia_analysis.sort_values('receita_total', ascending=False).index[0]
        
        # Coeficiente de variação para medir sazonalidade
        cv_trimestre = trimestre_analysis['receita_total'].std() / trimestre_analysis['receita_total'].mean()
        cv_mes = mes_analysis['receita_total'].std() / mes_analysis['receita_total'].mean()
        
        analysis = {
            'trimestres': trimestre_analysis.to_dict('index'),
            'meses': mes_analysis.to_dict('index'),
            'dias_semana': dia_analysis.to_dict('index'),
            'padroes_identificados': {
                'melhor_trimestre': melhor_trimestre,
                'melhor_mes': melhor_mes,
                'melhor_dia_semana': melhor_dia,
                'sazonalidade_trimestral': cv_trimestre,
                'sazonalidade_mensal': cv_mes,
                'nivel_sazonalidade': 'Alta' if cv_trimestre > 0.3 else 'Média' if cv_trimestre > 0.15 else 'Baixa'
            },
            'recomendacoes_sazonais': self._generate_seasonal_recommendations(melhor_trimestre, melhor_mes, melhor_dia, cv_trimestre)
        }
        
        self.insights['sazonalidade'] = analysis
        return analysis
    
    def _generate_seasonal_recommendations(self, melhor_trimestre, melhor_mes, melhor_dia, cv_trimestre):
        """Gera recomendações baseadas nos padrões sazonais"""
        recomendacoes = []
        
        if cv_trimestre > 0.3:  # Alta sazonalidade
            recomendacoes.append(f"Alta sazonalidade detectada. Concentrar esforços de marketing no Q{melhor_trimestre}")
            recomendacoes.append("Considerar ajustes de estoque baseados nos padrões sazonais")
        
        meses_nome = {1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril', 5: 'Maio', 6: 'Junho',
                     7: 'Julho', 8: 'Agosto', 9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'}
        
        recomendacoes.append(f"Melhor performance em {meses_nome.get(melhor_mes, melhor_mes)} - intensificar campanhas neste período")
        recomendacoes.append(f"Vendas mais fortes em {melhor_dia} - otimizar campanhas para este dia")
        
        return recomendacoes
    
    def analyze_pricing_opportunities(self):
        """
        Análise de oportunidades de precificação
        
        Returns:
        --------
        dict: Análise de pricing
        """
        # Análise de elasticidade por categoria (proxy através de dispersão de preços)
        pricing_analysis = self.data.groupby('categoria').agg({
            'preco_unitario': ['mean', 'median', 'std', 'min', 'max'],
            'quantidade': 'sum',
            'valor_total': 'sum'
        })
        
        # Flatten columns
        pricing_analysis.columns = ['preco_medio', 'preco_mediano', 'desvio_preco', 'preco_min', 'preco_max', 'qtd_vendida', 'receita_total']
        
        # Coeficiente de variação de preços
        pricing_analysis['cv_preco'] = pricing_analysis['desvio_preco'] / pricing_analysis['preco_medio']
        
        # Margem potencial (diferença entre max e min)
        pricing_analysis['margem_potencial'] = ((pricing_analysis['preco_max'] - pricing_analysis['preco_min']) / pricing_analysis['preco_min'] * 100).round(1)
        
        # Análise por produto individual
        produto_pricing = self.data.groupby('produto').agg({
            'preco_unitario': ['mean', 'std', 'count'],
            'quantidade': 'sum'
        })
        produto_pricing.columns = ['preco_medio', 'desvio_preco', 'num_transacoes', 'qtd_vendida']
        produto_pricing['cv_preco'] = produto_pricing['desvio_preco'] / produto_pricing['preco_medio']
        
        # Produtos com oportunidade de ajuste de preço
        produtos_oportunidade = produto_pricing[
            (produto_pricing['cv_preco'] > 0.1) & 
            (produto_pricing['num_transacoes'] >= 5)
        ].sort_values('cv_preco', ascending=False)
        
        analysis = {
            'pricing_por_categoria': pricing_analysis.to_dict('index'),
            'categoria_maior_variacao': {
                'nome': pricing_analysis.sort_values('cv_preco', ascending=False).index[0],
                'cv_preco': pricing_analysis.sort_values('cv_preco', ascending=False).iloc[0]['cv_preco']
            },
            'categoria_maior_margem_potencial': {
                'nome': pricing_analysis.sort_values('margem_potencial', ascending=False).index[0],
                'margem_potencial': pricing_analysis.sort_values('margem_potencial', ascending=False).iloc[0]['margem_potencial']
            },
            'produtos_oportunidade_pricing': produtos_oportunidade.head(10).to_dict('index'),
            'recomendacoes_pricing': self._generate_pricing_recommendations(pricing_analysis, produtos_oportunidade)
        }
        
        self.insights['pricing'] = analysis
        return analysis
    
    def _generate_pricing_recommendations(self, pricing_analysis, produtos_oportunidade):
        """Gera recomendações de precificação"""
        recomendacoes = []
        
        # Categoria com maior variação
        cat_maior_var = pricing_analysis.sort_values('cv_preco', ascending=False).index[0]
        recomendacoes.append(f"Revisar estratégia de pricing para categoria {cat_maior_var} (alta variação de preços)")
        
        # Categoria com maior potencial
        cat_maior_pot = pricing_analysis.sort_values('margem_potencial', ascending=False).index[0]
        recomendacoes.append(f"Explorar aumento de preços na categoria {cat_maior_pot} (maior margem potencial)")
        
        if len(produtos_oportunidade) > 0:
            recomendacoes.append(f"Padronizar preços de {len(produtos_oportunidade)} produtos com alta variação")
            recomendacoes.append("Implementar testes A/B para otimização de preços")
        
        return recomendacoes
    
    def generate_comprehensive_insights(self):
        """
        Gera análise completa com insights estratégicos
        
        Returns:
        --------
        dict: Todos os insights consolidados
        """
        print("🔍 Iniciando análise abrangente do negócio...")
        
        # Executar todas as análises
        self.calculate_key_metrics()
        self.analyze_products_performance()
        self.analyze_categories_performance()
        self.analyze_customer_behavior()
        self.analyze_geographic_performance()
        self.analyze_channel_performance()
        self.analyze_seasonal_patterns()
        self.analyze_pricing_opportunities()
        
        # Gerar insights estratégicos consolidados
        strategic_insights = self._generate_strategic_insights()
        
        self.insights['estrategicos'] = strategic_insights
        
        print("✅ Análise abrangente concluída!")
        return self.insights
    
    def _generate_strategic_insights(self):
        """Gera insights estratégicos consolidados"""
        
        insights_estrategicos = {
            'principais_descobertas': [],
            'oportunidades': [],
            'riscos': [],
            'recomendacoes_imediatas': [],
            'recomendacoes_medio_prazo': [],
            'kpis_monitoramento': []
        }
        
        # Principais descobertas
        if 'produtos' in self.insights:
            produto_destaque = self.insights['produtos']['produto_destaque']
            insights_estrategicos['principais_descobertas'].append(
                f"Produto '{produto_destaque['nome']}' representa {produto_destaque['participacao_receita']:.1f}% da receita total"
            )
        
        if 'categorias' in self.insights:
            cat_lider = self.insights['categorias']['categoria_lider']
            insights_estrategicos['principais_descobertas'].append(
                f"Categoria '{cat_lider['nome']}' lidera com {cat_lider['participacao']:.1f}% da receita"
            )
        
        if 'canais' in self.insights:
            canal_lider = self.insights['canais']['canal_lider']
            insights_estrategicos['principais_descobertas'].append(
                f"Canal '{canal_lider['nome']}' concentra {canal_lider['participacao']:.1f}% das vendas"
            )
        
        # Oportunidades
        if 'clientes' in self.insights:
            segmentacao = self.insights['clientes']['segmentacao']
            if 'At Risk' in segmentacao:
                at_risk = segmentacao['At Risk']['num_clientes']
                insights_estrategicos['oportunidades'].append(
                    f"Reativar {at_risk} clientes em risco com campanhas direcionadas"
                )
        
        if 'geografia' in self.insights:
            concentracao = self.insights['geografia']['concentracao_geografica']['top_3_estados_receita']
            if concentracao < 70:
                insights_estrategicos['oportunidades'].append(
                    "Baixa concentração geográfica - oportunidade de expansão nacional"
                )
        
        # Riscos
        if 'produtos' in self.insights:
            concentracao_produto = self.insights['produtos']['produto_destaque']['participacao_receita']
            if concentracao_produto > 30:
                insights_estrategicos['riscos'].append(
                    f"Alta dependência de um produto ({concentracao_produto:.1f}%) - risco de concentração"
                )
        
        if 'canais' in self.insights:
            concentracao_canal = self.insights['canais']['diversificacao']['concentracao_canal_principal']
            if concentracao_canal > 70:
                insights_estrategicos['riscos'].append(
                    f"Alta dependência de um canal ({concentracao_canal:.1f}%) - risco operacional"
                )
        
        # Recomendações imediatas
        insights_estrategicos['recomendacoes_imediatas'].extend([
            "Implementar dashboard de monitoramento em tempo real",
            "Configurar alertas para queda de performance em produtos principais",
            "Iniciar programa de fidelização para clientes Champions"
        ])
        
        # Recomendações médio prazo
        insights_estrategicos['recomendacoes_medio_prazo'].extend([
            "Diversificar portfólio de produtos para reduzir concentração",
            "Expandir para novos canais de venda",
            "Implementar análise preditiva para previsão de demanda"
        ])
        
        # KPIs para monitoramento
        insights_estrategicos['kpis_monitoramento'].extend([
            "Receita mensal e crescimento MoM",
            "Ticket médio por canal e categoria",
            "Taxa de retenção de clientes",
            "Concentração de receita (produtos e canais)",
            "Performance geográfica",
            "Sazonalidade e tendências"
        ])
        
        return insights_estrategicos
    
    def export_insights_report(self, file_path='reports/business_insights.txt'):
        """
        Exporta relatório completo de insights
        
        Parameters:
        -----------
        file_path : str
            Caminho para salvar o relatório
        """
        import os
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        if not self.insights:
            self.generate_comprehensive_insights()
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write("="*80 + "\n")
            f.write("RELATÓRIO COMPLETO DE INSIGHTS DE NEGÓCIO - E-COMMERCE\n")
            f.write("="*80 + "\n")
            f.write(f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n\n")
            
            # Métricas principais
            if 'metricas_principais' in self.insights:
                f.write("📊 MÉTRICAS PRINCIPAIS\n")
                f.write("-" * 30 + "\n")
                metrics = self.insights['metricas_principais']
                f.write(f"💰 Receita Total: R$ {metrics['receita_total']:,.2f}\n")
                f.write(f"🎫 Ticket Médio: R$ {metrics['ticket_medio']:.2f}\n")
                f.write(f"📦 Total de Pedidos: {metrics['num_pedidos']:,}\n")
                f.write(f"👥 Clientes Únicos: {metrics['num_clientes']:,}\n")
                f.write(f"🛍️ Produtos Únicos: {metrics['num_produtos']:,}\n")
                f.write(f"📅 Período: {metrics['periodo_dias']} dias\n")
                f.write(f"💵 Receita Diária Média: R$ {metrics['receita_diaria_media']:.2f}\n\n")
            
            # Insights estratégicos
            if 'estrategicos' in self.insights:
                estrategicos = self.insights['estrategicos']
                
                f.write("💡 PRINCIPAIS DESCOBERTAS\n")
                f.write("-" * 30 + "\n")
                for descoberta in estrategicos['principais_descobertas']:
                    f.write(f"• {descoberta}\n")
                f.write("\n")
                
                f.write("🚀 OPORTUNIDADES IDENTIFICADAS\n")
                f.write("-" * 30 + "\n")
                for oportunidade in estrategicos['oportunidades']:
                    f.write(f"• {oportunidade}\n")
                f.write("\n")
                
                f.write("⚠️ RISCOS IDENTIFICADOS\n")
                f.write("-" * 30 + "\n")
                for risco in estrategicos['riscos']:
                    f.write(f"• {risco}\n")
                f.write("\n")
                
                f.write("📋 RECOMENDAÇÕES IMEDIATAS\n")
                f.write("-" * 30 + "\n")
                for rec in estrategicos['recomendacoes_imediatas']:
                    f.write(f"• {rec}\n")
                f.write("\n")
                
                f.write("🎯 RECOMENDAÇÕES MÉDIO PRAZO\n")
                f.write("-" * 30 + "\n")
                for rec in estrategicos['recomendacoes_medio_prazo']:
                    f.write(f"• {rec}\n")
                f.write("\n")
        
        print(f"✅ Relatório de insights exportado para: {file_path}")

# Exemplo de uso
if __name__ == "__main__":
    # Simular dados para teste
    from data_processing import generate_sample_data
    
    # Gerar dados de exemplo
    sample_data = generate_sample_data(3000)
    
    # Criar analisador de negócios
    analyzer = BusinessAnalyzer(sample_data)
    
    # Gerar insights completos
    insights = analyzer.generate_comprehensive_insights()
    
    # Exportar relatório
    analyzer.export_insights_report()
    
    print("✅ Análise de negócio concluída com sucesso!")