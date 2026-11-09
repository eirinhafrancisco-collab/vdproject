# Relatório de Análise Exploratória (EDA) e Pré-processamento
**Dataset:** `merged_major_occupations.csv`

---

## 1. Carregamento e Dimensões do Dataset

* **Dimensões totais (Linhas x Colunas):** `1505 x 18`
* **Cursos únicos (`cip4`):** `285`
* **Códigos de profissão únicos (`soc`):** `449` *(Nota: existem 463 títulos em `occupation`, o que indica 10 pares `(cip4, soc)` com variações ou sub-especializações de título no mesmo código SOC).*
* **Áreas académicas alargadas (`broad_field`):** `37`

---

## 2. Tipos de Dados, Valores Nulos (NaN) e Cardinalidade

| Coluna | Tipo (`dtype`) | Nulos (Qtd) | Nulos (%) | Valores Únicos | Exemplo (1ª linha) |
| :--- | :--- | :---: | :---: | :---: | :--- |
| `cip4` | `object` | 0 | 0.00% | 285 | `100` *(perdeu o zero à esquerda)* |
| `field_of_study` | `object` | 0 | 0.00% | 285 | `Agriculture, General` |
| `broad_field` | `object` | 0 | 0.00% | 37 | `Agricultural/Animal/Plant/Veterinary Science...` |
| `broad_field_short` | `object` | 0 | 0.00% | 37 | `Agriculture` |
| `soc` | `object` | 0 | 0.00% | 449 | `19-1011` |
| `occupation` | `object` | 0 | 0.00% | 463 | `Animal Scientists` |
| `occ_ai_exposure` | `float64` | 0 | 0.00% | 426 | `1.041` |
| `occ_ai_exposure_language` | `float64` | 0 | 0.00% | 430 | `0.972` |
| `occ_ai_exposure_image` | `float64` | 0 | 0.00% | 435 | `1.12` |
| `field_ai_exposure` | `float64` | 0 | 0.00% | 234 | `0.806` |
| `field_ai_exposure_percentile` | `float64` | 0 | 0.00% | 258 | `30.3` |
| `field_ai_exposure_language` | `float64` | 0 | 0.00% | 236 | `0.827` |
| `field_ai_exposure_image` | `float64` | 0 | 0.00% | 241 | `0.691` |
| `median_starting_salary` | `int64` | 0 | 0.00% | 285 | `39292` |
| `median_salary_4yr` | `float64` | **31** | **2.06%** | 276 | `52676.0` |
| `n_occupations` | `int64` | 0 | 0.00% | 20 | `4` |
| `n_institutions` | `int64` | 0 | 0.00% | 129 | `48` |
| `n_graduates` | `int64` | 0 | 0.00% | 266 | `2162` |

---

## 3. Verificação de Duplicados e Formatação de Strings

* **Linhas 100% duplicadas:** `0`
* **Pares `(cip4, soc)` duplicados:** `10` *(diferem no nome descritivo da coluna `occupation` ou métricas associadas; como `count(linhas) == n_occupations` para todos os cursos, estas linhas fazem parte da contagem oficial `n_occupations` do curso).*
* **Comprimento das strings em `cip4`:** `{4: 1327, 3: 178}` -> **178 linhas perderam o zero à esquerda** ao serem guardadas no CSV (ex.: `"100"` em vez de `"0100"`, `"408"` em vez de `"0408"`).
* **Strings com espaços extra (início/fim):** `0` em todas as colunas de texto.

---

## 4. Estatísticas Descritivas — Nível Par Curso-Ocupação (`N = 1505`)

| Variável | Count | Mean | Std | Min | 1% | 5% | 25% | 50% (Med) | 75% | 95% | 99% | Max |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `occ_ai_exposure` | 1505 | 0.7535 | 0.7403 | -2.670 | -1.6178 | -0.8860 | 0.450 | 1.010 | 1.320 | 1.418 | 1.4820 | 1.528 |
| `occ_ai_exposure_language` | 1505 | 0.7607 | 0.7714 | -1.793 | -1.4127 | -0.8940 | 0.354 | 0.977 | 1.323 | 1.669 | 1.8130 | 1.857 |
| `occ_ai_exposure_image` | 1505 | 0.6720 | 0.7953 | -3.655 | -1.6482 | -0.7562 | 0.244 | 0.803 | 1.270 | 1.791 | 2.2442 | 2.421 |

