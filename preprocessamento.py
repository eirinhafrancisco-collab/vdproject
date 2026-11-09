"""
Script de Análise Exploratória (EDA) e Pré-processamento
Dataset: merged_major_occupations.csv
"""

import pandas as pd
import numpy as np

# Configuração para ver todas as colunas direitinhas no terminal
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth', 50)

# ==============================================================================
# 1. ANÁLISE EXPLORATÓRIA DE DADOS (EDA)
# ==============================================================================

print("=" * 80)
print("1. CARREGAMENTO E DIMENSÕES DO DATASET")
print("=" * 80)

# sep=None com engine='python' deteta automaticamente se o CSV está separado por ',' ou ';'
df = pd.read_csv("merged_major_occupations.csv", sep=None, engine="python", dtype={"cip4": str, "soc": str})

print(f"Dimensões totais (Linhas x Colunas): {df.shape[0]} x {df.shape[1]}")
print(f"Cursos únicos (cip4):                {df['cip4'].nunique()}")
print(f"Profissões únicas (soc):             {df['soc'].nunique()}")
print(f"Áreas alargadas (broad_field):       {df['broad_field'].nunique()}")

print("\n" + "=" * 80)
print("2. TIPOS DE DADOS, VALORES NULOS (NaN) E CARDINALIDADE")
print("=" * 80)
info_df = pd.DataFrame({
    "Tipo (dtype)": df.dtypes,
    "Nulos (Qtd)": df.isna().sum(),
    "Nulos (%)": (df.isna().sum() / len(df) * 100).round(2),
    "Valores Únicos": df.nunique(),
    "Exemplo (1ª linha)": df.iloc[0].values
})
print(info_df)

print("\n" + "=" * 80)
print("3. VERIFICAÇÃO DE DUPLICADOS E FORMATAÇÃO DE STRINGS")
print("=" * 80)
print(f"Linhas 100% duplicadas:              {df.duplicated().sum()}")
print(f"Pares (cip4, soc) duplicados:        {df.duplicated(subset=['cip4', 'soc']).sum()}")
print(f"Comprimento das strings em 'cip4':   {df['cip4'].str.len().value_counts().to_dict()}")

str_cols = df.select_dtypes(include="object").columns
whitespace_issues = {col: int((df[col].str.strip() != df[col]).sum()) for col in str_cols if df[col].notna().any()}
print(f"Strings com espaços extra (início/fim): {whitespace_issues}")

print("\n" + "=" * 80)
print("4. ESTATÍSTICAS DESCRITIVAS — NÍVEL PAR CURSO-OCUPAÇÃO (Todas as linhas)")
print("=" * 80)
occ_num_cols = ["occ_ai_exposure", "occ_ai_exposure_language", "occ_ai_exposure_image"]
print(df[occ_num_cols].describe(percentiles=[0.01, 0.05, 0.25, 0.5, 0.75, 0.95, 0.99]).T.round(4))

print("\n" + "=" * 80)
print("5. ESTATÍSTICAS DESCRITIVAS — NÍVEL DO CURSO (Deduplicado por cip4)")
print("=" * 80)
# Deduplicamos por cip4 para que os cursos com mais profissões não distorçam as médias
df_courses = df.drop_duplicates(subset=["cip4"]).copy()
course_num_cols = [
    "field_ai_exposure", "field_ai_exposure_percentile",
    "field_ai_exposure_language", "field_ai_exposure_image",
    "median_starting_salary", "median_salary_4yr",
    "n_occupations", "n_institutions", "n_graduates"
]
print(df_courses[course_num_cols].describe(percentiles=[0.01, 0.05, 0.25, 0.5, 0.75, 0.95, 0.99]).T.round(4))

