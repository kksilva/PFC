# Guia de Estilo de Escrita Técnica — Karine Giselle de Souza Silva

Este guia consolida três fontes, nesta ordem de prevalência em caso de conflito:

1. **`modelo_PFC_latex.pdf`** (nesta pasta) — o modelo oficial de monografia do curso, que
   inclui um manual de escrita técnica completo. É a **fonte normativa**: regras de precisão,
   citações, honestidade e apresentação vêm dele.
2. **O estilo efetivamente praticado** nos seus relatórios (Proposta de Projeto, Relatórios
   Parciais 1–3, Relatório Experimental) e na monografia (Introdução e Descrição do Processo),
   analisado em outubro/2026. As Seções 3, 11 e 12 deste guia descrevem esse estilo e prevalecem
   sobre as recomendações genéricas do modelo sempre que houver divergência de tom e ritmo.
3. Observações de banca/orientador, quando houver.

Use este guia ao redigir ou revisar qualquer capítulo em `PFC_monografia/`.

---

## 1. O estilo em uma frase

**Formal-técnico, impessoal e explicativo: cada parágrafo conduz o leitor do princípio físico ao
mecanismo e daí à implicação de engenharia, com períodos fluidos amarrados por conectivos e
advérbios, fechando em uma sentença de síntese.**

O texto deve ser **coeso** (as ideias se encadeiam, nada fica solto), **coerente** (conceito,
nomenclatura e linha de raciocínio consistentes do início ao fim), **fluido** (o leitor atravessa
o parágrafo sem tropeços) e **dinâmico** (o parágrafo avança: sempre sai de um estágio de
entendimento para um estágio maior).

## 2. Estrutura esperada por capítulo (conforme o modelo)

| Capítulo | Seções |
|---|---|
| 1. Introdução | 1.1 Motivação e Justificativa · 1.2 Objetivos do Projeto · 1.3 Local de Realização · 1.4 Estrutura da Monografia |
| 2. Descrição do Processo | 2.1 Processo/sistema estudado · 2.2 Instrumentação do Processo · 2.3 Situação Atual/Estado da Arte · 2.4 Resumo do Capítulo |
| 3. Metodologia | Descrição dos métodos utilizados, com justificativa das escolhas e discussão de alternativas |
| 4. Resultados | 4.1 Atividades do Projeto · 4.2 Requisitos do Sistema · 4.3 Desenvolvimento e Implementação · 4.4 Testes · 4.5 Análise dos Resultados · 4.6 Resumo do Capítulo |
| 5. Conclusões | 5.1 Considerações Finais · 5.2 Propostas de Continuidade |
| — | Referências Bibliográficas · Apêndices |

Os títulos podem ser adaptados ao contexto (o próprio modelo autoriza), mas **cada capítulo deve
conter os pontos listados**, mesmo sob outro nome.

- **Resumo:** no máximo **duas páginas, no máximo dois parágrafos**: (i) objetivos e descrição
  sucinta do local; (ii) metodologia e resultados alcançados. Linguagem acessível, limitando
  jargões — merece esforço extra de convencimento.
- **Abstract:** tradução fiel do Resumo, cuidado especial com termos técnicos.

## 3. Ritmo de frases e uso de advérbios (o seu jeito)

Esta seção codifica o estilo praticado e **prevalece sobre a regra genérica do modelo de frases
curtas**.

- **Períodos fluidos de raciocínio.** Frases que encadeiam causa e consequência podem e devem
  ter 25–35 palavras, com orações subordinadas ligadas por *"que"*, *"nas quais"*, *"de modo a"*,
  *"uma vez que"*, *"de forma que"*. O raciocínio técnico ganha naturalidade quando a relação
  lógica é feita dentro da frase. Ex.: *"A interação entre os campos gera forças eletromagnéticas
  que produzem o torque responsável pela rotação do eixo."*
- **Frases curtas para fatos e comandos.** Afirmações pontuais, valores e instruções ficam em
  frases de 8–15 palavras. Alternar período longo (raciocínio) e frase curta (fato) é o que dá
  dinamismo ao texto.
- **Advérbios são bem-vindos** quando qualificam o raciocínio, não quando embelezam: *"normalmente"*
  (condição típica), *"tipicamente"* (valor representativo), *"diretamente"* (relação sem
  intermediário), *"portanto"* (conclusão), *"assim"* (consequência), *"aproximadamente"*,
  *"usualmente"*, *"essencialmente"*, *"parcialmente"*. Proibidos os que fingem certeza sem
  base: *"obviamente"*, *"certamente"*, *"naturalmente"*, *"evidentemente"*.