---

## 5. Estatísticas Descritivas — Nível do Curso (Deduplicado por `cip4`, `N = 285`)

| Variável | Count | Mean | Std | Min | 1% | 5% | 25% | 50% (Med) | 75% | 95% | 99% | Max |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `field_ai_exposure` | 285 | 0.8281 | 0.5498 | -1.201 | -1.0926 | -0.4074 | 0.677 | 1.035 | 1.189 | 1.3352 | 1.3976 | 1.419 |
| `field_ai_exposure_percentile` | 285 | 50.0007 | 29.0186 | 0.000 | 1.0360 | 4.9800 | 25.000 | 50.000 | 75.000 | 95.0200 | 98.9640 | 100.000 |
| `field_ai_exposure_language` | 285 | 0.8401 | 0.5919 | -1.174 | -0.9408 | -0.3798 | 0.618 | 0.982 | 1.244 | 1.5364 | 1.6945 | 1.857 |
| `field_ai_exposure_image` | 285 | 0.7391 | 0.5806 | -1.796 | -1.0043 | -0.4028 | 0.415 | 0.852 | 1.128 | 1.4856 | 1.6808 | 1.815 |
| `median_starting_salary` | 285 | 46381.31 | 17499.12 | 10084.0 | 18900.44 | 24529.20 | 33319.0 | 41189.0 | 59738.0 | 75895.20 | 92535.48 | 106754.0 |
| `median_salary_4yr` | **277** | 67427.06 | 20203.50 | 22986.0 | 37205.48 | 40585.00 | 51701.0 | 64445.0 | 82019.0 | 102405.60 | 123230.32 | 145296.0 |
| `n_occupations` | 285 | 5.2807 | 4.3042 | 1.0 | 1.00 | 1.00 | 3.0 | 4.0 | 7.0 | 12.80 | 19.32 | 36.0 |
| `n_institutions` | 285 | 87.1649 | 168.9280 | 1.0 | 1.00 | 1.00 | 5.0 | 22.0 | 79.0 | 418.40 | 860.04 | 1216.0 |
| `n_graduates` | 285 | 8532.75 | 32278.06 | 16.0 | 17.84 | 26.20 | 212.0 | 1358.0 | 4136.0 | 36206.00 | 89531.68 | 429074.0 |

---

## 6. Distribuição por Categoria Académica (`broad_field`)

