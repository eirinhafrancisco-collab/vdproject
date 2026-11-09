# Documentação do Dataset: `merged_major_occupations.csv`

## Visão Geral

Este dataset resulta da fusão (*merge*) de informações relativas a **áreas de estudo universitárias (Majors)** e as respetivas **saídas profissionais (Occupations)**. Combina métricas de retorno financeiro (salários), dados demográficos institucionais e índices detalhados de exposição à Inteligência Artificial (IA) — tanto ao nível da profissão específica como ao nível agregado do curso.

## Dicionário de Dados

Abaixo encontra-se a descrição detalhada das 18 colunas que compõem o dataset, apresentadas exatamente pela ordem em que surgem no ficheiro CSV:

| # | Coluna | Tipo de Dados | Descrição |
| :--- | :--- | :--- | :--- |
| **1** | `cip4` | Texto / Código | Código **CIP** (*Classification of Instructional Programs*) de 4 dígitos que identifica de forma padronizada a área de estudo. |
| **2** | `field_of_study` | Texto | Nome específico do curso ou área de estudo (ex: *Computer Science*, *Nursing*). |
| **3** | `broad_field` | Texto | Categoria académica alargada onde o curso se insere (ex: *Engineering*, *Health Professions*). |
| **4** | `broad_field_short` | Texto | Versão abreviada ou sigla da categoria académica alargada (ideal para gráficos e visualizações). |
| **5** | `soc` | Texto / Código | Código **SOC** (*Standard Occupational Classification*) que identifica a profissão de forma padronizada. |
| **6** | `occupation` | Texto | Título ou nome descritivo da profissão associada à área de estudo. |
| **7** | `occ_ai_exposure` | Numérico (Float) | Índice global de exposição da profissão (`soc`) à Inteligência Artificial. |
| **8** | `occ_ai_exposure_language` | Numérico (Float) | Índice de exposição da profissão especificamente a modelos de linguagem (LLMs / processamento de texto). |
| **9** | `occ_ai_exposure_image` | Numérico (Float) | Índice de exposição da profissão especificamente a tecnologias de geração e reconhecimento de imagem/visão computacional. |
| **10** | `field_ai_exposure` | Numérico (Float) | Índice global de exposição da área de estudo (`cip4`) à IA, considerando o conjunto das suas saídas profissionais. |
| **11** | `field_ai_exposure_percentile` | Numérico (Float/Int) | Percentil de exposição à IA da área de estudo em comparação com todos os outros cursos (de 0 a 100). |
| **12** | `field_ai_exposure_language` | Numérico (Float) | Índice agregado de exposição da área de estudo a modelos de linguagem (LLMs). |
| **13** | `field_ai_exposure_image` | Numérico (Float) | Índice agregado de exposição da área de estudo a modelos de imagem. |
| **14** | `median_starting_salary` | Numérico | Salário mediano de entrada no mercado de trabalho para recém-graduados desta área de estudo. |
| **15** | `median_salary_4yr` | Numérico | Salário mediano dos graduados 4 anos após a conclusão do curso. |
| **16** | `n_occupations` | Inteiro | Número total de profissões distintas mapeadas/associadas a esta área de estudo. |
| **17** | `n_institutions` | Inteiro | Número de instituições de ensino superior que oferecem este curso/área de estudo. |
| **18** | `n_graduates` | Inteiro | Número total de estudantes graduados registados nesta área de estudo. |

## Notas sobre a Estrutura (Pós-Merge)

* **Granularidade:** Cada linha do dataset representa um par único entre um curso (`cip4`) e uma profissão (`soc`).
* **Repetição de Dados de Curso:** Como um curso pode dar acesso a várias profissões (relação `1:N`), os dados específicos da área de estudo (colunas 1 a 4 e 10 a 18) irão repetir-se nas linhas que partilham o mesmo `cip4`, variando apenas os dados das colunas referentes à ocupação (colunas 5 a 9).