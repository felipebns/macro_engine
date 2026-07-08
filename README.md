## Arquitetura

Fluxo modular com separacao clara entre orquestracao, dados, LLM e UI.

1) `app.py` (Streamlit) recebe o cenario, aciona a `Pipeline` e renderiza JSON, markdown e graficos.
2) `Pipeline` coordena as etapas e consolida o contexto final.
3) `StockWrapper` baixa dados macro e de acoes, calcula periodos similares, retornos medios e ranking de setores/tickers.
4) `LLM_Wrapper` executa as etapas de parsing, riscos, JSON final e relatorio (com self-critique).
5) `Plot` gera graficos salvos em `data/plots`.

## Decisoes de prompt engineering

Os prompts usados estao dentro do codigo (em `services/prompts.py`), com separacao por etapa:

- Parsing: transforma o cenario em variacoes percentuais padronizadas.
- Riscos: força grounding no contexto e no cenario macro (evita justificativas meta).
- JSON final: explicita canais de transmissao e justificativas por setor/ticker.
- Self-critique: revisa o JSON final e remove incoerencias, mantendo o mesmo schema.

## Extensoes escolhidas

- Self-critique loop: garante racional mais consistente e canais de transmissao mais claros.
- Interface Streamlit: entrega uma UI simples e funcional para analise interativa.
- Canais de transmissao explicitos: presentes no JSON final e no relatorio.

## Por que escolhi aprofundar o Case 2

O Case 2 pareceu mais desafiador e alinhado as minhas habilidades de Tech/AI. Ele permite demonstrar
engenharia de dados, prompts, orquestracao e UI em um fluxo unico, e as extensoes agregam valor direto
para a interpretacao macro-setorial.

## Tempo gasto

Aproximadamente 20 horas, gastei muito tempo para baixar os relatórios FOCUS, mas eles se mostraram excepcionalmente difíceis de extrair dados consistentemente. Como utilizo algumas chamadas de LLM aqui, gastei bastante tempo também configurando seus prompts e como eu estou pegando dados de múltiplas fontes também, o processamento deles para decidir um período ideal para análise demorou mais do que esperava

## Limitacoes identificadas

- A comparacao usa o cenario atual do usuario versus variacoes historicas observadas, sem incorporar
	projeoes de mercado oficiais como baseline.
- Varias chamadas de LLM aumentam custo e podem propagar subjetividades ao longo do fluxo.
- A integracao com o relatório Focus foi tentada, mas a extracao dos PDFs mostrou baixa confiabilidade.

## Com mais 2 semanas eu faria

- Integraria dados de projeoes do relatorio Focus como baseline do cenario, com parser mais robusto.
- Implementaria validacao de consistencia dos outputs e testes automatizados para LLM e dados.

## Exemplo de execucao

Url para site: https://macroengine.streamlit.app/ 

Input: Dolar em 6.2

Output json: 

