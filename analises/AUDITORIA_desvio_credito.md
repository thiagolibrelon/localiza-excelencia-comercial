# Auditoria — Desvio de política de crédito (risco de compliance)

**Por que este arquivo existe:** duas explorações independentes (lotes diferentes, dias diferentes, prompts diferentes) encontraram o MESMO padrão: vendedor orientando o cliente a contornar o limite de crédito aprovado, estruturando o contrato de um jeito que "não é lido" pelo sistema de crédito. Isso não é comportamento comercial — é risco de compliance. Separado aqui pra revisão própria do jurídico/risco, fora do fluxo normal de treinamento de vendas.

**Status:** 2 casos confirmados, ambos no novo lote (5.348 ligações). Não fizemos busca sistemática na base inteira — isso é uma amostra que apareceu em 2 de 16 lotes explorados (12,5%), o que sugere que pode haver mais casos não descobertos.

---

## Caso 1 — Cliente 12936013

- **segment_id:** `46f31ecb-0894-4241-9382-81d202cbae6f`
- **Data:** 2026-06-16 · **Duração:** 686s
- **Vendedora:** Andressa ("André" nas falas, provavelmente erro de STT)
- **Padrão:** crédito de R$100 mil reprovado; vendedora orienta pedir R$80 mil com justificativa, envolvendo a supervisora, e ensina o workaround de converter reserva diária em mensal "porque aí não lê o crédito".

### Transcrição completa

