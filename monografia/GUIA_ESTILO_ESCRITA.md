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
- **Proibida a acumulação de ideias por vírgulas sem conectivo.** Quando uma frase junta
  três ou mais ideias apenas com vírgulas ("a corrente gera um campo perpendicular proporcional
  tensão desenvolvida e, portanto, à corrente medida"), cada vírgula esconde uma relação lógica
  que a língua portuguesa explicita com conectivo: *"que"*, *"e esse"*, *"de modo que"*,
  *"pois"*, *"sendo"*, *"o que"*, *"de forma que"*, *"porque"*. Uma frase sua carrega 2–4
  ideias, mas cada elo diz de que tipo é a ligação — causal, consecutiva, explicativa ou
  simples adição. Este é o padrão dos trechos que a autora marca como confusos: não é a
  ideia, é a vírgula fazendo o papel de conectivo. Ex. de transformação — antes:
  *"a corrente percorre um condutor interno gera um campo magnético perpendicular proporcional
  tensão desenvolvida e, portanto, à corrente medida"* — depois: *"a corrente que percorre o
  condutor interno gera um campo magnético perpendicular, e esse campo desenvolve uma tensão
  proporcional, de modo que a tensão de saída reproduz a corrente medida"*. Se a frase
  estoura quatro ideias mesmo com conectivos, parte-se em duas.
- **Proibida a frase-solta que só anuncia.** Uma frase curta cujo único papel é
  anunciar o que vem a seguir ("O benefício é duplo.", "O procedimento é o seguinte.",
  "A Tabela X consolida os dados.") quebra o encadeamento. A informação do anúncio entra
  fundida ao período seguinte com conectivo ("...e, com isso, a roda não patina, pois...").
  Cada ideia tem início, meio e fim dentro do fluxo, com conectivos, não em letreiro
  separado.
- **Proibida a clívula enfática "é ... que" para ideias correntes.** "Na realimentação,
  é contra ela que o torque estimado é comparado" vira "na realimentação, o torque
  estimado é comparado a ela". A construção "é ... que" fica para ênfases realmente
  contrastivas, uma por capítulo no máximo.
- **Proibida a sequência de frases curtas que carrega raciocínio.** Quando duas ou três frases
  seguidas de menos de 15 palavras estabelecem relação de causa, consequência ou qualificação,
  elas devem ser fundidas em um único período conectado, com *"que"*, *"pois"*, *"sendo"*,
  *"o que"*, *"de modo que"*, *"na qual"*. Frase curta isolada é recurso; sequência de frases
  curtas é telegrafia. Ex. de transformação — antes: *"A força passa, então, a depender apenas
  do torque do motor, e este, da corrente. É a única região em que o modelo é válido e a
  dinâmica identificada representa a planta. Todo o projeto do controlador se apoia nela."* —
  depois: *"A força passa, então, a depender apenas do torque do motor, que por sua vez decorre
  da corrente, sendo essa a única região em que o modelo é válido, a dinâmica identificada
  representa a planta e todo o projeto do controlador se apoia."*
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
- **Frase pontual de sinalização é proibida.** Construções como *"A primeira é direta."*,
  *"A segunda é estrutural."*, *"O primeiro é o estimador."* — frases-carteiro que só
  anunciam e não informam — destroem o ritmo. O conteúdo delas entra dentro de um período
  corrido, amarrado pelo conectivo. Frase curta é para fato e valor medido
  (ver Seção 3), nunca para letreiro de parágrafo.
- **Proibição total de ponto e vírgula e de dois-pontos no texto do assistente.** Regra
  da autora (28/10, segunda reclamação): o assistente não usa ";" nem ":" em nenhuma
  situação. Onde o raciocínio pediria ";", se parte a frase em duas. Onde pediria ":",
  reestrutura-se com vírgula, "resulta em", "é" ou período novo. Equação anunciada com
  verbo ("resulta em", "é dada por" seguido de vírgula e equação na linha própria), sem
  dois-pontos. Quando a autora mesma mantiver ":" em texto dela, isso é escolha dela e
  não licença para o assistente.
- **Teto de comprimento de frase.** Períodos de raciocínio no máximo ~30 palavras. Acima
  disso, dividir em duas, retomando o sujeito. O assistente tende a estender o período com
  oração após oração; a autora prefere duas frases médias a uma frase longa. (O ritmo
  fluido da Seção 3 se faz com períodos de 15–30 palavras alternados com fatos curtos,
  nunca com períodos de 40+.)
- **Cota de conectivos e advérbios.** Repetição de conectivo é vício detectado em revisão
  (28/10): "assim" no máximo uma vez por seção; nunca o mesmo conectivo em parágrafos
  adjacentes; nunca dois advérbios conectivos na mesma frase ("de modo que", "uma vez
  que", "de forma que", "dessa forma", "assim" competem pela mesma vaga — usar um só, e
  variar o próximo). Antes de entregar um texto, varrer as ocorrências de cada conectivo
  por seção e reescrever as repetições com pontuação simples (vírgula, ponto) ou com
  conector de outra família (adição, contraste, causa, tempo).
- **Redundância entre frases vizinhas.** Se a frase seguinte repete a anterior com outras
  palavras, fundir ou cortar. Cada informação entra uma vez no capítulo (ver "número
  aparece uma só vez"); o mesmo vale para ideias — o parágrafo de resultado não repete o
  de método com sinônimos, ele avança.
- **Redundância entre capítulos é proibida — cada conteúdo tem um dono.** Fato, derivação,
  justificativa e número vivem em exatamente UM capítulo; os demais referenciam
  (Capítulo X, Seção Y) em vez de repetir. O mapa de propriedade é:
  - **Cap 2** — teoria, fundamentos, definições, estrutura de controle, proposta (o quê e
    para quê, sem valores identificados, sem ganhos);
  - **Cap 3** — como os experimentos foram feitos (montagem, protocolo, instrumentos,
    derivações das componentes de incerteza);
  - **Cap 4** — o que foi medido e ajustado (números, regressões, ganhos, simulação),
    sem reexplicar protocolo (referencia a Metodologia), sem interpretações que
    pertencem à Conclusão; a teoria do controlador referencia o Cap 2, e o Cap 4 cuida
    apenas das escolhas numéricas e do desempenho;
  - **Cap 5** — interpretações, consequências, continuidade.
  Sintoma típico a varrer: parágrafo de papel/motivação de ensaio idêntico em Metodologia
  e Resultados (fica em Metodologia; Resultados abre com o que o ensaio entregou);
  explicação de I₀, cascata, feedforward ou inferencial aparecendo nos dois capítulos
  (fica no Cap 2; Cap 4 referencia); número canônico citado em mais de um lugar (fica no
  resultado que o produz, ou na tabela).
- **Cada seção de sensor define a malha de controle completa, no padrão da IMU.** Variável de
  processo, variável manipulada e como a malha fecham, em parágrafo próprio antes do veredito.
  Comparação de sensores não antecipa decisão do trabalho: modo de medição, calibrações e
  adoções vivem na Metodologia; a seção de sensor é imparcial até o veredito.
- **Tom formal sem solas conversacionais.** Evitar construções como "A malha fecha
  comparando...", "assim como na solução com...", sequências de frases curtas soltas e
  explicações em estilo de conversa. Preferir o indicativo com subordinação ("A malha compara
  ... e ajusta ..."), "como no arranjo com..." e períodos que amarram as ações. O texto da
  autora soa acadêmico, nunca didático-conversado.
- **O controlador vive no Capítulo 4 (Resultados), não na Conclusão.** Teoria (PI, IMC),
  estrutura, justificativas e valores na seção de malha de controle; a Conclusão discute
  consequências e remete.
- **Padrão do leitor leigo (auditoria 27/10): cada termo na primeira ocorrência leva a frase
  de apoio embutida** (duty cycle, platô, armado, 63,2%, sensorless, anti-windup, histerese,
  K_v); **cada número leva referencial prático** (0,25 s está na faixa elétrica da
  literatura; r² = 0,962 significa 96% da variância explicada); **cada dedução fecha todos os
  elos** (por que a roda travada faz a corrente determinar a força; por que μ = 0,80 exige
  transferência de carga; por que o intercepto é proibido). Figura citada = leitor guiado
  sobre o que olhar + frase-síntese do que ela prova.
- **Citações fora por decisão da autora: escrever primeiro, `\cite` depois, numa rodada única.**
  Texto novo nasce sem `\cite`; frases que dependerão de fonte ficam impessoais e completas
  sem a atribuição formal.

## 15d. Lições da rodada de dúvidas do Cap. 4 (29/10)

- **Razão ou porcentagem citada carrega os operandos.** "(DE ONDE VEIO 7%? DE ONDE VEIO 45%?)"
  toda razão citada volta com a operação que a gerou — "+45%, em 110°, onde o quociente
  47,18/32,52 = 1,45" — e não solta. A regra do número único se estende: quando o número
  retorna, retorna com a conta, apontando para a tabela que fornece os operandos.
- **Conceito usado em mais de um capítulo é definido uma vez, com label, e citado depois.**
  "(ESPERO QUE TENHA CITADO ANTERIORMENTE...)" — u = (α − 95)/85 nasce na metodologia com
  `\label{eq:normalizacao}` e, no Cap. 4, aparece como "conforme a
  Equação~\eqref{eq:normalizacao} da metodologia". Nunca redefinir, nem repetir a fórmula.
- **Frase de validação nomea o que se valida, as variáveis e o como.**
  "(EXPLIQUE O QUE É VALIDADO, QUAIS SAO AS VARIAVEIS E COMO COMPROVA)" — o template é
  "valida-se X contra Y, medido por Z, e a evidência é W", com remissão à seção da
  metodologia que define o ensaio. "Cruza as duas fontes de dados" sem esse esqueleto é
  opaco para o leitor.
- **ABNT não prescreve tempo verbal.** "(NO PASSADO MESMO? O QUE DIZ A ABNT?)" — a NBR
  14724 não regra tempo; o presente do indicativo é o padrão do trabalho (Seção 7), e o
  Cap. 4 o mantém ("observa-se", "a força cresce").
- **Observação sem medição entra declarada como observação.** "(ADICIONAR QUE A BATERIA
  DESCARREGOU MAIS RAPIDO — NAO FOI MEDIDO)" — a forma é "registra-se como observação, sem
  medição dedicada, que...", o que registra o fato sem inventar dado (Seção 11).
- **Comentário que pede resposta no chat é comentário que pede resposta no chat.**
  "(ME RESPONDA NO CHAT SE TEMOS OUTROS DADOS...)" — distinguir dos pedidos de reescrita:
  pergunta informacional/conceitual é respondida no chat, com nenhum ou mínimo ajuste no
  texto; só dúvida de entendimento do texto reescreve a passagem.
- **Causa atribuída a equipamento comercial pede verificação no documento do fabricante.**
  "(NAO É SOBRE? PESQUISE ISSO NO MANUAL DESSE ESC)" — identificar o equipamento pelo
  modelo (Team Orion Vortex R8, conforme a ficha do fabricante) e citar a função; quando o
  manual é escaneado e a especificação não é extraível, declarar a evidência indireta (o
  comportamento cíclico observado) em vez de afirmar limiar não verificado.
- **Duas rodadas separadas: reescrita primeiro, auditoria depois.** A rodada que atende
  comentários reescreve e completa mantendo a estrutura e o tom da autora; a auditoria de
  ortografia e gramática é rodada posterior, com artifícios de fluidez, coesão e
  coerência. Não misturar as duas numa única passada.
- **Salvamento concorrente do editor sobrescreve o disco.** A autora edita no VS Code
  enquanto o assistente edita os mesmos arquivos; um "salvar" dela reverte as correções.
  Antes de cada rodada, comparar o arquivo com o espelho git (`diff`) para detectar
  overwrite; ao final, avisá-la para fechar e reabrir o arquivo antes de continuar.

## 15c. Vícios do assistente identificados nas correções da autora (28/10)

Lições extraídas do diff entre o texto gerado pelo assistente e as correções manuais da
autora. Cada item traz o exemplo real (meu → dela).

- **Proibição de meta-discurso.** O assistente anuncia o que vai fazer em vez de fazer:
  *"Convém explicitar por que a análise ocupa dois scripts e não um por ensaio: a divisão
  segue..."* → *"A divisão segue os modelos que o controlador consome, assim,..."*. Proibido
  escrever sobre o texto ("convém registrar", "merece destaque", "cabem aqui", "importa
  notar"). A informação entra direta, sem cerimônia de apresentação.
- **Sem frase-tópico que rotula o parágrafo.** *"A motivação da estrutura é proteger o
  processo sem desligar o controle."* — a autora apagou. O parágrafo começa no conteúdo,
  não num letreiro do que ele vai argumentar.
- **Sem fecho elaborado ou metafórico.** *"Como cada modelo sustenta um elo da malha,
  reproduzir os scripts é reproduzir a cadeia que sustenta o controlador."* — a autora
  podou. Fecho é declaração simples do que ficou estabelecido, sem floreio nem rima
  interna. O assistente tende a terminar parágrafos com uma frase de efeito; ela termina
  com o fato.
- **Sem exagero de consequência.** *"segui-la destruiria o equipamento"* → *"segui-la pode
  causar danos ao equipamento"*. O assistente radicaliza verbos; a autora hedges. Toda
  consequência física sem instrumentação vai no condicional ou no "pode".
- **Atribuição uma vez só.** *"realimentação das notas de aula, o controlador..."* →
  *"realimentação, o controlador..."*. Depois de citado e definido o conceito, o texto usa
  o conceito diretamente. O assistente re-ancora a fonte a cada ocorrência; a autora
  ancora uma vez e segue.
- **Sem ilustração de terceiros quando o próprio sistema ilustra.** O parágrafo do exemplo
  do reator (slide do Raffo) foi removido. Explicação didática boa é a que usa o próprio
  automodelo como caso; exemplo alheio vira aula solta e sai.
- **Redundância de qualificadores.** *"a referência pedida"* → *"a referência"*;
  *"a validação depende desse desconto"* → *"a validação é dependente"*. O assistente
  empilha sinônimos e apostos; cada palavra que não desambigua é cortada.
- **Subscrito sempre semântico, nunca abreviado.** $T_{\mathrm{ader}}$ →
  $T_{\mathrm{aderência}}$. A regra de símbolo único se estende: subscrito abreviado que
  exige decodificação vira palavra inteira (aderência, repouso, tração).
- **Conectivos da autora, em ordem de preferência observada:** "assim," (consequência
  imediata), "Em compensação," (o custo do benefício), "Aqui" (mudança de caso dentro do
  mesmo assunto), "Nesse caso", "Dessa forma", "Contudo". O assistente sobrecarrega "de
  modo que" e "uma vez que"; ela os converte em "assim," + vírgula ou em ponto.

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
- [ ] Nenhuma frase pontual de sinalização ("A primeira é direta.")? Todas absorvidas em períodos corridos?
- [ ] Nenhum ";" e nenhum ":" no texto gerado? Frases com teto de ~30 palavras?
- [ ] Nenhum conectivo repetido em parágrafos adjacentes ("assim" no máx. 1 por seção)? Nenhuma ideia repetida entre frases vizinhas?
- [ ] Os períodos longos carregam raciocínio encadeado e as frases curtas, fatos? (ritmo fluido)
- [ ] Advérbios qualificam condições e conclusões (normalmente, tipicamente, portanto, diretamente) — sem "obviamente/evidentemente"?
- [ ] Cada bloco fecha com frase-síntese e abre ponte para o próximo?
- [ ] Toda sigla definida por extenso na primeira ocorrência do documento?
- [ ] Citações ao final das frases; citações de terceiros em todo conceito que não é seu?
- [ ] Terminologia consistente do início ao fim?
- [ ] Toda figura/tabela com `\caption`+`\label` e conclusão associada no texto?
- [ ] Impessoal, presente do indicativo, sem hipérbole ou coloquialismo?
- [ ] Incertezas reportadas junto aos resultados?
