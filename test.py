import requests
import pandas as pd
import time
import os

API_KEY = "ad58f785280d84da4ff50cec60c3bc666d8dc00b98a203f61624aa7e529d499e"
url = "https://serpapi.com/search.json"
arquivo_excel = "lojas_roupa_goiania_cabulosa.xlsx"
capitais = [
    "Rio Branco", "Maceió", "Macapá", "Manaus", "Salvador", "Fortaleza", "Brasília", "Vitória",
    "Goiânia", "São Luís", "Cuiabá", "Campo Grande", "Belo Horizonte", "Belém", "João Pessoa",
    "Curitiba", "Recife", "Teresina", "Rio de Janeiro", "Natal", "Porto Alegre", "Porto Velho",
    "Boa Vista", "Florianópolis", "São Paulo", "Aracaju", "Palmas", "Itapuranga"
]

# Lista cabulosa de termos variados
termos = [
    "lojas de roupa",
    "lojas de roupa feminina",
    "moda masculina",
    "boutique feminina",
    "loja de roupas infantis",
    "loja de roupas plus size",
    "moda evangélica",
    "roupas baratas",
    "loja de moda fitness",
    "lojas de roupa atacado",
    "loja de moda casual",
    "lojas populares de roupa",
    "lojas de roupas centro",
    "loja de terno",
    "roupas para jovens"
]


# Carrega resultados existentes (cache), se houver
if os.path.exists(arquivo_excel):
    df_cache = pd.read_excel(arquivo_excel)
    print(f"📁 Cache carregado com {len(df_cache)} registros.")
else:
    df_cache = pd.DataFrame(columns=["Nome", "Telefone", "Endereço"])

resultados_novos = []
for capital in capitais:
    for termo in termos:
        consulta = f"{termo} em {capital}"
        print(f"🔍 Buscando: {consulta}")
        params = {
            "engine": "google",
            "q": consulta,
            "api_key": API_KEY
        }

        try:
            response = requests.get(url, params=params)
            data = response.json()

            locais = data.get("local_results", {}).get("places", [])

            for empresa in locais:
                if isinstance(empresa, dict):
                    nome = empresa.get("title", "N/A")
                    telefone = empresa.get("phone", "N/A")
                    endereco = empresa.get("address", "N/A")

                    novo_registro = {
                        "Nome": nome,
                        "Telefone": telefone,
                        "Endereço": endereco
                    }

                    # Verifica se já existe no cache
                    if not ((df_cache["Nome"] == nome) & (df_cache["Telefone"] == telefone)).any():
                        resultados_novos.append(novo_registro)

        except Exception as e:
            print(f"❌ Erro na consulta: {termo} -> {e}")

        time.sleep(2)

# Adiciona novos dados e remove duplicatas
df_novos = pd.DataFrame(resultados_novos)
df_final = pd.concat([df_cache, df_novos], ignore_index=True).drop_duplicates(subset=["Nome", "Telefone"])

# Salva o Excel atualizado
df_final.to_excel(arquivo_excel, index=False)

print(f"✅ {len(df_novos)} novas lojas adicionadas. Total agora: {len(df_final)} lojas únicas.")
