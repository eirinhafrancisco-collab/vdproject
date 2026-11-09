"""
Junta ai_salary_majors.csv (1 linha por curso) com major_occupations.csv
(1 linha por par curso-ocupação) usando o código CIP de 4 dígitos (cip4).

Resultado: uma tabela em formato longo (1 linha por par curso-ocupação), com os
atributos do curso repetidos em cada linha.

ATENÇÃO: como os atributos do curso se repetem, somar n_graduates ou fazer a
média dos salários sobre esta tabela dá mais peso aos cursos com mais
ocupações. Para métricas ao nível do curso, deduplicar por cip4 primeiro.
"""
import pandas as pd

FIELDS_CSV = "ai_salary_majors.csv"
OCC_CSV = "major_occupations.csv"  # ajustar ao nome local
OUT_CSV = "merged_major_occupations.csv"

fields = pd.read_csv(FIELDS_CSV)
occ = pd.read_csv(OCC_CSV)

# 1) cip4 como texto de 4 caracteres: ao ler como inteiro perdem-se os zeros
#    à esquerda (ex.: 100 devia ser "0100").
for df in (fields, occ):
    df["cip4"] = df["cip4"].astype(str).str.zfill(4)

# 2) Evitar colisões de nomes: as colunas ai_exposure* existem nos dois
#    ficheiros, mas com significados e escalas diferentes
#    (curso = média das ocupações; ocupação = valor individual).
fields = fields.rename(
    columns={
        "ai_exposure": "field_ai_exposure",
        "ai_exposure_percentile": "field_ai_exposure_percentile",
        "ai_exposure_language": "field_ai_exposure_language",
        "ai_exposure_image": "field_ai_exposure_image",
    }
)
occ = occ.rename(
    columns={
        "ai_exposure": "occ_ai_exposure",
        "ai_exposure_language": "occ_ai_exposure_language",
        "ai_exposure_image": "occ_ai_exposure_image",
    }
)

# 3) Os nomes dos cursos diferem entre ficheiros em ~60% dos cip4; usa-se o
#    nome do ficheiro de cursos e descarta-se o do ficheiro de ocupações.
occ = occ.drop(columns=["field_of_study"])

# 4) Validações antes de juntar
assert fields["cip4"].is_unique, "cip4 duplicado no ficheiro de cursos"
assert set(occ["cip4"]) <= set(fields["cip4"]), "cip4 em ocupações sem curso"
assert not occ.duplicated(["cip4", "soc"]).any(), "par curso-ocupação repetido"

# 5) Junção 1:N (cada linha de ocupação tem exatamente um curso)
merged = occ.merge(fields, on="cip4", how="left", validate="many_to_one")

# 6) Verificações pós-junção
assert len(merged) == len(occ)
assert merged["field_of_study"].notna().all()
counts = occ.groupby("cip4").size()
check = fields.set_index("cip4")["n_occupations"]
assert (counts == check.loc[counts.index]).all(), "n_occupations não bate"

# 7) Ordem de colunas: identificação, ocupação, curso
cols = [
    "cip4", "field_of_study", "broad_field", "broad_field_short",
    "soc", "occupation",
    "occ_ai_exposure", "occ_ai_exposure_language", "occ_ai_exposure_image",
    "field_ai_exposure", "field_ai_exposure_percentile",
    "field_ai_exposure_language", "field_ai_exposure_image",
    "median_starting_salary", "median_salary_4yr",
    "n_occupations", "n_institutions", "n_graduates",
]
merged = merged[cols]

merged.to_csv(OUT_CSV, index=False, encoding="utf-8")
print(f"{OUT_CSV}: {merged.shape[0]} linhas x {merged.shape[1]} colunas")