```json
{
    "sectors": {
        "benefited": [
            {
                "sector": "exportadoras",
                "rationale": "Exportadoras são top no contexto (sorted_sectors: exportadoras = 28.2728) e o cenário mostra affected_metrics.dolar = 20.16; isso indica vantagem potencial porque grande parte da receita é cotada em USD e a conversão para BRL tende a aumentar receita e margem. Evidência: forte cross-section (ranking/setor) mas limitada quanto a detalhes operacionais e hedges presentes nas empresas.",
                "transmission_mechanism": "Receita cotada em USD -> conversão para BRL amplificada por affected_metrics.dolar = 20.16 -> aumento de receita BRL e potencial melhoria de margens se custos locais não aumentarem proporcionalmente; canais explícitos: affected_metrics.dolar (20.16) altera receita convertida -> EBITDA/fluxo de caixa -> valuation. Observação objetiva: evidência operacional específica (hedges, custo em USD) é limitada no contexto."
            },
            {
                "sector": "papel e celulose",
                "rationale": "Papel e celulose está entre os líderes (sorted_sectors: papel e celulose = 19.8561) e várias empresas do setor vendem em mercados internacionais; com affected_metrics.dolar = 20.16 a conversão de receitas em USD para BRL tende a favorecer receitas e margens. Evidência direta sobre preços de commodity não está disponível no contexto, portanto há incerteza sobre persistência do efeito.",
                "transmission_mechanism": "Preços/volume denominados em USD -> conversão a BRL impactada por affected_metrics.dolar = 20.16 -> maior receita BRL e possível melhoria de margens se custos locais não subirem no mesmo ritmo; canais explícitos: affected_metrics.dolar -> receita BRL -> margem operacional/EBITDA. Evidência sobre preços internacionais de celulose não foi fornecida (evidência limitada)."
            },
            {
                "sector": "seguradoras",
                "rationale": "Seguradoras aparecem no ranking (seguradoras = 10.9242). A ligação positiva com choque cambial é menos direta; affected_metrics.dolar = 20.16 pode aumentar volatilidade e, condicionalmente, afetar resultados financeiros via rendimento de ativos e ajustes técnicos, mas o contexto não fornece métricas de reservas, duration ou mix de ativos, então a evidência direta é limitada.",
                "transmission_mechanism": "Maior volatilidade/impacto macro ligado a affected_metrics.dolar = 20.16 e possível reação política -> rendimento das carteiras e resultados financeiros das seguradoras mudam; canais explícitos: affected_metrics.dolar (20.16) / possível alteração de affected_metrics.selic (atualmente 0 no contexto) -> rendimento de ativos financeiros -> resultado financeiro / valuation. Observação objetiva: falta de dados sobre duration e composição de ativos reduz a robustez da conclusão."
            },
            {
                "sector": "construção civil",
                "rationale": "Construção civil aparece com score positivo (construção civil = 6.5922) no sorted_sectors; efeito indireto pode ocorrer se o choque cambial favorecer setores exportadores ou alterar demanda relativa por imóveis, porém o impacto depende do mix de insumos importados e financiamento. O contexto não informa composição de custos e exposição a importações, portanto a evidência é moderada/limitada.",
                "transmission_mechanism": "Diferença entre affected_metrics.dolar = 20.16 e estabilidade de affected_metrics.selic = 0 no cenário atual pode alterar custos relativos (insumos importados vs locais) e condições de financiamento; canais explícitos: affected_metrics.dolar -> custo de insumos importados -> margem de projetos; affected_metrics.selic (0) indica que, no cenário fornecido, custo de financiamento não foi alterado, mas se selic aumentasse a dinâmica mudaria. Evidência operacional específica é limitada."
            },
            {
                "sector": "óleo e gás",
                "rationale": "Óleo e gás tem presença no ranking (óleoe gás = 6.5321) e tende a se beneficiar de preços internacionais em USD; com affected_metrics.dolar = 20.16 a receita convertida para BRL pode melhorar. Entretanto, o contexto não traz preços de petróleo ou exposição específica, então a evidência direta sobre magnitude do benefício é limitada.",
                "transmission_mechanism": "Receita indexada a preços internacionais em USD -> conversão para BRL influenciada por affected_metrics.dolar = 20.16 -> potencial aumento de receita BRL e margens se custos locais não subirem proporcionalmente; canais explícitos: affected_metrics.dolar -> receita BRL -> EBITDA/fluxo de caixa. Observação objetiva: ausência de preço do petróleo ou dados de hedging no contexto reduz a certeza da estimativa."
            }
        ],
        "harmed": [
            {
                "sector": "shopping centers",
                "rationale": "Shopping centers estão listados entre os piores (shopping centers = -0.8254). Apreciação do dólar (affected_metrics.dolar = 20.16) tende a associar-se a pressão sobre consumo discricionário e, se ocorrer aperto monetário subsequente, queda de tráfego e vendas, afetando ocupação e receitas variáveis. O contexto não indica variação em affected_metrics.selic ou inflacao, então a evidência do canal consumo->juros é condicional.",
                "transmission_mechanism": "affected_metrics.dolar = 20.16 pode pressionar poder de compra via inflação importada e incerteza econômica -> queda do consumo discricionário -> vendas de lojistas -> receita variável e NOI dos shopping centers; canais explícitos: affected_metrics.dolar -> vendas inquilinos -> receita de aluguel variável -> NOI/valuation. Observação: ausência de mudança em affected_metrics.selic/inflacao no contexto torna o risco dependente de cenários adicionais (evidência condicional)."
            },
            {
                "sector": "alimentos e bebidas",
                "rationale": "Alimentos e bebidas aparecem negativos no ranking (alimentos e bebidas = -4.2026). A alta do dólar (affected_metrics.dolar = 20.16) pode elevar custos de embalagens e insumos importados e pressionar margens, mas o contexto não fornece preços de commodities alimentares, então a evidência direta é limitada.",
                "transmission_mechanism": "affected_metrics.dolar = 20.16 -> aumento do custo de insumos/embalagens importadas -> compressão de margem se repasse for parcial; canais explícitos: affected_metrics.dolar -> custo de produção -> margem bruta -> lucro operacional. Observação objetiva: falta de dados sobre composição de custos e preços de commodities no contexto reduz a força da inferência."
            },
            {
                "sector": "varejo",
                "rationale": "Varejo está entre os piores (varejo = -6.4380) e é sensível a deterioração do consumo e custo do crédito. affected_metrics.dolar = 20.16 pode, por canais macro, reduzir poder aquisitivo e, se acompanhandado por aumento de juros, agravar a queda de vendas; o contexto mostra piores tickers de consumo, mas não provê variação em affected_metrics.selic/inflacao, logo parte da evidência é condicional.",
                "transmission_mechanism": "affected_metrics.dolar = 20.16 pode reduzir poder de compra e elevar custos via inflação importada; canais explícitos: affected_metrics.dolar -> consumo discricionário -> receita e giro do varejo -> margens. Observação: ausência de mudança em affected_metrics.selic/inflacao no contexto atual torna algumas conexões condicionais e a evidência parcialmente limitada."
            },
            {
                "sector": "bancos",
                "rationale": "Bancos têm score moderado (bancos = 2.8899) mas podem ser impactados por choque cambial que eleva risco-país e deteriora qualidade de crédito. No contexto, affected_metrics.dolar = 20.16 está presente e affected_metrics.selic = 0 (sem alteração), logo o efeito sobre bancos depende de reação macro (por exemplo, se selic subir). A evidência direta sobre provisões e exposição cambial dos bancos não está disponível, portanto é limitada.",
                "transmission_mechanism": "affected_metrics.dolar = 20.16 -> aumento do risco-país/volatilidade -> possível piora na qualidade do crédito e necessidade de provisões; canais explícitos: affected_metrics.dolar -> risco de crédito -> provisões -> lucro líquido/valor. Observação objetiva: falta de dados sobre vencimentos, provisões e exposição cambial específica reduz a certeza das conclusões."
            },
            {
                "sector": "transportes",
                "rationale": "Transportes está presente no ranking (transportes = 4.2479) e é sensível a custos de combustíveis e volumes de comércio internacional. affected_metrics.dolar = 20.16 pode afetar custos e demanda internacional; a evidência histórica é moderada e o contexto não fornece preços de combustíveis, logo há incerteza quanto à magnitude.",
                "transmission_mechanism": "affected_metrics.dolar = 20.16 -> pode elevar custos logísticos/importados e afetar volumes de exportação/importação -> compressão de margens operacionais; canais explícitos: affected_metrics.dolar -> custo de combustível/insumos -> Ebitda operacional. Observação: ausência de preços de combustíveis e dados operacionais específicos limita a precisão da avaliação."
            }
        ]
    },
    "tickers": {
        "positive": [
            {
                "ticker": "SUZB3.SA",
                "justification": "Suzano (SUZB3.SA) é papel e celulose com grande parcela de receita em USD; no contexto SUZB3.SA está em best_stocks e sorted_sectors mostra papel e celulose com score elevado. Affected_metrics.dolar = 20.16 implica que a conversão de vendas em USD para BRL tende a elevar receita e margem, salvo reversão nos preços internacionais. Evidência direta sobre hedges e exposição de custo está ausente (evidência limitada)."
            },
            {
                "ticker": "EMBJ3.SA",
                "justification": "EMBJ3.SA figura entre os best_stocks (EMBJ3.SA = 38.03) e está associada ao setor 'exportadoras' que se beneficia de affected_metrics.dolar = 20.16 via conversão de receita em USD para BRL. A conclusão baseia-se no ranking e na métrica affected_metrics.dolar; há pouca granularidade operacional disponível no contexto (evidência limitada sobre estrutura de custo/hedges)."
            },
            {
                "ticker": "CMIG4.SA",
                "justification": "CMIG4.SA aparece em best_stocks; como empresa de energia com receitas reguladas, tende a oferecer previsibilidade de caixa em cenários voláteis. No contexto, affected_metrics.dolar = 20.16 está presente e affected_metrics.selic = 0 (cenário sem mudança de juros), de modo que a resiliência percebida é suportada por classificação/ranking, mas faltam dados operacionais detalhados (evidência limitada)."
            }
        ],
        "negative": [
            {
                "ticker": "YDUQ3.SA",
                "justification": "YDUQ3.SA (educação) está em worst_stocks; o setor depende de demanda doméstica e crédito estudantil. Affected_metrics.dolar = 20.16 no contexto indica choque cambial que, via canais macro, pode reduzir poder de compra e aumentar risco de inadimplência; affected_metrics.selic = 0 atualmente no cenário, mas se juros subissem o impacto sobre crédito aumentaria. Evidência operacional específica (elasticidade por segmento) não foi fornecida (evidência limitada)."
            },
            {
                "ticker": "COGN3.SA",
                "justification": "COGN3.SA (educação) aparece em worst_stocks e tem modelo dependente de crédito ao consumidor e mensalidades recorrentes. Affected_metrics.dolar = 20.16 sugere condição macro que pode reduzir demanda e elevar inadimplência; affected_metrics.selic = 0 no contexto atual, portanto parte do risco é condicional a alterações de juros. Há falta de dados granulares sobre carteira/recebíveis (evidência limitada)."
            },
            {
                "ticker": "ASAI3.SA",
                "justification": "ASAI3.SA (varejo/atacadista) figura entre as piores no ranking; com affected_metrics.dolar = 20.16 há risco de aumento de custos de embalagens/importados e perda de poder aquisitivo do consumidor, pressionando vendas e margens. O contexto não detalha composição de custos ou estratégias de repasse de preços, por isso a evidência é limitada."
            }
        ]
    },
    "top_risks": [
        {
            "rank": 1,
            "risk": "Mudança de regime macro-financeiro desencadeada pela depreciação cambial (FX) que não foi acompanhada pelo cenário histórico usado.",
            "why_it_matters": "O cenário atual indica dólar +20,16% enquanto Selic, inflação e PIB estão estimados como inalterados — uma depreciação desse porte pode forçar resposta do Banco Central (alta de juros) ou gerar saída de fluxo estrangeiro/risk-off, comprimindo múltiplos e revertendo a vantagem esperada para exportadoras e papel e celulose.",
            "evidence_from_context": [
                "affected_metrics: dolar = 20.16, selic = 0, inflacao = 0, pib = 0",
                "best_sectors: exportadoras, papel e celulose, seguradoras",
                "periods: [\"2018-02-01/2018-07-31\",\"2018-08-01/2019-01-31\",\"2022-11-01/2023-04-30\",\"2024-02-01/2024-07-31\",\"2024-06-01/2024-11-30\"]"
            ],
            "historical_clue": "Há precedentes nos períodos listados de movimentos macro que evoluíram para regimes distintos (ex.: episódios de volatilidade em 2018 e 2022-23), mas a relação direta entre um choque cambial isolado e resposta monetária não é perfeitamente reproduzida nos períodos fornecidos — evidência moderada/indireta.",
            "impact": "alto",
            "likelihood": "alto"
        },
        {
            "rank": 2,
            "risk": "Concentração excessiva em poucos papéis/sets: desempenho puxado por poucos nomes correlacionados com exportações e commodities.",
            "why_it_matters": "Top 3 tickers (EMBJ3.SA, CMIG4.SA, SUZB3.SA) apresentam ganhos médios muito superiores ao restante, e os setores líderes (exportadoras, papel e celulose) dominam o ranking; um choque idiossincrático em qualquer desses nomes ou uma correção nesses setores impacta fortemente o resultado do portfólio/teses.",
            "evidence_from_context": [
                "best_stocks: [\"EMBJ3.SA\",\"CMIG4.SA\",\"SUZB3.SA\"]",
                "all_stocks_sorted: top values -> EMBJ3 38.03, CMIG4 30.05, SUZB3 26.85 (distância grande para próximos)",
                "sorted_sectors: exportadoras 28.27, papel e celulose 19.86"
            ],
            "historical_clue": "Os scores mostram alta concentração nos líderes; não há detalhe nos períodos que comprove se a performance histórica foi diversificada ou puxada por poucos eventos, portanto a evidência é forte para concentração cross-section mas fraca quanto à repetibilidade histórica.",
            "impact": "alto",
            "likelihood": "alto"
        },
        {
            "rank": 3,
            "risk": "Reversão por choque de preço de commodities ou queda da demanda externa que neutraliza benefício cambial para exportadoras e papel e celulose.",
            "why_it_matters": "A tese parece se apoiar em vantagem cambial para exportadoras/papel e celulose; se o dólar forte for consequência de crescimento global fraco ou de queda nos preços de commodities, a receita em USD pode cair e margens/exportações não se traduzirão em valorização das ações líderes.",
            "evidence_from_context": [
                "best_sectors: exportadoras, papel e celulose",
                "affected_metrics: dolar = 20.16 (sem informação de commodities)",
                "periods: inclusão de janelas em 2022-2023 e 2018 que tiveram ciclos de commodities distintos"
            ],
            "historical_clue": "Os períodos fornecidos incluem episódios com diferentes trajetórias de commodities; não há métrica direta de preços de commodities no contexto, logo a hipótese de reversão por queda de commodities é plausível mas a evidência histórica direta é fraca.",
            "impact": "medio",
            "likelihood": "medio"
        }
    ],
    "periods": [
        "2018-02-01/2018-07-31",
        "2018-08-01/2019-01-31",
        "2022-11-01/2023-04-30",
        "2024-02-01/2024-07-31",
        "2024-06-01/2024-11-30"
    ]
}
```