print("\n" + "=" * 80)
print("6. DISTRIBUIÇÃO POR CATEGORIA ACADÉMICA (broad_field)")
print("=" * 80)
broad_summary = df_courses.groupby(["broad_field", "broad_field_short"], dropna=False).agg(
    n_cursos=("cip4", "count"),
    total_graduados=("n_graduates", "sum"),
    salario_inicial_med=("median_starting_salary", "median"),
    salario_4anos_med=("median_salary_4yr", "median"),
    ai_exposure_media=("field_ai_exposure", "mean")
).sort_values(by="n_cursos", ascending=False)
print(broad_summary.round(3))

print("\n" + "=" * 80)
print("7. CHECK DE CONSISTÊNCIA E ANOMALIAS LÓGICAS")
print("=" * 80)
# 7.1 Verificar se n_occupations bate certo com o número de linhas por cip4
occ_counts = df.groupby("cip4").size()
mapped_counts = df_courses.set_index("cip4")["n_occupations"]
mismatches = (occ_counts != mapped_counts.loc[occ_counts.index]).sum()
print(f"Cursos onde count(linhas) != n_occupations: {mismatches}")

# 7.2 Verificar se há salários a 4 anos inferiores ao salário inicial
sal_drop = df_courses[df_courses["median_salary_4yr"] < df_courses["median_starting_salary"]]
print(f"Cursos com salário 4 anos < salário inicial: {len(sal_drop)}")
if len(sal_drop) > 0:
    print(sal_drop[["cip4", "field_of_study", "median_starting_salary", "median_salary_4yr"]])

# 7.3 Comparar a média simples de occ_ai_exposure com field_ai_exposure
calc_mean_ai = df.groupby("cip4")["occ_ai_exposure"].mean()
diff_ai = (calc_mean_ai - df_courses.set_index("cip4")["field_ai_exposure"]).abs()
print(f"Diferença máx entre mean(occ_ai_exposure) e field_ai_exposure: {diff_ai.max():.6f}")
print(f"Diferença média entre mean(occ_ai_exposure) e field_ai_exposure: {diff_ai.mean():.6f}")

# 7.4 Contagem de Outliers (critério IQR 1.5x)
print("\nContagem de potenciais Outliers (fora de [Q1 - 1.5*IQR, Q3 + 1.5*IQR]):")
for col in course_num_cols:
    s = df_courses[col].dropna()
    q1, q3 = s.quantile(0.25), s.quantile(0.75)
    iqr = q3 - q1
    outliers = ((s < (q1 - 1.5 * iqr)) | (s > (q3 + 1.5 * iqr))).sum()
    print(f"  [Curso]    {col:<30}: {outliers:>3} outliers (Min: {s.min()}, Max: {s.max()})")

for col in occ_num_cols:
    s = df[col].dropna()
    q1, q3 = s.quantile(0.25), s.quantile(0.75)
    iqr = q3 - q1
    outliers = ((s < (q1 - 1.5 * iqr)) | (s > (q3 + 1.5 * iqr))).sum()
    print(f"  [Ocupação] {col:<30}: {outliers:>3} outliers (Min: {s.min()}, Max: {s.max()})")

# 7.5 Linhas com valores nulos
rows_with_nulls = df[df.isna().any(axis=1)]
print(f"\nTotal de linhas com pelo menos um valor nulo: {len(rows_with_nulls)}")
if len(rows_with_nulls) > 0:
    print(rows_with_nulls.head(10))