- **O parágrafo fecha com síntese.** Ao final de cada bloco, uma frase-síntese curta e contundente
  declara o veredito do raciocínio: *"A aceleração, portanto, é uma consequência do torque, mas
  não é diretamente o torque."* / *"Dessa forma, a utilização de X não se mostra adequada para a
  metodologia proposta."*
- **Ponte entre blocos.** A última frase de um parágrafo prepara o próximo tópico, e a primeira
  frase do parágrafo seguinte retoma a ideia: nunca dois parágrafos começam do zero.

## 4. Arquitetura do parágrafo expositivo

Sequência padrão dos seus textos comparativos e explicativos — manter:

1. **Contextualização/definição** do conceito ou componente, com termo estrangeiro em itálico
   entre parênteses e sigla em travessão quando aplicável: *(*Electronic Speed Controller* — ESC)*.
2. **Princípio físico ou técnico**: lei física, mecanismo de funcionamento, equação numerada.
3. **Mecanismo/causa**: como o princípio se realiza no caso concreto (a sequência de eventos).
4. **Implicação de engenharia**: o que isso significa para o projeto — vantagem, limitação ou
   consequência para a escolha em discussão.
5. **Síntese ou transição** (ver Seção 3).

**Definições embutidas**: ao introduzir um termo ou valor, explique-o no próprio período com aposto
após travessão ou "é de": *"cuja constante de velocidade é de 2100 rpm/V — velocidade de rotação
aproximada do motor, em rotações por minuto por volt aplicado, em condições próximas à operação
sem carga mecânica significativa."*

**Equações** são anunciadas no texto ("satisfaz", "tem-se", "pode ser estimado por"), numeradas, e
comentadas imediatamente abaixo com *"em que $x$ é..., $k$ a..., e $c$ o..."*. Equação entra na
frase com pontuação própria.

## 5. Precisão

- Use as palavras corretas: não escreva "redondo" se é esférico, "igual" se é aproximado.
- Não use "grande", "pequeno", "máximo", "ótimo" sem uma escala que defina o conceito.
- Prefira números que deem noção de escala a adjetivos difíceis de precisar: *"o processo possui
  custo operacional X% maior que o processo Y"*.
- Qualificadores quantitativos são obrigatórios junto a advérbios como "aproximadamente": dê o
  valor ou o intervalo.

## 6. Clareza e objetividade

- Explicite todos os passos do raciocínio lógico — pular etapas é a causa mais comum de confusão.
- Defina todo conceito antes de usá-lo; nunca invoque para frente.
- Cuidado com pronomes sem referente claro — prefira repetir o substantivo (repetição não é
  problema em texto técnico).
- Tom impessoal: o sujeito é o objeto de estudo ou "o presente trabalho" — nunca "eu"/"nós".
  Prefira voz ativa ou passiva sintética (*"obteve-se"*, *"optou-se por"*).
- Sem opiniões, hipérboles, clichês ou arrogância (*"como é sabido"*, *"é claro que"*).
- Palavras concretas no lugar de abstratas: *"a centrífuga girou as amostras"* em vez de *"a
  máquina processou as amostras"*.
- Tão conciso quanto possível sem perder o encadeamento: cortar palavra morta, não conectivo que
  carrega relação lógica.

## 7. Vícios comuns (evitar sempre)

- Estrangeirismo sem necessidade — quando usado, em itálico e com tradução entre parênteses.
- Alternar tempo verbal entre passado e presente — o padrão do trabalho é o **presente**.
- Iniciar frase com verbo deixando o sujeito implícito.
- Citação no meio da frase — a citação vai sempre ao final, antes do ponto:
  *"... estimado a partir da aceleração \cite{mascarenhas2006}."*
- Sigla sem definição por extenso na primeira ocorrência do documento inteiro.
- Definir conceito só por exemplo — primeiro defina, depois exemplifique.
- Duas frases-síntese consecutivas, dois conectivos iguais em sequência, ou parágrafos que
  começam todos com a mesma construção (monotonia destrói a fluidez).

## 8. Coesão textual

- Anáforas que retomam o substantivo: *"Essa abordagem..."*, *"Esse deslocamento..."*.
- Conectivos variados, amarrando causa, contraste, adição e conclusão: *"Além disso"*, *"Além de"*,
  *"Dessa forma"*, *"Assim"*, *"Por isso"*, *"Portanto"*, *"Entretanto"*, *"Embora"*,
  *"Uma vez que"*, *"Conforme"*, *"À medida que"*, *"Nesse contexto"*, *"Nesse sentido"*,
  *"De modo a"*, *"De forma que"*, *"Por fim"*.
