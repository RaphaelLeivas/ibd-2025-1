import streamlit as st
import pandas as pd
import sqlite3
from sqlite3 import Error

# --- Conexão com o Banco de Dados ---
def criar_conexao(db_arquivo):
    """ Cria uma conexão com o banco de dados SQLite especificado pelo db_arquivo """
    conn = None
    try:
        conn = sqlite3.connect(db_arquivo)
        return conn
    except Error as e:
        st.error(f"Erro ao conectar ao banco de dados: {e}")
        return None

# --- Funções de Busca de Dados ---
def obter_esquema(conn):
    """ Obtém o esquema do banco de dados """
    query = "SELECT name FROM sqlite_master WHERE type='table';"
    tabelas = pd.read_sql_query(query, conn)
    esquema = {}
    for nome_tabela in tabelas['name']:
        esquema[nome_tabela] = pd.read_sql_query(f"PRAGMA table_info({nome_tabela});", conn)
    return esquema

def obter_dados_tabela(conn, nome_tabela):
    """ Busca todos os dados de uma tabela específica """
    try:
        return pd.read_sql_query(f"SELECT * FROM {nome_tabela}", conn)
    except Exception as e:
        st.error(f"Erro ao buscar dados da tabela {nome_tabela}: {e}")
        return pd.DataFrame()

def obter_precos_filtrados(conn, regioes, produtos):
    """ Busca preços de combustíveis filtrados por região e produto """
    query = "SELECT * FROM precos_combustiveis WHERE regiao IN ({}) AND produto IN ({})".format(
        ','.join('?' for _ in regioes),
        ','.join('?' for _ in produtos)
    )
    params = regioes + produtos
    try:
        df = pd.read_sql_query(query, conn, params=params)
        df['data_coleta'] = pd.to_datetime(df['data_coleta'])
        return df
    except Exception as e:
        st.error(f"Erro ao buscar dados filtrados: {e}. Verifique se a tabela 'precos_combustiveis' e as colunas 'regiao', 'produto' e 'data_coleta' existem.")
        return pd.DataFrame()

def main():
    st.set_page_config(page_title="Explorador de Dados de Combustíveis", layout="wide")

    st.title("⛽ Explorador de Dados de Combustíveis")
    st.write("Uma aplicação interativa para explorar e visualizar a base de dados disponibilizada pela ANP.")

    db_arquivo = "gas_data.db"
    conn = criar_conexao(db_arquivo)

    if conn is not None:
        st.sidebar.title("Navegação")
        modo_app = st.sidebar.selectbox("Escolha uma seção",
                                        ["Explorador de Dados", "Análise de Preços"])

        if modo_app == "Explorador de Dados":
            st.header("Esquema do Banco de Dados e Visualizador de Tabelas")

            with st.expander("Ver Esquema do Banco de Dados"):
                esquema = obter_esquema(conn)
                for nome_tabela, info_tabela in esquema.items():
                    st.subheader(f"Tabela: `{nome_tabela}`")
                    st.dataframe(info_tabela)

            tabelas = [name for name, _ in obter_esquema(conn).items()]
            if tabelas:
                tabela_selecionada = st.selectbox("Selecione uma tabela para ver seus dados", tabelas)
                if tabela_selecionada:
                    dados = obter_dados_tabela(conn, tabela_selecionada)
                    st.subheader(f"Dados da tabela `{tabela_selecionada}`")
                    st.dataframe(dados)
            else:
                st.warning("Nenhuma tabela encontrada no banco de dados.")

        elif modo_app == "Análise de Preços":
            st.header("Análise Interativa de Preços de Combustíveis")

            try:
                todos_os_dados = obter_dados_tabela(conn, 'precos_combustiveis')
                if not todos_os_dados.empty:
                    todos_os_dados['data_coleta'] = pd.to_datetime(todos_os_dados['data_coleta'])
                    regioes = sorted(todos_os_dados['regiao'].unique())
                    produtos = sorted(todos_os_dados['produto'].unique())

                    st.sidebar.header("Filtros")
                    regioes_selecionadas = st.sidebar.multiselect("Selecione as Regiões", regioes, default=regioes[0] if regioes else [])
                    produtos_selecionados = st.sidebar.multiselect("Selecione os Produtos", produtos, default=produtos[0] if produtos else [])

                    if not regioes_selecionadas or not produtos_selecionados:
                        st.warning("Por favor, selecione pelo menos uma região e um produto.")
                    else:
                        dados_filtrados = obter_precos_filtrados(conn, regioes_selecionadas, produtos_selecionados)

                        st.subheader("Dados Filtrados")
                        st.dataframe(dados_filtrados)

                        st.subheader("Tendências de Preços (Valor de Venda)")
                        if not dados_filtrados.empty:
                            # Assumindo que a coluna de preço se chama 'valor_venda'
                            st.line_chart(dados_filtrados, x='data_coleta', y='valor_venda', color='produto')
                        else:
                            st.info("Não há dados para exibir para os filtros selecionados.")
                else:
                    st.error("A tabela 'precos_combustiveis' está vazia ou não existe.")
            except Exception as e:
                st.error(f"Ocorreu um erro durante a análise: {e}")

        conn.close()
    else:
        st.error("Não foi possível conectar ao banco de dados. Por favor, garanta que o arquivo 'gas_data.db' existe no mesmo diretório.")

if __name__ == "__main__":
    main()
