import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class DataProcessor:
    """Classe principal para processamento de dados de vendas"""
    
    def __init__(self):
        self.data = None
        self.processed_data = None
        
    def load_data(self, file_path=None, data=None):
        """
        Carrega dados de arquivo Excel/CSV ou aceita DataFrame
        
        Parameters:
        -----------
        file_path : str, optional
            Caminho para o arquivo de dados
        data : pd.DataFrame, optional
            DataFrame com dados já carregados
        """
        if file_path:
            if file_path.endswith('.xlsx') or file_path.endswith('.xls'):
                self.data = pd.read_excel(file_path)
            elif file_path.endswith('.csv'):
                self.data = pd.read_csv(file_path)
            else:
                raise ValueError("Formato de arquivo não suportado. Use .xlsx, .xls ou .csv")
        elif data is not None:
            self.data = data.copy()
        else:
            raise ValueError("É necessário fornecer file_path ou data")
            
        print(f"✅ Dados carregados: {len(self.data)} registros")
        return self.data
    
    def data_quality_check(self):
        """
        Verifica qualidade dos dados
        
        Returns:
        --------
        dict: Relatório de qualidade dos dados
        """
        if self.data is None:
            raise ValueError("Dados não carregados. Use load_data() primeiro.")
            
        quality_report = {
            'shape': self.data.shape,
            'null_values': self.data.isnull().sum().to_dict(),
            'data_types': self.data.dtypes.to_dict(),
            'duplicates': self.data.duplicated().sum(),
            'memory_usage': self.data.memory_usage(deep=True).sum() / 1024**2  # MB
        }
        
        print("📊 RELATÓRIO DE QUALIDADE DOS DADOS")
        print("-" * 40)
        print(f"Dimensões: {quality_report['shape']}")
        print(f"Duplicatas: {quality_report['duplicates']}")
        print(f"Uso de memória: {quality_report['memory_usage']:.2f} MB")
        print(f"Valores nulos por coluna:")
        for col, nulls in quality_report['null_values'].items():
            if nulls > 0:
                print(f"  - {col}: {nulls} ({nulls/len(self.data)*100:.1f}%)")
        
        return quality_report
    
    def clean_data(self, remove_outliers=True, outlier_threshold=0.99):
        """
        Limpa e prepara os dados para análise
        
        Parameters:
        -----------
        remove_outliers : bool, default True
            Se deve remover outliers
        outlier_threshold : float, default 0.99
            Percentil para definir outliers
        """
        if self.data is None:
            raise ValueError("Dados não carregados. Use load_data() primeiro.")
            
        df = self.data.copy()
        initial_shape = df.shape[0]
        
        print("🧹 INICIANDO LIMPEZA DOS DADOS")
        print("-" * 40)
        
        # 1. Converter colunas de data
        date_columns = ['data_pedido', 'data_compra', 'date', 'data']
        for col in df.columns:
            if any(date_col in col.lower() for date_col in date_columns):
                df[col] = pd.to_datetime(df[col], errors='coerce')
                print(f"✅ Convertida coluna de data: {col}")
        
        # 2. Remover linhas com valores nulos críticos
        critical_columns = ['valor_total', 'preco_unitario', 'quantidade']
        for col in critical_columns:
            if col in df.columns:
                before = len(df)
                df = df.dropna(subset=[col])
                removed = before - len(df)
                if removed > 0:
                    print(f"🗑️ Removidas {removed} linhas com {col} nulo")
        
        # 3. Remover duplicatas
        before_dup = len(df)
        df = df.drop_duplicates()
        removed_dup = before_dup - len(df)
        if removed_dup > 0:
            print(f"🗑️ Removidas {removed_dup} duplicatas")
        
        # 4. Validar valores negativos
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        for col in numeric_columns:
            if col in ['valor_total', 'preco_unitario', 'quantidade']:
                before = len(df)
                df = df[df[col] > 0]
                removed = before - len(df)
                if removed > 0:
                    print(f"🗑️ Removidas {removed} linhas com {col} negativo/zero")
        
        # 5. Remover outliers (se solicitado)
        if remove_outliers and 'valor_total' in df.columns:
            threshold = df['valor_total'].quantile(outlier_threshold)
            before = len(df)
            df = df[df['valor_total'] <= threshold]
            removed = before - len(df)
            if removed > 0:
                print(f"🗑️ Removidos {removed} outliers (acima do percentil {outlier_threshold*100}%)")
        
        # 6. Criar colunas derivadas
        self._create_derived_columns(df)
        
        self.processed_data = df
        final_shape = df.shape[0]
        
        print(f"\n✅ LIMPEZA CONCLUÍDA")
        print(f"Registros iniciais: {initial_shape:,}")
        print(f"Registros finais: {final_shape:,}")
        print(f"Taxa de retenção: {final_shape/initial_shape*100:.1f}%")
        
        return self.processed_data
    
    def _create_derived_columns(self, df):
        """Cria colunas derivadas para análise"""
        
        # Colunas temporais
        date_col = None
        for col in df.columns:
            if 'data' in col.lower() and df[col].dtype == 'datetime64[ns]':
                date_col = col
                break
        
        if date_col:
            df['ano'] = df[date_col].dt.year
            df['mes'] = df[date_col].dt.month
            df['mes_nome'] = df[date_col].dt.strftime('%B')
            df['dia_semana'] = df[date_col].dt.day_name()
            df['trimestre'] = df[date_col].dt.quarter
            df['semana_ano'] = df[date_col].dt.isocalendar().week
            print("✅ Criadas colunas temporais")
        
        # Validar se valor_total = quantidade * preco_unitario
        required_cols = ['valor_total', 'quantidade', 'preco_unitario']
        if all(col in df.columns for col in required_cols):
            df['valor_calculado'] = df['quantidade'] * df['preco_unitario']
            df['diferenca_valor'] = abs(df['valor_total'] - df['valor_calculado'])
            
            # Corrigir pequenas diferenças de arredondamento
            tolerance = 0.01
            inconsistent = df['diferenca_valor'] > tolerance
            if inconsistent.sum() > 0:
                print(f"⚠️ Encontradas {inconsistent.sum()} inconsistências de valor")
                # Usar o valor calculado como padrão
                df.loc[inconsistent, 'valor_total'] = df.loc[inconsistent, 'valor_calculado']
                print("✅ Valores corrigidos")
        
        return df
    
    def get_basic_stats(self):
        """
        Retorna estatísticas básicas dos dados processados
        
        Returns:
        --------
        dict: Estatísticas básicas
        """
        if self.processed_data is None:
            raise ValueError("Dados não processados. Use clean_data() primeiro.")
            
        df = self.processed_data
        
        stats = {
            'total_records': len(df),
            'date_range': {
                'start': df['data_pedido'].min() if 'data_pedido' in df.columns else None,
                'end': df['data_pedido'].max() if 'data_pedido' in df.columns else None
            },
            'unique_counts': {
                'produtos': df['produto'].nunique() if 'produto' in df.columns else None,
                'categorias': df['categoria'].nunique() if 'categoria' in df.columns else None,
                'clientes': df['cliente_id'].nunique() if 'cliente_id' in df.columns else None
            },
            'financial_summary': {
                'receita_total': df['valor_total'].sum() if 'valor_total' in df.columns else None,
                'ticket_medio': df['valor_total'].mean() if 'valor_total' in df.columns else None,
                'ticket_mediano': df['valor_total'].median() if 'valor_total' in df.columns else None
            }
        }
        
        return stats
    
    def export_processed_data(self, file_path):
        """
        Exporta dados processados para arquivo
        
        Parameters:
        -----------
        file_path : str
            Caminho para salvar o arquivo
        """
        if self.processed_data is None:
            raise ValueError("Dados não processados. Use clean_data() primeiro.")
            
        if file_path.endswith('.xlsx'):
            self.processed_data.to_excel(file_path, index=False)
        elif file_path.endswith('.csv'):
            self.processed_data.to_csv(file_path, index=False)
        else:
            raise ValueError("Formato não suportado. Use .xlsx ou .csv")
        
        print(f"✅ Dados exportados para: {file_path}")