- Transição de seção recapitula antes de avançar: *"Após a análise comparativa dos métodos de
  medição, optou-se por..."*.
- Nomenclatura consistente do início ao fim: sempre "sistema de propulsão", "curva característica
  torque versus corrente", "sensor ACS758" (não variar sinônimos para o mesmo objeto).

## 9. Boas práticas

- Defina a estrutura do texto **antes** de começar a escrever.
- Antes de um trecho longo, adiante ao leitor o que será discutido; ao final, declare a conclusão
  alcançada.
- Destaque termos novos em itálico na primeira ocorrência, como marca de definição.
- Releia a cada parágrafo; releia cada seção para checar o encadeamento.
- Use corretor ortográfico e leia em voz baixa os trechos críticos — a fluidez se testa no ouvido.

## 10. Uso de referências

Toda afirmação se enquadra em três casos: (a) conhecimento geral → sem citação (evite excesso);
(b) ideia original → deixe claro no texto; (c) origem em outro trabalho → **sempre** citar.

- Nunca copie frases das referências — reescreva com suas palavras.
- Prefira revisão por pares > teses > anais > relatórios > páginas genéricas.
- Pesquise em bases confiáveis (Google Scholar, Scopus, Web of Science).
- Evite citação de segunda mão — rastreie a fonte original.
- Datasheets e manuais são citáveis pelo fabricante: *"Segundo o manual do fabricante..."*
  com entrada no `.bib`.

## 11. Honestidade

- Nunca maqueie resultados nem mostre só as melhores amostras.
- Não escreva de forma vague para mascarar o que não foi compreendido — descreva a limitação.
- Com poucas repetições, qualifique a conclusão como preliminar.

## 12. Gramática

- Erros gramaticais prejudicam a credibilidade.
- Vírgula nunca separa sujeito e verbo, nem "marca pausa"; travessão introduz aposto explicativo.
- Decimal com vírgula: 0,08 m; 2100 rpm/V.

## 13. Apresentação de resultados

- Sem adulteração, com análise objetiva do que os dados mostram.
- Gráfico quando a forma importa; tabela quando os valores exatos importam.
- Nunca figura/tabela sem conclusão associada no texto — toda figura encerra com uma frase do
  tipo *"Observa-se que..."* que extrai o que a figura prova.
- Sempre reporte incerteza quando significativa (resolução, desvio-padrão entre repetições,
  incerteza expandida).
- Nunca termine capítulo de forma abrupta: o "Resumo do Capítulo" sintetiza o que foi de fato
  mostrado.

## 14. Unidades e notação matemática

- Todo número tem unidade, sem itálico, maiúsculas/minúsculas corretas (`22 kN`, nunca `KN`).
- Defina toda variável antes de usá-la ou imediatamente depois da equação.
- Equações como parte da frase, com pontuação.
- Definições com `\triangleq`; equações citadas como "Equação (N)".
- Variáveis em itálico via ambiente matemático, operadores em romano.
- Nunca reaproveite símbolo para duas variáveis diferentes no documento.

## 15. Revisão: lições práticas (outubro/2026)

Lições extraídas das rodadas de revisão da autora sobre o Capítulo 2:

- **Um símbolo, um significado, em todo o documento — e a checagem é grep, não memória.**
  $T_m$ como duração da janela de contagem colidia com $T_m$ = torque do motor nas equações
  vizinhas: o olho leu torque, não tempo. Convenção adotada: janela de contagem é $T_j$;
  subscritos sempre semânticos e únicos. Antes de fechar um capítulo, varrer o `.tex` pelos
  símbolos usados e conferir colisões entre seções, não apenas dentro delas.
- **Perguntas entre parênteses são marcações de revisão, não texto.** Responder uma pergunta
  como "(e por quê é indireta?)" ou "(solitário?)" é reescrever a passagem de modo que a dúvida
  desapareça e então apagar a pergunta. A versão final nunca carrega parêntese de dúvida.
- **Quando a conclusão não é óbvia, mostre a cadeia causal em vez de afirmar.** "A relação é
  indireta" só convence se o texto desenhar a cadeia: causa (torque do motor) → efeitos
  intermediários (tração na roda, perdas de transmissão e resistências) → grandeza medida
  (aceleração líquida). Afirmações avaliativas ("indireto", "grosseiro", "sensível") exigem o
  encadeamento explícito logo no parágrafo em que aparecem.