| Categoria Alargada (`broad_field`) | Sigla (`broad_field_short`) | Nº Cursos | Total Graduados | Salário Inicial Mediano ($) | Salário 4 Anos Mediano ($) | Exposição IA Média |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| Engineering | Engineering | 38 | 126,642 | 73,001.5 | 93,119.0 | 1.059 |
| Multi/Interdisciplinary Studies | Interdisciplinary | 22 | 19,452 | 35,739.5 | 59,462.5 | 1.189 |
| Business, Management, Marketing... | Business | 19 | 563,489 | 50,722.0 | 72,480.0 | 1.112 |
| Health Professions and Related Programs | Health Professions | 18 | 521,977 | 38,612.0 | 63,231.5 | 0.394 |
| Engineering/Engineering-Related Tech... | Engineering Tech | 17 | 23,092 | 62,554.0 | 81,852.0 | 0.266 |
| Agricultural/Animal/Plant/Veterinary... | Agriculture | 15 | 19,282 | 43,778.0 | 56,812.0 | 0.274 |
| Biological and Biomedical Sciences | Biological Sciences | 14 | 97,726 | 33,873.0 | 64,820.0 | 1.025 |
| Social Sciences | Social Sciences | 12 | 127,382 | 36,930.0 | 55,992.0 | 1.136 |
| Education | Education | 12 | 96,342 | 38,231.0 | 47,700.0 | 1.058 |
| Visual and Performing Arts | Visual & Performing Arts | 10 | 85,311 | 24,915.0 | 43,597.0 | 0.281 |
| Architecture and Related Services | Architecture | 8 | 6,213 | 46,176.5 | 67,204.0 | 1.067 |
| Physical Sciences | Physical Sciences | 8 | 14,445 | 42,090.5 | 66,780.5 | 1.132 |
| Foreign Languages, Literatures... | Foreign Languages | 8 | 11,083 | 34,727.0 | 54,141.0 | 1.220 |
| Computer and Information Sciences... | Computer Science | 8 | 152,542 | 59,856.0 | 80,813.0 | 1.128 |
| Family and Consumer Sciences... | Family & Consumer Sci | 7 | 30,352 | 36,945.0 | 52,861.0 | 0.865 |
| Theology and Religious Vocations | Theology & Religion | 6 | 5,022 | 32,218.5 | 44,867.0 | 1.270 |
| Natural Resources and Conservation | Natural Resources | 6 | 19,370 | 34,256.0 | 51,279.0 | 0.378 |
| Communication, Journalism... | Communication | 6 | 115,194 | 34,661.5 | 55,118.0 | 1.072 |
| Public Administration and Social Service... | Public Administration | 5 | 33,374 | 41,991.0 | 54,080.0 | 1.042 |
| Psychology | Psychology | 4 | 129,129 | 34,479.0 | 53,810.0 | 1.202 |
| Homeland Security, Law Enforcement... | Homeland Security | 4 | 89,072 | 44,140.0 | 63,437.0 | 0.414 |
| English Language and Literature/Letters | English | 4 | 38,112 | 26,328.5 | 46,594.0 | 1.274 |
| Parks, Recreation, Leisure, Fitness... | Parks & Recreation | 4 | 44,920 | 32,276.5 | 49,805.0 | -0.045 |
| Mathematics and Statistics | Mathematics & Statistics | 4 | 14,644 | 59,639.5 | 91,876.0 | 1.372 |
| Legal Professions and Studies | Legal | 3 | 3,462 | 39,558.0 | 65,388.0 | 1.270 |
| Mechanic and Repair Technologies... | Mechanic & Repair Tech | 3 | 232 | 65,331.0 | 82,773.5 | -0.814 |
| Communications Technologies... | Communications Tech | 3 | 4,737 | 23,526.0 | 43,858.0 | 0.273 |
| Philosophy and Religious Studies | Philosophy & Religion | 3 | 5,062 | 28,712.0 | 55,814.0 | 1.359 |
| Area, Ethnic, Cultural, Gender... | Area & Ethnic Studies | 2 | 6,607 | 32,835.0 | 55,077.0 | 1.260 |
| Military Technologies and Applied Sci... | Military Tech | 2 | 494 | 60,405.5 | 78,622.5 | 0.288 |
| Science Technologies/Technicians | Science Tech | 2 | 680 | 65,255.0 | 87,817.0 | 0.450 |
| Transportation and Materials Moving | Transportation | 2 | 6,895 | 63,615.5 | 99,285.0 | -0.253 |
| Culinary, Entertainment, and Personal... | Culinary & Personal Svc | 2 | 1,362 | 39,862.5 | 54,358.0 | -0.439 |
| Library Science | Library Science | 1 | 70 | 27,108.0 | 38,786.0 | 1.009 |
| History | History | 1 | 17,835 | 31,194.0 | 51,168.0 | 0.855 |
| Construction Trades | Construction Trades | 1 | 206 | 72,864.0 | 90,691.0 | -1.201 |
| Precision Production | Precision Production | 1 | 24 | 19,151.0 | 37,055.0 | -1.101 |

---

## 7. Check de Consistência, Outliers e Valores Nulos