def generate_sample_data(n_records=5000):
    """
    Gera dados de exemplo para demonstração
    
    Parameters:
    -----------
    n_records : int, default 5000
        Número de registros a gerar
    
    Returns:
    --------
    pd.DataFrame: Dados de exemplo
    """
    np.random.seed(42)
    
    # Produtos e categorias
    produtos_info = [
        ('Smartphone Samsung Galaxy', 'Smartphones', 1200),
        ('iPhone 14', 'Smartphones', 4500),
        ('Notebook Dell Inspiron', 'Notebooks', 2800),
        ('Tablet iPad', 'Tablets', 2200),
        ('Fones JBL Bluetooth', 'Áudio', 300),
        ('Smartwatch Apple', 'Wearables', 2000),
        ('Camera Canon EOS', 'Fotografia', 3500),
        ('TV 55" LG OLED', 'TVs', 2500),
        ('Notebook Lenovo ThinkPad', 'Notebooks', 3200),
        ('Mouse Gamer Logitech', 'Periféricos', 150),
        ('Teclado Mecânico Corsair', 'Periféricos', 400),
        ('Monitor 24" Samsung', 'Monitores', 800),
        ('Carregador Wireless', 'Acessórios', 200),
        ('Caixa de Som JBL', 'Áudio', 500),
        ('HD Externo 1TB', 'Armazenamento', 300),
        ('Pendrive 64GB', 'Armazenamento', 80)
    ]
    
    # Gerando dados
    dados = []
    for i in range(n_records):
        # Data aleatória nos últimos 12 meses
        data_pedido = datetime.now() - timedelta(days=np.random.randint(0, 365))
        
        # Produto aleatório
        produto, categoria, preco_base = produtos_info[np.random.randint(0, len(produtos_info))]
        
        # Variação de preço
        preco_unitario = round(preco_base * np.random.uniform(0.8, 1.2), 2)
        
        # Quantidade
        quantidade = np.random.choice([1, 2, 3, 4, 5], p=[0.6, 0.2, 0.1, 0.06, 0.04])
        
        # Outros campos
        cliente_id = np.random.randint(1000, 9999)
        estado = np.random.choice(['SP', 'RJ', 'MG', 'RS', 'PR', 'SC', 'BA', 'GO'], 
                                 p=[0.35, 0.15, 0.12, 0.08, 0.08, 0.05, 0.07, 0.10])
        canal = np.random.choice(['Online', 'Marketplace', 'App Mobile'], p=[0.5, 0.35, 0.15])
        
        dados.append({
            'pedido_id': f'PED{i+1000:04d}',
            'data_pedido': data_pedido,
            'cliente_id': cliente_id,
            'produto': produto,
            'categoria': categoria,
            'quantidade': quantidade,
            'preco_unitario': preco_unitario,
            'valor_total': round(quantidade * preco_unitario, 2),
            'estado': estado,
            'canal_venda': canal
        })
    
    return pd.DataFrame(dados)

# Exemplo de uso
if __name__ == "__main__":
    # Criar instância do processador
    processor = DataProcessor()
    
    # Gerar dados de exemplo
    sample_data = generate_sample_data(1000)
    print("Dados de exemplo gerados!")
    
    # Carregar e processar
    processor.load_data(data=sample_data)
    processor.data_quality_check()
    processed_data = processor.clean_data()
    
    # Estatísticas básicas
    stats = processor.get_basic_stats()
    print("\n📊 ESTATÍSTICAS BÁSICAS:")
    print(f"Total de registros: {stats['total_records']:,}")
    print(f"Receita total: R$ {stats['financial_summary']['receita_total']:,.2f}")
    print(f"Ticket médio: R$ {stats['financial_summary']['ticket_medio']:.2f}")