Output markdown: 

## Resumo executivo
Affected_metrics principais: dolar = +20.16%, selic = 0 (sem mudança reportada), inflação/PIB sem alteração no contexto. O choque cambial eleva a atratividade nominal de receitas em USD, mas a ausência de variação em juros/inflação torna muitos efeitos condicionais e a evidência operacional é limitada.

## Top 5 setores beneficiados
- Exportadoras: Dólar +20,16% amplia conversão de receitas em USD para BRL, elevando receita e potencial margem; evidência operacional sobre hedges é limitada.  
- Papel e celulose: Similar às exportadoras, ganhos na conversão em BRL favorecem receitas, embora preços de commodities não tenham sido fornecidos.  
- Seguradoras: Podem se beneficiar de ativos reprecificados e oportunidades de rendimento, porém falta informação sobre duration e composição de carteira.  
- Construção civil: Impacto potencial via demanda relativa e insumos importados; efeito depende de exposição a custos em USD e financiamento.  
- Óleo e gás: Receita em USD tende a converter em mais BRL, apoiando EBITDA, mas ausência de dados de preço do petróleo e hedges reduz a certeza.

## Top 5 setores prejudicados
- Shopping centers: Dólar forte tende a pressionar consumo discricionário e vendas de lojistas, afetando NOI; canal é condicional à reação de juros/emprego.  
- Alimentos e bebidas: Custos de embalagens/insumos importados podem subir com o dólar, comprimindo margens sem garantia de repasse.  
- Varejo: Risco de queda de consumo e custo de crédito; impacto depende de se juros aumentarem (cenário atual mostra selic = 0).  
- Bancos: Choque cambial eleva risco-país e inadimplência potencial, aumentando provisões; falta de dados sobre exposições limita conclusão.  
- Transportes: Custos de combustíveis e volumes de comércio internacional podem ser afetados, comprimindo margens dependendo dos preços de energia.