* **Consistência `count(linhas) == n_occupations`:** `0` discrepâncias (100% consistente).
* **Consistência Salarial (`median_salary_4yr < median_starting_salary`):** `0` casos (todos os cursos têm progressão salarial positiva aos 4 anos).
* **Consistência de Exposição à IA (`mean(occ_ai_exposure)` vs `field_ai_exposure`):** Diferença média de `0.000254` (máx `0.000714`), confirmando que `field_ai_exposure` é exatamente a média simples das ocupações mapeadas, arredondada a 3 casas decimais.
* **Valores Nulos (`NaN`):** Existem exatamente **31 linhas** (correspondentes a **8 cursos únicos** de nicho, todos com `n_institutions == 1` e entre 17 a 27 graduados) onde falta apenas `median_salary_4yr`.
* **Outliers (Critério IQR 1.5x):**
  * **Variáveis de Volume (`n_graduates`, `n_institutions`, `n_occupations`):** Forte assimetria positiva (*right-skewed*). Cursos de massas (como *Business* ou *Nursing*) chegam a 429,074 graduados face a uma mediana de 1,358. São valores reais do mercado académico e **não erros de medição** — em vez de remoção, beneficiam de transformação logarítmica (`log10`) se forem usados em escalas contínuas.
  * **Variáveis de Exposição à IA (`occ_ai_exposure*`, `field_ai_exposure*`):** Os valores "outliers" na cauda inferior (ex.: `-2.67` ou `-3.655`) correspondem a profissões de trabalho físico/manual (*Construction Trades*, *Mechanic & Repair Tech*) cuja exposição à IA é naturalmente muito baixa (scores estandardizados *Z-score*).

---

## 8. Decisões de Pré-processamento Implementadas

1. **Restauro de Códigos `cip4` (`zfill(4)`):** Corrigir as 178 linhas cujo código `cip4` tem 3 caracteres (ex.: `"100"` -> `"0100"`).
2. **Desambiguação dos 10 pares `(cip4, soc)` repetidos:** Verificar se são profissões com títulos ligeiramente distintos no mesmo `soc` ou duplicados reais, mantendo a integridade com `n_occupations`.
3. **Imputação Hierárquica e Flag de Nulos em `median_salary_4yr`:**
   * Criar a coluna booleana `is_salary_4yr_imputed` (`True` nas 31 linhas / 8 cursos sem salário aos 4 anos) para transparência analítica.
   * Imputar os 8 cursos em falta estimando o salário aos 4 anos através do **rácio mediano de crescimento salarial da respetiva área académica (`broad_field`)**: $	ext{Salário 4 Anos Estimado} = 	ext{Salário Inicial} 	imes 	ext{Mediana}\left(rac{	ext{Salário 4 Anos}}{	ext{Salário Inicial}}ight)_{	ext{broad\_field}}$. Isto é muito mais rigoroso do que usar uma mediana simples, pois respeita o salário inicial real de cada curso (ex.: $17,585 em *Publishing* vs. $60,240 em *Slavic Languages*).
4. **Engenharia de Variáveis (*Feature Engineering*) para Visualização:**
   * `salary_growth_abs`: Ganho salarial absoluto após 4 anos ($	ext{median\_salary\_4yr} - 	ext{median\_starting\_salary}$).
   * `salary_growth_pct`: Taxa de crescimento salarial em percentagem ($rac{	ext{salary\_growth\_abs}}{	ext{median\_starting\_salary}} 	imes 100$).
   * `occ_vs_field_ai_diff`: Diferença entre a exposição à IA da profissão específica e a média do curso ($	ext{occ\_ai\_exposure} - 	ext{field\_ai\_exposure}$), permitindo destacar quais as saídas profissionais mais ou menos expostas dentro de um mesmo curso.
   * `field_ai_tier` e `occ_ai_tier`: Categorização qualitativa de exposição à IA (*Baixa*, *Moderada*, *Alta*, *Muito Alta*) baseada em quartis, facilitando filtros e cores em dashboards.
   * `log10_n_graduates` e `log10_n_institutions`: Transformação $\log_{10}(x)$ para visualização limpa de variáveis com forte assimetria sem perder os extremos.
5. **Exportação Dupla (Duas Granularidades):**
   * `cleaned_major_occupations.csv` (`1505` linhas): Tabela ao nível **Curso-Ocupação** (formato longo), ideal para gráficos de rede, *sankey*, *treemaps* ou detalhe de saídas profissionais.
   * `cleaned_majors_unique.csv` (`285` linhas): Tabela deduplicada ao nível do **Curso** (`cip4`), garantindo que *scatter plots*, *boxplots* e médias globais por curso não são distorcidos pelo número de profissões de cada curso.
