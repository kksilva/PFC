# Guia de Estilo de Escrita Técnica — Karine Giselle de Souza Silva

Este guia consolida duas fontes:

1. **`modelo_PFC_latex.pdf`** (nesta pasta) — o modelo oficial de monografia do curso, que
   inclui um manual de escrita técnica completo (Capítulo 3, "Metodologia", Seções 3.1 a 3.7).
   Esta é a **fonte normativa**: em caso de conflito, prevalece sobre qualquer outra observação
   deste guia.
2. A análise do estilo já praticado nos seus relatórios (Proposta de Projeto, Relatórios
   Parciais 1–3, Relatório Experimental), que mostra como você aplica esses princípios na
   prática e serve de referência de tom e terminologia.

Use este guia ao redigir ou revisar qualquer capítulo em `PFC_monografia/`.

---

## 1. Estrutura esperada por capítulo (conforme o modelo)

| Capítulo | Seções |
|---|---|
| 1. Introdução | 1.1 Motivação e Justificativa · 1.2 Objetivos do Projeto · 1.3 Local de Realização · 1.4 Estrutura da Monografia |
| 2. Descrição do Processo | 2.1 Processo/sistema estudado · 2.2 Instrumentação do Processo · 2.3 Situação Atual/Estado da Arte/Revisão da Literatura (2.3.1 Como elaborar) · 2.4 Resumo do Capítulo |
| 3. Metodologia | Descrição dos métodos utilizados, com justificativa das escolhas e discussão de alternativas |
| 4. Resultados | 4.1 Atividades do Projeto · 4.2 Requisitos do Sistema · 4.3 Desenvolvimento e Implementação · 4.4 Testes · 4.5 Análise dos Resultados · 4.6 Resumo do Capítulo |
| 5. Conclusões | 5.1 Considerações Finais · 5.2 Propostas de Continuidade |
| — | Referências Bibliográficas · Apêndices |

Os títulos de seção podem ser adaptados ao contexto do projeto (o próprio modelo autoriza isso:
*"você pode preferir usar títulos mais pertinentes ao seu contexto"*), mas **cada capítulo deve
conter os pontos listados**, mesmo que sob outro nome.

- **Resumo:** no máximo **duas páginas, no máximo dois parágrafos**: (i) objetivos do projeto e
  descrição sucinta do local onde foi desenvolvido; (ii) metodologia utilizada e resultados
  alcançados. Linguagem acessível, limitando jargões — é, junto da Introdução e da Conclusão, o
  trecho que decide se o leitor avançará no texto, então merece um esforço extra de convencimento.
- **Abstract:** tradução fiel do Resumo, nunca literal — cuidado especial com termos técnicos.

---

## 2. Precisão

- Use as palavras corretas: não escreva "redondo" se é esférico, "igual" se é aproximado,
  "sistema" se é função de transferência.
- Não use "grande", "pequeno", "máximo", "mínimo", "ótimo" sem uma escala que defina o conceito.
- Prefira números que deem noção de escala a adjetivos difíceis de precisar.
- Evite generalidades: troque *"o processo tem alto custo"* por *"o processo possui custo
  operacional X% maior que o processo Y"*.

## 3. Clareza

- **Evite frases longas.** Nunca mais de 20 palavras por frase; a média deve ficar perto de 12.
- Não deixe ideias subentendidas — explicite todos os passos do raciocínio lógico. Pular etapas
  é a causa mais comum de confusão na leitura.
- Defina todo conceito antes de usá-lo.
- Cuidado com pronomes ("esse", "este", "isso", "ele") sem referente claro — prefira repetir o
  substantivo a deixar margem para dúvida.
- Repetição de palavras não é problema em texto técnico; o que importa é a clareza, não a
  variação estilística. Se uma frase ficar confusa, repita a ideia com outras palavras ou dê um
  exemplo, em vez de tentar reformular de forma mais "elegante".
- Domine o significado de toda palavra usada — nunca use um termo sobre o qual haja dúvida.

## 4. Objetividade

- Texto direto ao ponto, sem rodeios, livre de opiniões.
- **Nunca use hipérboles.** Cuidado com "otimizar", "muito grande", "enorme", "muito bom". Use
  números para quantificar, mesmo que seja só uma estimativa — especial atenção a "muito" e
  "muitos".