- **Alternativas rejeitadas recebem detalhe mínimo.** A revisão removeu as equações do filtro
  complementar e o parágrafo dos coxins de borracha da IMU: o que não muda a decisão entre
  alternativas não precisa de equação numerada nem de parágrafo próprio. Em comparação de
  alternativas, o essencial é princípio → o que mede → o que falta para o objetivo → veredito.
- **Registro formal sem exceção, inclusive nas revisões rápidas.** "Pra" → "Para a"; nomes
  próprios conferidos letra a letra (Raspberry Pi). Coloquialismo e nome próprio errado passam
  despercebidos na tela do editor e saltam aos olhos no PDF.
- **Palavras que se parecem, mas não são.** "solidário" (rigidamente acoplado, gira junto) ≠
  "solitário". Quando o termo técnico tem um vizinho comum no vocabulário, a definição
  embutida com travessão elimina a ambiguidade na primeira ocorrência.

## 15a. Lições da construção dos Caps. 2 e 3 (outubro/2026)

- **Número aparece uma vez só.** Valor novo entra na tabela ou na figura; a prosa discute
  padrões, regiões e interpretações — nunca reenumera. Se o número precisa voltar a aparecer,
  o texto está mal organizado, não faltando dado.
- **Conceitos-chave são nomeados uma vez e depois usados pelo nome.** Regiões de operação
  (zona morta, região de aderência, região de saturação), modos de ensaio (ensaio em vazio,
  ensaio de tração estática) e instrumentos são definidos com nome e limites na primeira
  ocorrência; daí em diante o texto trabalha com o nome. Faixas numéricas repetidas em cada
  parágrafo = sinal de que falta o conceito que as resume.
- **Explicações didáticas entram como frase de apoio no fluxo, não como parágrafo de aula.**
  r², η, regressão sem intercepto, stick-slip, método da 63,2%: uma frase curta no ponto da
  primeira ocorrência, amarrada ao que está sendo mostrado — *"o coeficiente de determinação
  r², fração da variância dos dados explicada pelo ajuste"*. Detalhamento longo vaza o ritmo.
- **Capítulo de Metodologia organizado por experimento, não por disciplina.** Cada ensaio com
  o mesmo template de blocos, na mesma ordem: **Definição e objetivo → Configuração →
  Checklist pré-ensaio → Procedimento (passo a passo numerado) → O que fornece**. O leitor
  sabe onde encontrar cada elemento em qualquer ensaio; a infraestrutura comum (montagem,
  cadeia de aquisição) fica numa seção inicial, descrita uma única vez e referenciada.
- **Capítulo de Resultados espelha a ordem dos experimentos da Metodologia.** O leitor
  atravessa os dois capítulos no mesmo ritmo; cada seção de resultado abre com o que o ensaio
  prometia e fecha com o que entregou.
- **Seções de sensor seguem o template da 2.2.1**: definição (nome por extenso entre
  parênteses + sigla) → fixação no veículo → equações da cadeia (cada uma anunciada por frase
  curta: "Pela Lei de Ohm...", "a segunda lei de Newton resulta em") → aplicação em malha
  fechada (o que a grandeza viabiliza como realimentação) → veredito ("Dessa forma...") →
  "Em síntese, a utilização do X apresenta vantagens e limitações:" → itemize com
  `\textbf{Vantagens:}` / `\textbf{Limitações:}`. O veredito vem **antes** da enumeração, e a
  seção fecha no itemize.
- **Seção de Proposta contém proposta, não resultados.** Nada de valores identificados,
  equações com parâmetros ajustados, ganhos de controlador ou menções a trabalhos externos —
  a proposta diz o quê e para quê; o como fica na Metodologia, o quanto fica nos Resultados,
  o controlador fica no Capítulo 5. Parâmetros aparecem como "a determinar experimentalmente".
- **Aferições são relatadas com sua repetição.** "Medido três vezes; o valor adotado é a média
  das três leituras" — toda dimensão, pesagem e leitura de calibração carrega a multiplicidade.
- **Atribuições em forma acadêmica impessoal.** "disponibilizado pelo orientador" /
  "desenvolvido no âmbito deste trabalho" — crédito claro sem quebrar o registro.
- **Não afirmar além dos dados recebidos.** Se a conclusão não decorre dos dados da autora, o
  texto hedged ("é compatível com", "a interpretação mais plausível é") ou silencia.
  Interpretações e consequências (o que os resultados implicam para o controlador, hipóteses
  de causa, discussão com a literatura) pertencem à **Conclusão**, não ao corpo de Resultados —
  onde só vive o que foi medido. Afirmar causa sem instrumentação (ex.: memória térmica vs.
  bateria aquecida) é atacável em banca; apresentar a alternativa e o que a separaria é defensável.
