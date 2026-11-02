import streamlit as st
import pandas as pd

def formatar_reais(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# Configuração da página
st.set_page_config(
    page_title="Dashboard Inteligente de Vendas",
    page_icon="📊",
    layout="wide"
)

# Cabeçalho do dashboard
st.title("📊 Dashboard de Performance Comercial")

st.markdown(
    """
    Acompanhe os principais indicadores de vendas,
    faturamento e desempenho dos produtos.
    """
)

st.divider()
# Carregar os dados da planilha
dados = pd.read_csv("vendas.csv")
# Filtros do dashboard
st.sidebar.header("Filtros")

regioes = ["Todas"] + sorted(dados["regiao"].unique().tolist())
categorias = ["Todas"] + sorted(dados["categoria"].unique().tolist())

regiao_selecionada = st.sidebar.selectbox("Escolha a região", regioes)
categoria_selecionada = st.sidebar.selectbox("Escolha a categoria", categorias)

# Aplicar filtros
dados_filtrados = dados.copy()

if regiao_selecionada != "Todas":
    dados_filtrados = dados_filtrados[
        dados_filtrados["regiao"] == regiao_selecionada
    ]

if categoria_selecionada != "Todas":
    dados_filtrados = dados_filtrados[
        dados_filtrados["categoria"] == categoria_selecionada
    ]

if dados_filtrados.empty:
    st.warning("Nenhuma venda encontrada para os filtros selecionados.")
    st.stop()

# Organizar os dados filtrados
dados_filtrados["data"] = pd.to_datetime(dados_filtrados["data"])

# Calcular faturamento de cada venda
dados_filtrados["faturamento"] = (
    dados_filtrados["quantidade"] * dados_filtrados["preco_unitario"]
)

# Criar coluna com o mês
dados_filtrados["mes"] = dados_filtrados["data"].dt.strftime("%Y-%m")

# Calcular os indicadores
faturamento = dados_filtrados["faturamento"].sum()
total_vendas = len(dados_filtrados)
produtos_vendidos = dados_filtrados["quantidade"].sum()

# Exibir indicadores
col1, col2, col3 = st.columns(3)

col1.metric("Faturamento", formatar_reais(faturamento))
col2.metric("Total de vendas", total_vendas)
col3.metric("Produtos vendidos", produtos_vendidos)

# Gráfico de faturamento mensal
st.subheader("📈 Faturamento por mês")

faturamento_mensal = dados_filtrados.groupby("mes")["faturamento"].sum()
st.bar_chart(faturamento_mensal)

# Gráfico de vendas por produto
st.subheader("📦 Vendas por produto")

vendas_por_produto = dados_filtrados.groupby("produto")["quantidade"].sum()
st.bar_chart(vendas_por_produto)

# Tabela detalhada de vendas
st.subheader("📋 Detalhamento das vendas")

st.dataframe(
    dados_filtrados[
        ["data", "produto", "categoria", "regiao", "quantidade", "preco_unitario", "faturamento"]
    ],
    use_container_width=True
)

# Gráfico de faturamento por região
st.subheader("🌎 Faturamento por região")

faturamento_regiao = dados_filtrados.groupby("regiao")["faturamento"].sum()

st.bar_chart(faturamento_regiao)

# Analista Inteligente de Vendas
st.divider()
st.header("🤖 Analista Inteligente de Vendas")

# Produto mais vendido
produto_mais_vendido = vendas_por_produto.idxmax()
quantidade_mais_vendida = vendas_por_produto.max()

# Região com maior faturamento
faturamento_regiao = dados_filtrados.groupby("regiao")["faturamento"].sum()
regiao_destaque = faturamento_regiao.idxmax()
maior_faturamento = faturamento_regiao.max()

# Exibir resultados
st.subheader("📌 Principais destaques")

st.write(
    f"O produto mais vendido foi **{produto_mais_vendido}**, "
    f"com **{quantidade_mais_vendida} unidades**."
)

st.write(
    f"A região com maior faturamento foi **{regiao_destaque}**, "
    f"com **{formatar_reais(maior_faturamento)}**."
)

# Comparação entre os meses
st.subheader("📊 Evolução do faturamento")

faturamento_mensal_analise = (
    dados_filtrados.groupby("mes")["faturamento"].sum().sort_index()
)

if len(faturamento_mensal_analise) >= 2:
    mes_anterior = faturamento_mensal_analise.iloc[-2]
    mes_atual = faturamento_mensal_analise.iloc[-1]

    diferenca = mes_atual - mes_anterior

    if diferenca > 0:
        st.success(
           f"O faturamento aumentou {formatar_reais(diferenca)} "
            "em relação ao mês anterior."
        )
    elif diferenca < 0:
        st.warning(
            f"O faturamento diminuiu {formatar_reais(abs(diferenca))} "
            "em relação ao mês anterior."
        )
    else:
        st.info("O faturamento permaneceu igual ao mês anterior.")
else:
    st.info("São necessários pelo menos dois meses de vendas para comparar.")

# Recomendações automáticas
st.subheader("💡 Recomendações do analista")

if len(vendas_por_produto) > 1:
    produto_menos_vendido = vendas_por_produto.idxmin()

    st.write(
        f"Vale acompanhar o desempenho de **{produto_menos_vendido}**, "
        "pois foi o produto com menor quantidade vendida."
    )

if len(faturamento_regiao) > 1:
    regiao_menor_faturamento = faturamento_regiao.idxmin()

    st.write(
        f"A região **{regiao_menor_faturamento}** apresentou o menor "
        "faturamento. Vale investigar oportunidades comerciais nessa região."
    )