## 3 tickers positivos (1–2 frases cada)
- SUZB3.SA: Papel e celulose com grande receita em USD; dólar em 20,16 favorece conversão de vendas para BRL, mas faltam dados de hedge.  
- EMBJ3.SA: Empresa ligada a exportadoras com alta posição no ranking; beneficia-se da conversão cambial reportada, com evidência operacional limitada.  
- CMIG4.SA: Energia regulada com caixa relativamente previsível; aparece entre os melhores e pode mostrar resiliência em cenário volátil, embora detalhes operacionais faltem.

## 3 tickers negativos (1–2 frases cada)
- YDUQ3.SA: Educação sensível a demanda doméstica e crédito; choque cambial pode reduzir poder de compra e elevar risco de inadimplência, sem dados segmentados.  
- COGN3.SA: Modelo dependente de mensalidades e crédito ao consumidor, vulnerável a deterioração do consumo; impacto condicional à evolução de juros.  
- ASAI3.SA: Varejo/atacado exposto a aumento de custos de embalagens/importados e perda de poder aquisitivo, pressionando margens sem granularidade de custos.

## Top 3 riscos (1–2 frases cada)
- Mudança de regime macro-financeiro (alto): Dólar +20,16 sem alteração de selic no cenário é inconsistente; resposta do BC (alta de juros) ou saída de fluxo estrangeiro pode reverter ganhos setoriais.  
- Concentração em poucos nomes (alto): Performance puxada por EMBJ3/CMIG4/SUZB3 aumenta vulnerabilidade a choques idiossincráticos nesses papéis.  
- Reversão por queda de commodities (médio): Se dólar forte refletir queda de demanda global ou preços de commodities, receitas em USD podem cair e anular a vantagem cambial.

## Observações finais
A leitura dos setores e tickers é fortemente influenciada por affected_metrics.dolar = 20.16, mas a ausência de variação em selic e falta de dados operacionais (hedges, composição de custos, preços de commodities) tornam muitas conclusões condicionais e baseadas em rankings cruzados, não em evidência granular.