**C:** Alô?
**A:** Oi, Luiz, bom dia.
**A:** Tudo bem?
**C:** dia, André. Beleza?
**A:** Tudo bem?
**C:** Olha,
**A:** Tudo bem por aqui.
**C:** André, eu
**A:** Sério,
**C:** fico olhando... Olha, o seu número é só ele que está respondendo que você me liga. Só o que
**A:** cai na caixa... Será que está
**C:** É...
**A:** no spam? Será que está no spam? Porque eu ligo... Como eu ligo de PABX, pode
**C:** rapaz.
**A:** isso. Está caindo no spam. Porque eu ligo de vários números. A localiza tem um número central, né?
**C:** Uhum. Uhum. Ué, fala aqui aí, Santana? Porque... Ué, todo mundo liga. Eu fiz o teste aqui do pessoal ligando outros certos falando assim... Então deve ser isso então, Andrinha.
**A:** Entendeu? Provavelmente deve ser isso. Luiz, é o seguinte, não tem uma notícia muito boa,
**C:** que foi?
**A:** a gente está vendo aqui o que acontece. É assim, o time de crédito fez aquela análise lá da... da documentação, consultou o Banco Central e aí assim, a localiza não aprovou os 100 mil. A gente não conseguiu aprovar. Aí eu mandei uma outra justificativa para o time, porque assim, quando acontece isso, eles consultam os bancos. E se a BTEC tiver algum perfil em alguma coisa nesse sentido, até no nome do sócio isso impacta. Agora... O que eu fiz uma justificativa aqui para eles? Falei, olha, então tá bom, a gente não conseguiu liberar 100 mil, mas a gente precisa pelo menos de 80. Que aí foi o que eu pedi aqui para eles. Aí fiz uma outra justificativa incluindo aqui minha supervisora no circuito para ver se eles flexibilizam. Só que assim, o time de crédito tem uma análise que eles fazem e tem que ter umas cumprir umas regras lá. Então você sabe, a gente sabe que às vezes a empresa acontece de ter uma restrição ou no cpf do sócio ou na própria... Alguma situação que está na justiça e aí impacta, sabe? Mas eu estou correndo atrás aqui,
**C:** Uhum.
**A:** porque se não, o que vai acontecer? O que vai acontecer? Vai acontecer aquela situação que a gente está vivendo. Exemplo. Tem uma, duas faturas que vão vencer no dia 26 do 6 e uma que vai vencer no dia 27 do 6. Então vamos supor que as três ali vencem no dia 26 do 6, porque duas vencem no dia 26 do 6 e uma no dia 27
**A:** do 6. Ali
**C:** Uhum.
**A:** tem quase R$6 mil, né? Só que o que aconteceu Eu com com vocês. vocês? Como você tem muito carro na rua, né, utilizando, o que acontece? Você fica com uma restrição assim, ó. Na localiza, quer ver? Fica mais fácil para explicar. Compromete o crédito dos carros que você está usando em utilização. Então, por exemplo, contratos abertos têm mais ou menos... 33 mil de carro em utilização. Financeiro a pagar quase 26 mil 830. Então, quando você paga essas faturas, o crédito volta. E aí esses contratos que você está utilizando não tem como a gente recuperar esse valor porque está em utilização. Deu para entender?
**C:** Entendi, entendi, porque o...
**A:** Entendeu? Então, assim... A única forma que a gente tem,
**A:** caso eu estou pedindo
**C:** vou colocar um todo
**A:** aqui,
**C:** o sonho.
**A:** vou aguardar
**C:** Então,
**A:** fazer mais uma
**A:** tentativa.
**A:** única forma
**C:** mais um...
**A:** que a gente tem é o seguinte, é ir pagando as faturas para liberar. Então hoje, por exemplo, aqui ó, eu estou te
**A:** mandando aqui no WhatsApp
**C:** que ir embora? Tem que ir embora?
**A:** Olha como é que está a situação hoje da BTEC aí, de contratos
**A:** abertos e
**C:** que ir aqui?
**A:** de financeiro. O
**A:** ideal seria,
**C:** vou ligar
**C:** aqui.
**A:** Porque
**A:** aqui
**C:** ligar
**A:** você
**C:** aqui.
**A:** tem... Vamos olhar aqui certinho.
**C:** Ainda é
**A:** Vamos
**C:** tudo
**C:** isso.
**A:** aqui. Hoje você tem 50 mil e está comprometido 60. Então tem 10 mil comprometido. Tem que pagar 10 mil em fatura para liberar ali.
**A:** Sim.
**C:** entendi, eu só não entendi o seguinte, hoje eu tenho 11 carros locados, 11 carros, né? 11 carros, eu não tenho fatura em atraso e
**A:** Não, mas as faturas não é vencer, compromete o crédito, entendeu? Não é fatura vencida. É fatura a vencer, contratos em utilização. Deu para entender?
**C:** entendi
**A:** Só que aqui,
**C:** um exemplo
**A:** agora a gente tem uma...
**C:** Por exemplo, eu tenho 11 contratos. Vamos pôr aí um contrato pelo outro a 3 mil e... Vamos pôr aí um contrato pelo outro a 3 mil e... Vamos pôr aí Vamos pôr 3.200.
**A:** Não, está dando ali, ó... Ali está dando contratos abertos. Está dando 33.775-41,
**C:** Pois
**A:** são os
**C:** então,
**A:** carros
**A:** que...
**C:** que eu estou falando. Eu tenho 11 carros. Então eu fiz a conta certa, mais ou menos. 11 carros, né? 11 carros está dando 33 mil. Beleza. Eu não tenho fatura vencida e por que está dando esse negativo?
**A:** Mas aí a localiza compromete faturas a vencer. Quando que eu comprometo o crédito? Fatura vencida e fatura a vencer. Aquilo que vai vencer compromete. Tanto que aqui, dívida no financeiro, 26 mil 830 é o que vai vencer. Agora eu tenho uma solução, tá?
**C:** Pois é,
**A:** te falar
**C:** vencer, ela
**A:** isso aqui.
**C:** vai vencer.
**A:** Mas aí compromete, é compromete compreendida localiza e compromete o que vai vencer
**A:** e o que está vencido.
**C:** não tem vencido?
**A:** Então, eu sei, mas o que vai vencer comprometeu R$ 26.830. O que vai vencer, o que está comprometendo o seu crédito hoje no financeiro são as faturas que vão vencer.
**C:** Eu tenho que ter fatura a vencer. Agora, se eu tiver a fatura atrasada,
**A:** Não,
**C:** aí tudo bem. Não, eu tenho fatura que vai a vencer.
**A:** mas a Localiza
**C:** Não,
**A:** compromete o crédito com faturas a vencer. Entendeu? Não é só uma questão só da BTEC, não, mas é todos assim, é uma política...
**C:** eu entendi.
**A:** Agora aqui, olha o que nós vamos
**C:** Eles
**A:** fazer.
**C:** pegam o valor do contrato, por exemplo, 33 de contrato mais a fatura.
**A:** agora deixa
**C:** então
**A:** eu te contar
**C:** é isso,
**A:** um negócio.
**C:** eu entendi. Eles pegam o exemplo. Eles pegam o... Quanto que eu tenho hoje de contrato? Então 33 mil. 33 mil mais a fatura que vai vencer. Que dá 26, ele somou tudo e está dando 59 mil. Não é isso?
**A:** Sim, isso. Agora deixa
**A:** eu te contar uma
**C:** eu isso
**A:** coisa. Agora aqui eu tenho uma solução. Vamos lá. Vamos lá o que a gente vai fazer, tá?
**C:** Eles pegam o contrato em aberto, mas a fatura, eles somem assim.
**A:** Isso, mais as faturas, isso
**A:** mesmo. Agora a gente vai fazer uma coisa aqui, um combinado. Eu vou fazer isso só para você, tá? A gente vai fazer assim... Se você tiver aluguel mensal, aluguel mensal 30 dias, o que você vai fazer? Você vai fazer uma reserva de uma diária e depois a gente altera esse contrato para o mensal. Porque quando
**C:** Entendi.
**A:** eu faço isso, ele não lê o crédito, entendeu? Só que você tem que ter o mínimo para fazer a reserva de um dia. Deu para entender? Só que aí, vamos lá, só raciocínio, tá? As meninas do escritório vão ficar um pouco comprometidas, porque se elas colocam 10, 7 ou 8 ou 15 dias, elas precisam de crédito. Mas no seu caso, no seu caso, como é de 30%, a gente faz assim. Você vai fazer de um dia e aí você vai... Esse usuário retirou o carro. A gente altera ele pro mensal porque aí não lê o crédito. Entendeu? Aí, assim, como que a gente vai combinar? Só que para isso acontecer, para
**C:** Entendi.
**A:** isso acontecer,
**C:** Eu sei
**A:** a gente
**A:** precisa...
**C:** está... Que
**C:** está a
**A:** você tem
**C:** parte
**A:** que...
**C:** da...
**C:** Uhum.
**A:** você tem
**C:** A gente
**A:** que dar
**C:** que vai
**C:** rolar normal, não tá no marginal marginal,
**A:** mil reais de fatura.
**C:** na próxima de a
**A:** Entendeu?
**C:** Coca-Cola ali... Uhum, entendi?
**A:** Para que
**A:** consiga
**C:** shopping deu bem?
**A:** fazer isso. Aí a gente vai conseguir direitinho. E aí, o que acontece? O 100 mil... Já tive uma reprovação, mas eu pedi 80. Vamos ver o que eu consigo lá, entendeu?
**A:** Aí assim, eu vou acompanhando.
**C:** Não.
**A:** é igual, já vai conversando com o financeiro? Fala assim financeiro? Existe a possibilidade da gente já ir antecipando essas faturas da Localiza para que se não o time lá do escritório que faz o aluguel diário, eles vão ficar sem possibilidade de fazer reserva aqui com a gente.
**C:** Eu já vou conversar com o... para pegar mais próximo, nem que não pague tudo, mas paga uma amanhã,
**A:** Não, você
**C:** paga outra
**C:** sexta
**A:** que pagar uns 15 mil.
**A:** É, tem que pagar aqui,
**C:** vai pagando,
**A:** ó. Tem que ser
**A:** aqui, ó.
**C:** pagando.
**A:** Aqui, ó. Aqui, ó. 6, 789. Ótimo 9... Você tem que pagar até o dia 13 do 7 para liberar ali... É, na verdade tem que pagar praticamente tudo, né?
**C:** vai pagando. Não, eu entendi. Eu entendi o Andresa. O processo da localiza. Ela pega os contratos em aberto, valor mais a fatura vencer e soma os dois aí para jogar em
**A:** E...
**C:** cima da carta de crédito. Ela
**C:** soma
**A:** isso
**C:** os contratos
**A:** agora
**C:** em aberto
**A:** eu...
**C:** e mais a fatura vencer.
**A:** Agora pode
**C:** Não é isso?
**A:** ficar tranquilo,
**C:** Não,
**A:** depender de mim aqui eu vou fazer. Só que assim,
**C:** isso aí eu
**C:** sei disso.
**A:** estou sem possibilidade porque é uma regra do financeiro da diretoria que
**C:** Eu sei...
**A:** acompanha. Você
**C:** Muito,
**A:** entendeu a situação, Luiz?
**C:** então com certeza, com
**C:** certeza.
**A:** aqui, quando a
**C:** Não, já
**A:** gente
**C:** está
**A:** tiver mensal
**C:** liberado
**A:** para
**C:** porque
**A:** comprometer
**C:** eles até
**A:** muito
**C:** colocaram...
**A:** crédito, você vai fazendo de mão diária.
**C:** Entendi.
**A:** Esse usuário retirou o carro, você vai me ligar para a gente mudar para o mensal. Aí eu vou mudando e ele não lê o crédito. Aí dá uma forma de você conseguir fazer mais. Entendeu? Então,
**C:** Não,
**C:** beleza então.
**A:** Então, primeiro, vou acompanhar esse retorno dos 80 mil.
**C:** Do 80 mil?
**A:** Vou novamente falar com a minha supervisora aqui para ver se ela consegue ter algum tipo de negociação à parte. E a outra questão é o seguinte... Veja também do seu lado se é possível você ir pagando pelo menos um bloco aí de faturas para a gente poder liberar esses créditos aí.
**C:** Não, beleza. Eu já alinhei com o condutor financeiro e explicar essa situação para eles entenderem
**A:** Porque
**C:** melhor.
**A:** senão as meninas lá têm aluga diária no escritório, vai ficar
**A:** prejudicada.
**C:** ficar prejudicado,
**A:** Você até que
**A:** não, porque você faz, mas essa obra nova que você vai precisar, você vai precisar de carro, né?
**C:** O que se dá
**A:** Entendeu?
**C:** de carro?
**A:** Pois é. Então tá bom, Luiz. Vou te encaminhar
**C:** Beleza?
**A:** à pesquisa e vamos conversando, tá bom?
**C:** Combinado.
**A:** Um abraço. Até mais.
**C:** Eu vou te mais, tchau.
**A:** Tchau, tchau.