# ==============================================================================
# 2. EXPLICAÇÃO DA ANÁLISE E DECISÕES DE PRÉ-PROCESSAMENTO
# ==============================================================================
"""
EXPLICAÇÃO DETALHADA DOS RESULTADOS DA EDA E DECISÕES DE PRÉ-PROCESSAMENTO:

1. FORMATAÇÃO DE CÓDIGOS ('cip4'):
   - Problema detetado: A análise revelou 178 linhas onde 'cip4' tem apenas 3 caracteres 
     (ex: "100", "408", "910") em vez de 4, porque perderam o zero à esquerda ao 
     serem exportados/abertos anteriormente.
   - Ação: Aplicar `.str.zfill(4)` na coluna `cip4` para garantir o formato padrão de 
     4 dígitos ("0100", "0408", "0910").

2. PARES (cip4, soc) REPETIDOS E INTEGRIDADE DE 'n_occupations':
   - Problema detetado: Existem 0 linhas 100% duplicadas, mas existem 10 pares (cip4, soc) 
     repetidos (porque existem 463 títulos de `occupation` para 449 códigos `soc` únicos). 
     Além disso, verificámos que `count(linhas) == n_occupations` tem 0 erros em todos os 285 cursos.
   - Ação: Não eliminar estas 10 linhas, pois representam especializações/títulos distintos 
     dentro do mesmo código SOC e a sua remoção quebraria a consistência com a coluna 
     `n_occupations` e com o cálculo de `field_ai_exposure` (cuja diferença máxima para a 
     média das linhas é de apenas 0.0007).

3. TRATAMENTO DE VALORES NULOS ('median_salary_4yr'):
   - Problema detetado: Existem exatamente 31 linhas (correspondentes a 8 cursos únicos, 
     todos eles cursos pequenos com `n_institutions == 1` e entre 17 e 27 graduados) onde 
     `median_salary_4yr` é NaN (2.06% do dataset). Todas as outras 17 colunas têm 0% de nulos.
   - Ação: 
     a) Criar uma coluna de controlo booleana `is_salary_4yr_imputed` (True/False) para 
        sinalizar de forma transparente quais os cursos que levaram imputação.
     b) Em vez de apagar os 8 cursos ou imputar uma mediana cega global, calcular o fator 
        mediano de crescimento salarial (median_salary_4yr / median_starting_salary) dentro 
        de cada área académica (`broad_field`) ao nível do curso, e multiplicar pelo 
        `median_starting_salary` real do curso em falta. Assim respeitamos tanto a área 
        de estudo como o patamar salarial inicial específico do curso.

4. TRATAMENTO DE OUTLIERS E ASSIMETRIA (SKEWNESS):
   - Problema detetado: Variáveis de contagem (`n_graduates`, `n_institutions`, `n_occupations`) 
     apresentam vários "outliers" estatísticos pelo método IQR (ex: 43 cursos em `n_graduates`, 
     chegando a 429.074 graduados em Business vs mediana de 1.358). Já os outliers em 
     `ai_exposure` (ex: -2.67 ou -3.655) são profissões manuais/físicas com baixíssima exposição.
   - Ação: Como todos estes valores são dados reais e empíricos do mercado de trabalho/ensino 
     e não erros de recolha, NÃO devemos apagar nem truncar (winsorizar) estas linhas. 
     Para facilitar a visualização de dados (evitando que 2 ou 3 megacursos esmaguem os 
     eixos dos gráficos), criamos colunas transformadas com logaritmo de base 10: 
     `log10_n_graduates` e `log10_n_institutions`.

5. CRIAÇÃO DE NOVAS VARIÁVEIS (FEATURE ENGINEERING PARA VISUALIZAÇÃO):
   - `salary_growth_abs`: Crescimento salarial absoluto ao fim de 4 anos ($).
   - `salary_growth_pct`: Crescimento salarial percentual ao fim de 4 anos (%).
   - `occ_vs_field_ai_diff`: Diferença entre a exposição à IA da ocupação e a média do 
     respetivo curso (`occ_ai_exposure - field_ai_exposure`). Mostra se uma saída 
     profissional específica está mais ou menos exposta do que a média do curso.
   - `field_ai_tier` / `occ_ai_tier`: Discretização da exposição à IA em 4 escalões 
     ("Baixa", "Moderada", "Alta", "Muito Alta") para facilitar codificação por cores/filtros.

6. RESOLUÇÃO DA GRANULARIDADE 1:N (EXPORTAÇÃO DUPLA):
   - Problema estrutural: Como cada curso se repete N vezes (consoante `n_occupations`), 
     usar a tabela completa para gráficos ao nível do curso enviesa os resultados.
   - Ação: Exportar dois ficheiros finais prontos a usar nas ferramentas de visualização:
     1) `cleaned_major_occupations.csv` (1505 linhas - nível Par Curso-Ocupação).
     2) `cleaned_majors_unique.csv` (285 linhas - nível Curso único, deduplicado por `cip4`).
"""


