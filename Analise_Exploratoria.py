from previsao_vendas import preco_info,df_anuncios
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd  # Importação de pandas estava faltando

# Função para converter preços para número
def converter_preco(preco):
    if isinstance(preco, str):
        return int(preco.replace("R$", "").replace(".", "").replace(",", "").strip())
    return preco

# Garantir que preco_info contém a chave "price"
if "price" in preco_info:
    preco_fipe = converter_preco(preco_info["price"]) / 100  # Corrigir escala
else:
    raise KeyError("A chave 'price' não foi encontrada em preco_info.")

# Verificar se df_anuncios está definido antes de usá-lo
if 'df_anuncios' not in globals():
    raise NameError("A variável df_anuncios não está definida. Certifique-se de carregá-la corretamente.")

def buscar_link():
    for link in df_anuncios["Link"]:
        print(link)
# Criar DataFrame corrigido
df_precos = pd.DataFrame({
    "Fonte": ["FIPE"] + ["Mercado Livre"] * len(df_anuncios),
    "Preço (R$)": [preco_fipe] + df_anuncios["Preço (R$)"].apply(converter_preco).tolist()
})

# Exibir estatísticas descritivas corrigidas
print("\n📊 Estatísticas descritivas dos preços (corrigidas):")
print(df_precos.groupby("Fonte")["Preço (R$)"].describe())

# Criar gráfico de comparação
plt.figure(figsize=(8, 5))
sns.boxplot(x="Fonte", y="Preço (R$)", data=df_precos, palette="coolwarm")
plt.title("📈 Comparação de Preços - FIPE vs Mercado Livre")
plt.ylabel("Preço (R$)")
plt.xlabel("Fonte")
plt.grid(True)
plt.show()