- **Aprovado é congelado.** Texto que a autora revisou e manteve não se reescreve — nem para
  "melhorar". Melhorias só respondem a perguntas dela, corrigem erro ou consertam coesão com o
  restante. A revisão dela tem prioridade sobre qualquer sugestão de estilo deste guia.
- **Perguntas entre parênteses DELA são pedidos, não dúvidas dela.** "(o que é isso?)",
  "(qual motivo?)", "(como assim? explique)" pedem que o assistente esclareça reescrevendo a
  passada com a explicação embutida — e apague a pergunta.
- **Ela poda o fim de frases longas.** Quando o raciocínio estende o período além do
  necessário, ela corta o rabo da frase em vez de repartir. Revisar imitando: encurtar o
  fecho, não alongar o meio.
- **Títulos de seções compostas usam "+"**: "Shunt Resistivo + Amplificador de
  Instrumentação", não "e".
- **Parágrafos curtos com respiro**: blocos de 3–6 linhas separados por linha em branco;
  um bloco, uma ideia.
- **Equações entram com anúncio simples**: "a Segunda Lei de Newton para rotação ..., é dada
  por:" — dois-pontos, sem cerimônia.
- **Poucos dois-pontos, poucos ponto e vírgula, poucos travessões.** A autora reclamou do
  excesso (revisão do Shunt/SS41F): travessão é para aposto explicativo pontual, não para toda
  explicação; dois-pontos anunciam raramente, preferindo-se o período; ponto e vírgula vira
  ponto quando a oração for longa. Variação de pontuação é parte do ritmo.
- **Citações fora por decisão da autora: escrever primeiro, `\cite` depois, numa rodada única.**
  Texto novo nasce sem `\cite`; frases que dependerão de fonte ficam impessoais e completas
  sem a atribuição formal.

## 15b. Convenções LaTeX duras (quebram silenciosamente se esquecidas)

- **Acentos em modo matemático**: `\mathrm{tração}` e `\text{tração}` perdem o `ç`/`ã` no PDF
  ("Ftrao"). Forma que funciona neste template: `F_{\text{tra\c{c}\~{a}o}}`. Escapes: ç =
  `\c{c}`, ã = `\~{a}`, õ = `\~{o}`, á/é/í = `\'{a}` etc.
- **Ambiente de lista correto**: `\begin{item}` não existe — compila em nonstopmode sem
  bullets, sem erro aparente. `itemize` (sem ordem) ou `enumerate` (passo a passo, sequência
  do sinal).
- **Fonte de figura em forma ABNT curta**: `\footnotesize{Fonte: Autor (ano).}` — sem URL na
  figura; o link completo vai em entrada `@misc` no `.bib` (como `ti_ina240_2`), citada na
  rodada de referências.
- **Splice de seções por script**: ao remendar `.tex` com `re.subn`, usar função de reposição
  (valor literal) — string de reposição processa escapes e duplica as barras.

## 16. Convenções LaTeX do projeto

- Fonte Times (norma PFC/UFMG); `book` 12pt, `abntex2`.
- Compile com `./compilar.sh` (ou `pdflatex` → `bibtex` → `pdflatex` ×2).
- Toda figura/tabela com `\caption` + `\label`; fonte da figura indicada em `\footnotesize`.
- Toda entrada do `.bib` citada no texto; toda `\cite` com entrada no `.bib`.

---

## 17. Checklist rápido antes de finalizar uma seção

- [ ] Cada parágrafo segue contextualização → princípio → mecanismo → implicação → síntese?
- [ ] Os períodos longos carregam raciocínio encadeado e as frases curtas, fatos? (ritmo fluido)
- [ ] Advérbios qualificam condições e conclusões (normalmente, tipicamente, portanto, diretamente) — sem "obviamente/evidentemente"?
- [ ] Cada bloco fecha com frase-síntese e abre ponte para o próximo?
- [ ] Toda sigla definida por extenso na primeira ocorrência do documento?
- [ ] Citações ao final das frases; citações de terceiros em todo conceito que não é seu?
- [ ] Terminologia consistente do início ao fim?
- [ ] Toda figura/tabela com `\caption`+`\label` e conclusão associada no texto?
- [ ] Impessoal, presente do indicativo, sem hipérbole ou coloquialismo?
- [ ] Incertezas reportadas junto aos resultados?