# ==============================================================================
# 3. PRÉ-PROCESSAMENTO PROPRIAMENTE DITO
# ==============================================================================

print("\n" + "=" * 80)
print("8. EXECUÇÃO DO PRÉ-PROCESSAMENTO E VERIFICAÇÃO DAS ESCOLHAS")
print("=" * 80)

df_clean = df.copy()

# ------------------------------------------------------------------------------
# PASSO 1: Corrigir zeros à esquerda em 'cip4' e limpar strings
# ------------------------------------------------------------------------------
df_clean["cip4"] = df_clean["cip4"].astype(str).str.strip().str.zfill(4)
for col in ["field_of_study", "broad_field", "broad_field_short", "soc", "occupation"]:
    df_clean[col] = df_clean[col].astype(str).str.strip()

print("[PASSO 1] Comprimento de 'cip4' após zfill(4):", df_clean["cip4"].str.len().value_counts().to_dict())

# ------------------------------------------------------------------------------
# PASSO 2: Inspeção dos 10 pares (cip4, soc) repetidos
# ------------------------------------------------------------------------------
dup_pairs = df_clean[df_clean.duplicated(subset=["cip4", "soc"], keep=False)].sort_values(by=["cip4", "soc"])
print(f"\n[PASSO 2] Verificação dos {len(dup_pairs)//2} pares (cip4, soc) repetidos (mantidos para preservar n_occupations):")
print(dup_pairs[["cip4", "field_of_study", "soc", "occupation", "occ_ai_exposure"]].to_string(index=False))

# ------------------------------------------------------------------------------
# PASSO 3: Imputação de 'median_salary_4yr' via rácio de crescimento por 'broad_field'
# ------------------------------------------------------------------------------
# Flag booleana para registar quais os registos imputados
df_clean["is_salary_4yr_imputed"] = df_clean["median_salary_4yr"].isna()

# Calculamos o rácio mediano (salário 4 anos / salário inicial) ao nível do curso único por broad_field
temp_courses = df_clean.drop_duplicates(subset=["cip4"]).copy()
temp_courses["growth_ratio"] = temp_courses["median_salary_4yr"] / temp_courses["median_starting_salary"]

broad_growth_ratios = temp_courses.groupby("broad_field")["growth_ratio"].median().to_dict()
global_growth_ratio = temp_courses["growth_ratio"].median()

# Mapear o rácio da respetiva broad_field (ou global como fallback seguro)
mapped_ratios = df_clean["broad_field"].map(broad_growth_ratios).fillna(global_growth_ratio)

# Preencher apenas onde median_salary_4yr é NaN, arredondando ao inteiro mais próximo
df_clean["median_salary_4yr"] = np.where(
    df_clean["median_salary_4yr"].isna(),
    (df_clean["median_starting_salary"] * mapped_ratios).round(0),
    df_clean["median_salary_4yr"]
)
df_clean["median_salary_4yr"] = df_clean["median_salary_4yr"].astype(int)

print("\n[PASSO 3] Cursos que tinham 'median_salary_4yr' nulo e valores imputados:")
imputed_courses = df_clean[df_clean["is_salary_4yr_imputed"]].drop_duplicates(subset=["cip4"])
print(imputed_courses[[
    "cip4", "field_of_study", "broad_field_short", 
    "median_starting_salary", "median_salary_4yr"
]].to_string(index=False))
print(f"Total de NaNs restantes no dataset inteiro: {df_clean.isna().sum().sum()}")