---

## Caso 2 — Cliente 27170310

- **segment_id:** `c757aa09-dd5a-4d3e-97ab-bd8c69b445f4`
- **Data:** 2026-06-29 · **Duração:** 1.182s
- **Padrão:** contrato aberto com franquia de 1.000 km (mais barata, "cabe" no limite de crédito) com promessa de migrar para 5.000 km no dia seguinte via "condutor de contrato" — estruturação deliberada pra passar por baixo do crédito aprovado.

### Transcrição completa

**A:** Bom dia, Andrew.
**C:** Alô? Bom dia, meu querido. Tudo na paz?
**A:** Tudo na paz com você? Tudo bem?
**C:** Tudo, meu filho? Com Jesus em um barco, né? A gente tem que colocar ele em primeiro lugar em tudo,
**A:** Com ele no barco a gente está seguro, a gente sabe que as coisas vão fluir.
**C:** né? É verdade. Certo.
**A:** Vamos lá, deixa eu te ajudar nesse processo aqui. Nós vamos precisar de fazer um procedimento diferente, porque eu dei uma olhada aqui, você não está conseguindo fazer esse pedido de reserva porque está comprometendo o crédito total que a empresa tem liberado. Eu até tentei uma liberação maior de crédito aqui, mas o pessoal do condutor de crédito não aprovou não. Mas a gente vai dar um jeito aqui para a gente conseguir liberar esse carro para você hoje, tá?
**C:** Certo,
**A:** O que nós vamos fazer? Eu estou vendo aqui... que você está com alguns boletos para vencer dia 5 do 7.
**C:** certo. Isso!
**A:** Aí o que nós vamos fazer então? Para você retirar esse carro hoje, nós vamos fazer esse aluguel por diárias para
**C:** Certo!
**A:** a gente conseguir dar um custo menor. E depois que você retirar o carro, você vai pegar esse carro hoje, aí amanhã
**A:** eu vou solicitar o meu condutor de contrato para fazer a alteração do contrato para você para o contrato do aluguel mensal, tá?
**C:** Certo!
**A:** Ou então tem uma outra opção também. Eu vou até olhar aqui se dá, porque de repente, ao invés de a gente fazer com a quilometragem de 5 mil km, a gente faça a quilometragem de mil porque reduz o valor. A gente olha se o crédito libera. Só ver quanto que vai dar de mil
**C:** Sim.
**A:** aqui,
**C:** Ponto,
**C:** veja.
**A:** se a de mil der
**C:** Eu estou
**A:** dentro
**C:** até aqui
**A:** limite,
**C:** o computador
**A:** a gente
**C:** aberto
**A:** faz o
**C:** aqui
**A:** dinheiro.
**C:** porque eu já faço tudo por aqui, né?
**A:** Ah não, excelente. Se você quiser já pode ir dando uma olhada aí que nós vamos contar na quilometragem de mil, de mil km,
**C:** Certo,
**A:** para...
**C:** já vou abrir aqui, eu abri a coisa agora, acho que é só abrir a internet aqui agora.
**A:** Não, tranquilo. Eu estou abrindo aqui também. Aí nós vamos fazer para a gente ver quanto que vai dar. Porque se der o valor de limite que nós temos aqui, a gente faz no de mil e depois eu peço migrar para 5 mil
**C:** A gente altera,
**A:** para você.
**C:** né? É
**A:** E isso
**C:** o tempo
**C:** também
**A:** é...
**C:** dia 5 agora eu estou pagando aquele boleto,
**A:** Isso, exatamente. Mas aí
**A:** você abre, a gente faz isso de mil, faz a abertura no contrato de mil e depois que o contrato for aberto eu peço meu condutor de crédito aqui para fazer a migração para 5 mil KMs aí
**C:** Entendi
**A:** vai dar certinho
**A:** também
**C:** Então, tá bom.
**A:** vamos só ver se o de mil se vai dar o preço aí para a gente poder pegar o que a gente tem de crédito aqui eu acredito que deve dar sim mas vamos fazer aí para ver se vai dar certo já estou entrando
**A:** aqui também
**C:** também já estou entrando aqui, já entrei aqui
**A:** Ah, não, beleza. Então, você deve estar até na minha frente. Meu sistema está lento?
**C:** Ah, tá? E tá
**A:** Ele está
**C:** chovendo por
**A:** devagar...
**C:** aí não?
**A:** Não, está chovendo não. Está tão friozinho, mas não está chovendo não.
**C:** Aqui é chuva, viu?
**A:** É mesmo?
**C:** É, agora que tem uma paradinha.
**A:** Mas está descendo água aí.
**C:** É esse período de São João todinho esse mês de junho.
**A:** Sempre
**C:** Foi muita
**A:** chove,
**C:** chuva
**A:** período
**C:** aqui.
**A:** de som é chove. É mesmo,
**A:** é engraçado.
**C:** é muita chuva. Muita chuva. São João mesmo choveu muito.
**A:** É mesmo gente, nossa eu vou te falar tem duas semanas que eu estou correndo atrás do pessoal aqui porque da grande maioria está de férias coletivas de empresa pessoal
**C:** É, e agora é
**C:** férias para a escola
**A:** escola
**C:** tudo, né?
**A:** exatamente
**C:** Para a criança, né?
**A:** exatamente nós estamos aqui mas tá fluindo devagar ainda tá indo né a gente sabe que são meses atípicos e ainda vem com copa do mundo junto ainda o negócio tá bom
**C:** É, hoje nem... Hoje para, né? Esse negócio desse jogo né?
**A:** Oi, para, para, meio dia. Na verdade, agora pela manhã o movimento já está bem assim, bem fraco, estou tendo pouquíssimos acionamentos aqui, mas depois de meio dia aí que não vai ter mesmo... O Ender, só para poder olhar aqui, você colocou retirada Recife?
**C:** Alô?
**A:** Oi, você colocou retirada foi Imperatriz? Foi, né?
**C:** Como é?
**A:** A retirada do caso você colocou foi Imperatriz?
**C:** Isso!
**A:** Imperatriz, tá...
**C:** Eu tá chegando lá... Eu creio que amanhã... Você tá aí em Belo Horizonte né?
**A:** Eu estou
**C:** Alô?
**A:** em Belo Horizonte.
**C:** Daí de Minas eu conheço eu passei uma semana aí em Governador Valadares
**A:** Governador
**C:** é longe
**A:** vai lá dar essa cidade próxima aqui.
**C:** é próximo mas
**A:** É próximo,
**C:** rapaz
**A:** próximo.
**C:** fiquei encantado aí sabe que foi na região de vocês meu amigo eu sou uma pessoa que eu gosto muito de
**A:** Sim,
**C:** queijo
**A:** sim.
**C:** Rapaz,
**A:** Só um pouco...
**C:** eu comi tanto queijo aí! Eu comi um tal de um queijo cabacinho! Um
**A:** Acabar
**C:** queijo chama... Não é?
**A:** assim é bom, é bom, é bom.
**C:** Você
**A:** Levou?
**C:** levei!
**A:** Você levou ou não levou para casa? Ou não deu para levar?
**C:** É bom demais!
**A:** Ah, não
**C:** Outra
**A:** pode...
**C:** coisa! Sabe o que aconteceu aí na região? Eu engordei! Eu acho que uma semana eu engordei! Porque tem um chazinho da tarde aí que o povo prepara uma mesa, meu amigo! É queijo! É bolacha! É não sei o quê! É tanta coisa!
**A:** O pessoal fala quando vem aqui para Minas engorda porque é tudo, né? Mas o queijo também eu gosto de um queijinho. Eu gosto de um queijinho com cafezinho, eu
**C:** Essa
**A:** sou assim...
**C:** região
**C:** de vocês aí de comida é bem melhor do que São Paulo, eu acho, sabe? Particularmente
**A:** sim,
**C:** a comida de vocês que São
**A:** sim. Mas
**C:** Paulo
**C:** Jesus...
**A:** gente tem uma fama de ter uma culinária muito boa e eu sou meio suspeito porque tudo que tem aqui eu gosto demais esse queijo
**C:** Lá eu comi
**A:** então
**C:** tanto
**C:** tipo
**A:** vou te falar
**C:** de queijo aí eu comi...
**A:** Se tiver oportunidade de você vir em Belo Horizonte também, você vai gostar. Em Belo Horizonte tem um... Nós temos o nosso mercado aqui, que vou te falar. O queijo aqui é fundamental. Excelente, excelente, sensacional.
**C:** É porque os queijos aí é queijo, muito queijo também, é feito artesanal, né? Aqueles queijos,
**A:** Artesanal,
**A:** grande maioria,
**C:** É...
**A:** grande maioria. A gente tem as propriedades rurais aqui que tem e tem muito e favorece também o clima, as fazendas que tem, as matas acaba que
**C:** É...
**A:** favorece bastante a
**C:** É...
**A:** maturação
**C:** É...
**A:** do queijo. Então isso é excelente, sem
**A:** contar
**A:** as criações
**C:** também
**A:** também.
**C:** em outro lugar aí, eu fui aí num pessoal que eles até fabricam, eles é fornecedor de café em Guaxu... Guaxu é Minas,
**A:** Gachopé
**A:** Minas também.
**C:** É perto de São Paulo, né? Já quase, né?
**A:** Guacho Pé, não. É assim, se for olhar o sentido onde você está de governador Valadares, sim, aí já é mais
**C:** Não,
**A:** próximo
**C:** mais
**A:** Paulo
**C:** estava em São Paulo. Eu fui de São Paulo
**A:** para
**C:** para lá.
**A:** Guacho Pé.
**C:** Foi aí a terra do café.
**A:** É, no caso aqui nós temos aqui uma região, sim, que fabrica, na verdade todo o estado, desde o Dado a gente tem região sul que fabrica, tem região leste que é mais forte um pouquinho, aí tem o norte, aí na verdade o café está presente aqui no estado praticamente todo.
**C:** É, é muito forte aí, né?
**A:** Muito forte, muito forte.
**C:** Muito
**A:** Mas isso
**C:** forte
**A:** desde
**C:** o...
**A:** muito tempo. Tinha aquela república lá do café com leite e juntava com São Paulo. Então acabou
**C:** Então
**A:** que ficou na região
**C:** qual é
**A:** mesmo
**C:** a região da
**A:** e...
**C:** gente aqui de Fernambuco?
**A:** Não conheço, acredita?
**C:** Não?
**A:** Não conheço. Sou doido para conhecer o máximo que eu fui foi só até Bahia depois eu não
**A:** acabei
**C:** muito
**C:** bom,
**A:** conhecer o Nordeste,
**C:** aparentemente.
**A:** não.
**C:** Aqui também de Porto de Galinha, esses passeios Maragogi né?
**A:** Eu sou doido para ir para o Nordeste e subir um pouquinho mais, mas um dia Deus vai me dar essa possibilidade,
**C:** Ai Deus,
**A:** um dia eu farei
**C:** ele... Ele honra, né?
**A:** sim,
**C:** Eu estava vendo
**C:** um monte, eu gosto de orar no monte, sabe?
**C:** Aqui. Aí eu estava com a missionária lá. Aí a missionária disse assim, ô amado, você acredita? que deixa como uma escuda. Já estou com o passaporte pronto e vou para a França pregar na França.
**A:** agora
**C:** Isso é mesmo, minha amada.
**C:** Eu digo acredito, porque Deus prepara tudo, né?
**A:** sim Deus
**A:** envia
**C:** quando foi
**C:** ontem eu fiquei tão feliz, irmão, ela já está na França pregando
**A:** olha
**C:** Aí eu disse, está vendo? Aí ela deu o testemunho dizendo que isso aqui, ela estava num lugar lá e dizendo que isso aqui é testemunho que eu vou dar agora, que naquele momento parecia improvável eu chegar até aqui, né?
**A:** A gente tem que acreditar e confiar que Deus...
**C:** É, então Deus é um Deus que ele muda, muda estação, muda tudo
**A:** Exatamente...
**C:** O povo aqui não vai fazer sol para pai de toma chuva. Ele confunde... É, ele
**C:** confunde...
**A:** é isso mesmo!
**C:** É, eu estava ontem... Ontem eu estava... Ontem eu estava... Não tive uma oportunidade eu estava dizendo... Irmão, vê o senhor que negócio forte. Eu disse... Eu estava no lugar... Tem uma ilha assim na frente, assim, perto da praia, sabe? Uma ilha. E aí eu vi numa areia, uma amarese secou, né? E aquele caminho assim. Aí veio uma passagem assim falando do deserto, né? Quando a gente está em deserto, processo e tudo. E aí eu disse, mas meu irmão, você crê que Deus cumpre promessa dentro do deserto?
**A:** Com certeza.
**C:** Aí eu digo...
**A:** E na verdade, é onde nós somos mais usados é no deserto,
**C:** Não!
**A:** né? Porque no deserto é que vem as nossas provações e...
**C:** Eu estava... Eu dei uma palavra agora de manhã. Eu dei uma palavra para uma pessoa que ligou para mim, sabe? Aí ele
**A:** Exatamente!
**C:** disse... Eu digo... Não, não falo nada não. Deixa eu só falar um negócio para você. Eu falo algo para ele. Eu disse... Irmão, engraçado não é nada que tem área que a gente está mais machucado, assim... Mais ferido... Mais passando aquele processo e é onde Deus usa a gente naquele... processo naquele dando força a outras pessoas naquilo ali já imaginou
**A:** Exatamente é isso mesmo! Quando somos fracos é que somos fortes, né?
**C:** isso a palavra disso né
**A:** Exatamente. Wendel,
**C:** pronto
**A:** eu olhei aqui, meu amigo. Não sei se você conseguiu aí. Enquanto estava conversando com você, eu fui fazendo aqui para a gente poder
**C:** pronto
**A:** ganhar tempo.
**C:** já estou aberto aqui
**A:** Eu olhei aqui para 1 mil KMs, eu acho que vai dar o que a gente precisa,
**C:** pronto
**A:** tá? Para 1 mil KMs
**C:** pronto
**A:** deu 3 mil 31800%. A gente faz para 1 mil e depois que você pegar o
**A:** carro eu solicito
**C:** gente altera
**A:** para poder alterar para 5 mil.
**C:** certo e
**C:** também
**A:** Então pode...
**C:** dia 5 agora também está pagando aquele boleto aí já vai tá
**A:** É, mas aí de qualquer maneira eu vou ter que pedir porque como a gente vai abrir esse contrato com mil KMs, aí eu vou ter que pedir para alterar ele para 5
**A:** mil, tá? Mas pode fazer com mil aí, você pega com mil, aí assim que você pegar o carro lá, você só me... Você pega hoje mesmo?
**C:** É, foi.
**A:** Aí você pegando hoje então, aí amanhã, se você lembrar, você só me manda um oi porque amanhã
**C:** Sim.
**A:** eu pego e já faço alteração aqui para o 5 mil
**C:** Pronto, tranquilo.
**A:** Tá bom? Mas faça para mim aí, vê se vai dar certinho para a gente poder confirmar aqui.
**C:** Vou fazer
**C:** aqui agora.
**A:** eu acho que vai dar certo
**C:** Vou fazer aqui agora.
**A:** aí. Acho que vai fechar certinho aí.
**C:** Aí eu boto... Tá mil, né?
**A:** Isso, coloca mil.
**C:** Eu boto pra 30 dias mesmo?
**A:** 30 dias, pode fazer normal, 30 dias aí, você precisa de 30 dias, não é?
**C:** Não? Isso, isso.
**A:** Então pode fazer normal 30 dias. O que você vai colocar diferente é só quilometragem, que ao invés de fazer
**C:** Entendi.
**A:** 5 mil a gente vai colocar mil para poder ficar dentro do limite e depois eu faço a alteração para 5 mil.
**C:** Entendi. Vai fechar lá não, né?
**A:** Você fala agência?
**C:** Sim? Não, né?
**A:** Não pessoal, a agência do aeroporto a gente funciona 24 horas
**C:** É, então tá aqui
**A:** pessoal vai
**C:** dia...
**A:** ter que torcer lá do aeroporto hoje.
**C:** É... E o cara aí... Vê se apareceu aí.
**A:** Opa, vou olhar aqui agora.
**C:** Deixa eu ver aqui... Cadê que tá até até aí? Aí continua lá. Ó o que eu faço ali ó...
**A:** Não apareceu ainda não deixa eu voltar aqui
**C:** Não, vai
**C:** aparecer
**A:** novo
**C:** agora.
**C:** Eu tava terminando
**C:** aqui.
**A:** que não tá no que você deixa eu ver se apareceu já fui aqui deixa
**C:** É, agora isso é tudo... E agora se apareceu?
**A:** eu olhar aqui agora apareceu retirados vai ser feita pelo jones
**C:** É, Jona.
**A:** Certinho.
**C:** Jona.
**A:** Tá tudo certinho, Jones de Castro. Certinho, tá apareceu aqui pra gente, sim. Tá tudo ok, tá? Aí eu só vou te pedir o seguinte então, Ender. Se você lembrar, amanhã você me dá um e que vai ser o WebEx. Vamos mudar
**A:** o contrato.
**C:** outra coisa,
**A:** Mas qual...
**C:** eu ia ter com você porque como eu vou precisar mais um mês desse que eu estou em
**A:** Uhum.
**C:** relação àquela questão da quilometragem, ver se tu me ajuda? Lembra que tu disse qualquer coisa a gente vê, botar uma quilometragem a mais e ver se fica o mesmo valor.
**A:** No caso, se a gente aumentar a quilometragem, a quilometragem maior vai ter sempre uma variação de preço. Então sempre
**C:** Então deixa
**A:** tem...
**C:** quieto.
**A:** É, aí sempre tem... No caso, a gente pode administrar. A gente pode olhar essa questão aí para se for o caso tentar diminuir um pouquinho para você não pagar quilometragem excedente, tá?
**C:** É...
**A:** Aí você vê se puder evitar, a gente vai acompanhando. No sistema aí você consegue ver também. Sabe no sistema aí quando você... A superior tem escrito aí gestão e dentro
**C:** Sim...
**A:** do gestão tem painel de gestão de veículos e reservas.
**C:** Pronto.
**A:** Quando você abrir aí, você vai fazer o filtro aí você coloca o nome da empresa aí você pode colocar o período aí de um dia só para poder abrir os contratos aí aí quando você clicar em contrato essa que você está com você está com 2 mil km né Tem que administrar, porque pelo que eu estou vendo aqui, dia 29 fechou com 2,249. Tem que sempre estar administrando aí, mas você consegue verificando a evolução do contrato que você está utilizando. Mas a gente vai acompanhando, então está com 2 mil e vai administrando. Mas a diferença geralmente não é uma diferença muito grande não, tá? Se você ver que você vai usar... Ah, não, eu estou usando 2 e 500, 2 e 600, 2 e 700, é bom a gente mudar. Enquanto ficar nesse limite que você está bem próximo, eu acho que você consegue administrar aí e consegue segurar um pouquinho Mas vai sempre olhando nesse campo que eu te falei e você consegue ver que tem lá dados de consumo de quilometragem aí vai te dando o consumo vai te dar o consumo que você teve até hoje por exemplo mas
**C:** Entendi.
**A:** qualquer coisa você me chama aqui que a gente olha
**C:** Entendi.
**A:** a possibilidade
**C:** Bom, até
**C:** amanhã
**A:** mudar se
**C:** eu falo
**A:** você
**C:** contigo, né? Pra gente ver alterar, tá?
**A:** Eu vou deixar aqui já agendado aqui, é só para você me passar um oi aqui, que se eu tiver com uma demanda muito grande eu já dou prioridade para fazer aqui.
**C:** Amanhã, né?
**A:** Isso amanhã, você pegando hoje, amanhã a gente faz essa alteração.
**C:** Tá bom, tranquilo.
**A:** Tá bom? Então tá
**C:** Tá bom,
**A:** certo
**C:** meu querido.
**A:** então, Edu? Tem mais algo mais
**C:** Não,
**A:** que eu posso te
**C:** não,
**A:** ajudar
**C:** querido,
**A:** momento,
**C:** isso mesmo,
**A:** amigo?
**C:** viu?
**A:** Então
**C:** Obrigado
**A:** precisando
**C:** mesmo, viu?
**A:** ou tô à disposição precisando aqui pode me chamar prazer enorme
**C:** Tá bom.
**A:** falar com você e dá
**A:** um jeito
**A:** agora
**C:** mesmo.
**A:** de conhecer Belo Horizonte também você veio pertinho
**C:** É...
**A:** você
**C:** comer um queijinho aí e
**C:** tomar
**A:** qual igreja?
**C:** café. Eu sou... Aqui eu sou da igreja da família.
**A:** Olha, engraçado, aqui perto de casa tem uma igreja da família Não sei se é da mesma,
**C:** É, né?
**A:** mas tem uma igreja da família perto
**C:** É...
**A:** de casa aqui
**C:** Aqui também... Aqui a gente... Eu vou muito também gostar na Advec, né?
**C:** Você é
**A:** coisa
**C:** de qual
**A:** Coisa boa Eu sou de uma que nós temos aqui É uma igreja de bairro mesmo Chama Igreja Cristã Morada
**C:** Sim.
**A:** Morada. Mas nós já temos já uma na Bahia e já tem uma também lá no sul, no Paraná. Nós estamos aí já
**C:** Em crescimento, né?
**A:** plantando as nossas sementes aí
**C:** Expansão
**A:** já. Exato.
**C:** é isso mesmo o reino tem que quanto
**A:** Tem que expandir,
**C:** mais a gente
**C:** semeia no reino mais Deus ele opera né
**A:** Exatamente, exatamente mas
**A:** com ele nós vamos crescendo
**A:** vamos em
**A:** fé caminhando em fé ou
**C:** é verdade mesmo
**A:** então meu irmão prazer
**C:** obrigado
**A:** em falar
**C:** fique
**A:** você
**A:** novamente
**A:** então
**C:** viu semana
**A:** tá na paz
**C:** abençoada
**A:** também que
**A:** deixa
**C:** para
**C:** você
**C:** vitória
**A:** gente para
**C:** vitória
**A:** nós para
**C:** nome
**C:** de Jesus
**C:** amém
**A:** vou te pedir para fazer aquela avaliação antes
**C:** bota
**A:** de encerrar
**C:** agora
**C:** agora
**A:** fazer uma
**C:** tu vai mandar
**C:** aqui no computador
**C:** é no
**A:** aguardar
**C:** Agora, valeu,
**A:** Então, um
**C:** meu irmão.
**A:** abraço, amigo. Até
**C:** Abraço.
**A:** mais.

---

## Recomendação

1. Encaminhar este arquivo ao jurídico/risco de crédito antes de qualquer uso em treinamento comercial.
2. Considerar rodar uma busca dirigida (não é preciso IA — regex/keyword) por "não lê o crédito", "cabe no limite", "franquia menor pra depois migrar" na base inteira (6.623 ligações) pra dimensionar quantos casos existem.
3. Não usar nenhum dos dois exemplos acima como "boa prática de contorno de objeção" em nenhum material de treinamento — o oposto do que a Hipótese 3 (Challenger bem feito) recomenda.