- Tom impessoal, apresentando fatos, não opiniões. A voz passiva é o instrumento mais comum para
  isso em português, mas prefira a voz ativa ou a passiva sintética (*"obteve-se"*, *"optou-se
  por"*) quando possível, para manter o texto fluido.
- Prefira palavras concretas a abstratas: troque *"a máquina processou as amostras"* por *"a
  centrífuga girou as amostras"*.
- Controle o tom: sem linguagem coloquial, sem clichês, sem arrogância ("obviamente", "como é
  sabido", "é claro que").

## 5. Concisão

- Tão curto quanto possível sem perder clareza ou precisão.
- Não escreva para encher página. Se um trecho não for relevante, corte-o, mova-o para um
  apêndice ou substitua por uma referência.
- Evite redundâncias como "opinião pessoal" e "garantia absoluta".

## 6. Vícios comuns (evitar sempre)

- Estrangeirismos sem necessidade — quando usados, em itálico e com tradução entre parênteses.
- Linguagem rebuscada.
- Alternar tempo verbal entre passado e presente — escolha um e mantenha.
- Iniciar frase com verbo deixando o sujeito implícito.
- Inserir citações no meio da frase — a citação vai sempre ao final.
- Usar siglas sem defini-las por extenso na primeira ocorrência.
- "Como sabemos", "como é sabido", "por razões óbvias", "é evidente que", "talvez seja verdade
  que" — frases que só revelam que o autor não sabe explicar o que afirma.
- Definir um conceito só por meio de exemplo — primeiro defina, depois exemplifique.

## 7. Boas práticas

- Defina a estrutura do texto **antes** de começar a escrever.
- Nunca invoque um conceito antes de defini-lo; evite referências "para frente" no texto.
- Antes de um trecho longo com ideias diversas, adiante ao leitor o que será discutido; ao final,
  declare explicitamente a conclusão alcançada. Vale especialmente para seções e capítulos.
- Destaque termos novos em itálico na primeira ocorrência, como marca de definição.
- Releia a cada parágrafo; releia rapidamente cada seção para checar o encadeamento das ideias.
- Corte palavras sempre que possível.
- Use corretor ortográfico e peça para alguém ler o texto.

## 8. Uso de referências

Toda afirmação em texto técnico se enquadra em um de três casos:

- **(a)** conhecimento geral da área → em geral não precisa de citação (evite excesso; se um
  parágrafo inteiro se baseia numa referência, basta citá-la no início do parágrafo);
- **(b)** ideia original do autor → deixe isso claro no texto, para não parecer (a) ou (c);
- **(c)** origem em outro trabalho (inclusive de autoria própria anterior) → **sempre** citar.

Regras práticas:

- Nunca copie frases das referências — reescreva com suas próprias palavras; se precisar manter
  o texto original, use aspas e itálico.
- Prefira fontes com revisão por pares (artigos, livros) a teses/dissertações, depois anais de
  congresso e por último relatórios; evite páginas de internet genéricas.
- Pesquise em bases confiáveis (Web of Science, Scopus, Google Scholar), não em buscadores
  genéricos.
- Prefira referências recentes em temas de fronteira; prefira referências consolidadas (muitas
  citações) em temas já maduros.
- Evite citação de segunda mão — rastreie a fonte original sempre que possível.

## 9. Honestidade e plágio

- Nunca "maqueie" resultados nem mostre apenas as melhores amostras para parecer bem-sucedido.
- Não escreva de forma vaga para mascarar o que não foi bem compreendido.
- Dê crédito a quem o merece: toda vez que usar trabalho de terceiros, cite. Nunca assuma crédito
  pelo trabalho de outra pessoa — tem implicações legais e acadêmicas.

## 10. Gramática

- Erros gramaticais prejudicam a credibilidade do texto.
- Use a vírgula corretamente — nunca para "marcar uma pausa"; nunca separando sujeito e verbo.

---

## 11. Estrutura de parágrafo observada nos seus relatórios

Nas seções comparativas (escolha de sensores, de método de medição de torque etc.), seus
relatórios já seguem um padrão lógico consistente com as regras acima — mantenha-o:

1. **Contextualização/definição** do conceito ou componente.
2. **Princípio físico ou técnico** envolvido (lei física, equação quando aplicável).
3. **Vantagens** relevantes ao objetivo do trabalho.
4. **Desvantagens/limitações.**
5. **Conclusão parcial**, retomando a discussão e apontando a decisão ou a transição para o
   próximo tópico (ex.: *"Dessa forma, a utilização de X não se mostra adequada para a
   metodologia proposta devido a..."*).

## 12. Coesão textual

- Anáforas que retomam o substantivo da frase anterior: *"Essa abordagem..."*, *"Esse
  deslocamento..."* — mas sem abusar de pronomes ambíguos (ver Seção 3).
- Conectores lógicos variados, nunca repetidos em sequência: *"Entretanto"*, *"Dessa forma"*,
  *"Assim"*, *"Além disso"*, *"Por fim"*, *"Embora"*, *"No entanto"*, *"Uma vez que"*,
  *"Conforme"*, *"Nesse sentido"*.
- Transições entre seções recapitulam o que veio antes de introduzir o próximo passo: *"Após a
  análise comparativa dos métodos..., optou-se por..."*.
- Sigla definida por extenso só na primeira ocorrência do documento inteiro, entre parênteses:
  *"Controlador Eletrônico de Velocidade (ESC)"*.

## 13. Apresentação de resultados

- Apresente os resultados sem adulteração, com análise objetiva do que os dados mostram.
- Gráfico quando a tendência/forma importa; tabela quando os valores exatos importam ou o
  gráfico fica difícil de ler.
- Nunca inclua gráfico/tabela sem uma conclusão associada no texto.
- Sempre reporte a incerteza quando significativa (resolução do instrumento, desvio-padrão entre
  repetições etc.).
- Avalie o tamanho da amostra antes de generalizar — com poucas repetições, qualifique a
  conclusão como preliminar (caso atual da curva T×I em `Resultados.tex`, que aguarda o ensaio
  definitivo).
- Nunca termine um capítulo de forma abrupta ou genérica; o "Resumo do Capítulo" deve sintetizar
  o que foi de fato mostrado.

## 14. Unidades e notação matemática

- Todo número tem unidade. Não escreva a unidade em itálico no ambiente matemático e respeite
  maiúsculas/minúsculas (`22 kN`, nunca `22 KN`).
- Defina toda variável antes de usá-la ou imediatamente depois da equação.
- Trate equações como parte da frase, com pontuação ao final (`\enspace,` ou `\enspace.`).
- Marque definições explicitamente com `\triangleq` ou `:=`.
- Cite equações numeradas como "Equação (N)".
- Variáveis em itálico, operadores não — por isso toda expressão matemática fica no ambiente
  `$...$`, mesmo uma letra isolada.
- Nunca reaproveite um símbolo para duas variáveis diferentes no mesmo documento.

## 15. Convenções práticas do LaTeX do projeto

- Fonte **Times**, exigida pela norma do PFC/UFMG.
- Compile sempre mais de uma vez (`pdflatex` → `bibtex` → `pdflatex` → `pdflatex`, ou simplesmente
  `./compilar.sh`) para resolver referências cruzadas.
- Toda figura/tabela com `\caption` e `\label`.
- Toda referência no `.bib` citada com `\cite{}` no texto, e toda citação com entrada no `.bib`.

---

## 16. Checklist rápido antes de finalizar uma seção

- [ ] Nenhuma frase passa de ~20 palavras; a média está perto de 12?
- [ ] Toda sigla foi definida por extenso na primeira ocorrência do documento?
- [ ] Nenhuma opinião, hipérbole ou clichê — só fatos e números?
- [ ] Toda afirmação de terceiros está citada, e a citação está ao final da frase?
- [ ] O parágrafo contextualiza antes de concluir, e fecha retomando a ideia central?
- [ ] Há conectores lógicos variados amarrando as frases, sem repetição em sequência?
- [ ] Toda figura/tabela tem `\caption`+`\label` e uma conclusão associada no texto?
- [ ] O texto está impessoal (sem "eu"/"nós"), em voz ativa ou passiva sintética?
- [ ] A terminologia é consistente com o resto do trabalho (ex.: sempre "sistema de propulsão",
  "sensor ACS758", "curva característica torque versus corrente")?