# ------------------------------------------------------------------------------
# PASSO 4: Feature Engineering (Novas Variáveis para Visualização)
# ------------------------------------------------------------------------------
# 4.1 Progressão salarial absoluta e percentual (aos 4 anos)
df_clean["salary_growth_abs"] = df_clean["median_salary_4yr"] - df_clean["median_starting_salary"]
df_clean["salary_growth_pct"] = (
    (df_clean["salary_growth_abs"] / df_clean["median_starting_salary"]) * 100
).round(2)

# 4.2 Diferença de exposição à IA da ocupação face à média do curso
df_clean["occ_vs_field_ai_diff"] = (df_clean["occ_ai_exposure"] - df_clean["field_ai_exposure"]).round(3)

# 4.3 Transformações logarítmicas (base 10) para variáveis com forte assimetria positiva
df_clean["log10_n_graduates"] = np.log10(df_clean["n_graduates"]).round(4)
df_clean["log10_n_institutions"] = np.log10(df_clean["n_institutions"]).round(4)

# 4.4 Categorização em Escalões (Tiers por Quartis) de Exposição à IA
tier_labels = ["Baixa (Q1)", "Moderada (Q2)", "Alta (Q3)", "Muito Alta (Q4)"]

# Para o curso, usamos os percentis já existentes (0-25, 25-50, 50-75, 75-100)
df_clean["field_ai_tier"] = pd.cut(
    df_clean["field_ai_exposure_percentile"],
    bins=[-0.001, 25.0, 50.0, 75.0, 100.0],
    labels=tier_labels
)

# Para a ocupação, calculamos os quartis sobre a distribuição de occ_ai_exposure
df_clean["occ_ai_tier"] = pd.qcut(
    df_clean["occ_ai_exposure"],
    q=4,
    labels=tier_labels
)

print("\n[PASSO 4] Amostra das novas colunas criadas (Feature Engineering):")
new_cols = [
    "cip4", "soc", "salary_growth_abs", "salary_growth_pct", 
    "occ_vs_field_ai_diff", "log10_n_graduates", "field_ai_tier", "occ_ai_tier"
]
print(df_clean[new_cols].head(8).to_string(index=False))

# ------------------------------------------------------------------------------
# PASSO 5: Separação por Granularidade e Exportação dos Datasets Finais
# ------------------------------------------------------------------------------
# 1) Dataset Completo (Nível Par Curso-Ocupação: 1505 linhas)
OUT_OCC_CSV = "cleaned_major_occupations.csv"
df_clean.to_csv(OUT_OCC_CSV, index=False, encoding="utf-8")

# 2) Dataset ao Nível do Curso (Deduplicado por cip4: 285 linhas)
# Removemos as colunas exclusivas da ocupação individual para evitar confusão
occ_specific_cols = [
    "soc", "occupation", "occ_ai_exposure", "occ_ai_exposure_language", 
    "occ_ai_exposure_image", "occ_vs_field_ai_diff", "occ_ai_tier"
]
df_courses_clean = df_clean.drop(columns=occ_specific_cols).drop_duplicates(subset=["cip4"]).copy()

OUT_COURSE_CSV = "cleaned_majors_unique.csv"
df_courses_clean.to_csv(OUT_COURSE_CSV, index=False, encoding="utf-8")

print("\n" + "=" * 80)
print("9. RESUMO FINAL DA EXPORTAÇÃO")
print("=" * 80)
print(f"1) '{OUT_OCC_CSV}' (Nível Curso-Ocupação): {df_clean.shape[0]} linhas x {df_clean.shape[1]} colunas")
print(f"2) '{OUT_COURSE_CSV}'      (Nível Curso Único):    {df_courses_clean.shape[0]} linhas x {df_courses_clean.shape[1]} colunas")
print("Pré-processamento concluído com sucesso!")