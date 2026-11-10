# Projeto #2 de Visualização de Dados: 6 perguntas para responder com gráficos

Dataset: TidyTuesday 2026-10-20 (*College majors, AI disruption risk and starting salaries*).
Tabelas limpas geradas por `prepare_data.py`: `courses_clean.csv` (285 cursos), `occupations_clean.csv` (463 profissões) e `merged_clean.csv` (1505 pares curso-profissão).

As perguntas seguem uma narrativa: **o tipo de exposição → onde estão as pessoas → onde está o dinheiro → o que a média esconde → como as áreas se ligam**.

---

## 1. O tipo de IA muda a relação com o salário?

- **Gráfico:** dois scatterplots lado a lado (facets), com linha de tendência.
  - `median_starting_salary` vs `field_ai_exposure_language`
  - `median_starting_salary` vs `field_ai_exposure_image`
- **Tabela:** `courses_clean.csv`
- **Porque é interessante:** a exposição global quase não se relaciona com o salário (Spearman ≈ 0), mas os dois tipos apontam em sentidos opostos: ≈ −0,21 para linguagem e ≈ +0,39 para imagem (salário inicial). Aos 4 anos, imagem sobe para ≈ +0,49.
- **Cuidados:** são correlações entre cursos, não causalidade. Marca os cursos com `low_sample` e diz que a exposição é um z-score.

## 2. Há cursos "seguros e bem pagos" e "expostos e mal pagos"?

- **Gráfico:** scatter dos 285 cursos com quadrantes anotados.
  - x: `field_ai_exposure`, y: `median_starting_salary`
  - cor: `broad_field_short`, tamanho: `n_graduates` (escala log)
- **Tabela:** `courses_clean.csv`
- **Porque é interessante:** é o gráfico "de capa", que mostra de uma vez onde cada curso fica entre risco e retorno.
- **Cuidados:** desenha `low_sample` com menos opacidade. Etiqueta só os extremos, senão fica ilegível.

## 3. A maioria dos graduados está em cursos muito expostos à IA?

- **Gráfico:** treemap ou sunburst `broad_field_short` → `field_of_study`.
  - área: `n_graduates`, cor: `field_ai_exposure`
- **Tabela:** `courses_clean.csv`
- **Porque é interessante:** mostra o peso real de cada área no mercado (Enfermagem tem ~429 mil, a mediana dos cursos ~1 400).
- **Cuidados:** `n_graduates` conta graduados com salário reportado, não o total real. Soma sempre sobre `courses`, nunca sobre `merged` (inflaciona os cursos com mais profissões).

## 4. A média de um curso esconde profissões muito diferentes?

- **Gráfico:** strip plot ou boxplot de `occ_ai_exposure` dentro de cada um dos 15 maiores cursos, com um marcador na média (`field_ai_exposure`).
- **Tabela:** `merged_clean.csv`
- **Porque é interessante:** `field_ai_exposure` é a média simples das profissões associadas, sem ponderar por quantas pessoas as exercem. Este gráfico mostra a limitação do indicador.
- **Cuidados:** usa os cursos com mais profissões (`n_occupations`), senão não há distribuição para mostrar.

## 5. Que cursos arrancam devagar mas disparam, e estão expostos à IA?

- **Gráfico:** dumbbell (salário inicial → salário aos 4 anos) dos 15 cursos com maior `salary_growth_ratio`, cor por `field_ai_exposure`.
- **Tabela:** `courses_clean.csv` (filtrar `has_4yr_salary`)
- **Porque é interessante:** o crescimento mediano é ~1,45x (de 1,02x a 2,98x), por isso o topo destaca-se. Cruza crescimento com exposição.
- **Cuidados:** o topo (Practical Nursing, 2,98x) parte de um salário inicial de 10 084 USD. Verifica `median_starting_salary` e `low_sample` antes de o destacar. Os 8 cursos sem salário aos 4 anos ficam de fora (diz-o na legenda).

## 6. Que profissões ligam áreas muito diferentes, e quão expostas são?

- **Gráfico:** sankey `broad_field_short` → `soc_group` (22 grupos), com cor pela exposição. Alternativa: grafo bipartido.
- **Tabela:** `merged_clean.csv` e `occupations_clean.csv` (`n_courses`)
- **Porque é interessante:** há "hubs": Engineering Managers aparece em 46 cursos e Natural Sciences Managers em 43.
- **Cuidados:** usar `soc_group` em vez das 463 profissões evita um sankey ilegível.

---

## Extra: análise de robustez (para o relatório)

Os professores do ensino superior (SOC 25-1xxx) aparecem em 216 dos 285 cursos e têm exposição alta. A coluna `field_ai_exposure_excl_postsec` recalcula a exposição do curso sem eles.

- O ranking mantém-se (Spearman ≈ 0,98 com a original).
- 11 cursos ficam sem valor, por só terem este tipo de profissão.
- Podes mostrar isto num slope chart (exposição com vs sem estes professores) ou repetir o gráfico 2 com a versão alternativa.

## Notas gerais para todos os gráficos

- **Escala da exposição:** são z-scores (média 0, DP 1) calculados na fonte; negativo significa "menos exposto que a média", não "sem exposição".
- **Salários:** USD, só bacharelatos, medianas das medianas das instituições (sem ponderar por graduados).
- **Áreas com ≤ 2 cursos** (9 de 37, por exemplo Construction Trades, History, Precision Production) não servem para médias ou boxplots por área.
- **Ler os CSV limpos** com `pd.read_csv(f, dtype={'cip4': str, 'soc': str})`, e nunca pelo Excel.