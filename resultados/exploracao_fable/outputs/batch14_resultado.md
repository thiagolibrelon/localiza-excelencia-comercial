# Lote 14 — Exploração P3+P7

## Resumo do lote
- Total de ligações no lote: 38
- Ligações da BASE_ANTIGA_1275: 10
- Ligações do NOVO_LOTE_5348: 28

## P3 — Problemas recorrentes (tabela de frequência)
| Código | Categoria | Ocorrências | Resolvido na ligação (SIM/NAO/PARCIAL — contagem) | Escalou (contagem por destino) |
|---|---|---|---|---|
| P1 | Acesso/sistema (portal, senha, biometria) | 1 | SIM: 1 (aprovação de usuário + senha + biometria resolvidos ao vivo) | nao_escalou: 1 |
| P2 | Faturamento/cobrança | 4 | SIM: 2 / PARCIAL: 2 | 0800: 1; nao_escalou: 3 |
| P3 | Multa/infração | 1 | PARCIAL: 1 (faturas de multa conferidas, baixa pendente) | 0800: 1 |
| P4 | Manutenção/substituto | 1 | PARCIAL: 1 (revisão agendada, taxa de deslocamento em análise) | nao_escalou: 1 |
| P5 | Condutor/cadastro | 2 | SIM: 2 (descadastro de telefone; inativação de usuário) | nao_escalou: 2 |
| P6 | Km excedente | 0 | — | — |
| P7 | Disponibilidade | 0 | — | — |
| P8 | Franquia/agência | 1 | PARCIAL: 1 (feedback registrado, sem compensação) | interno (e-mail p/ gestão da loja): 1 |
| P9 | Sinistro | 0 | — | — |
| P10 | Reserva/sistema | 4 | SIM: 3 / PARCIAL: 1 | IT (correção em andamento): 1; nao_escalou: 3 |
| P11 | Outro | 2 | NAO: 1 (insatisfação com downgrade de veículo) / PARCIAL: 1 (reclamação de preço, prometeu desconto) | nao_escalou: 2 |

Obs.: Cliente 25070786 conta em P2 e P3 (faturas de multa + baixa de pagamento). Bloqueio de reserva do cliente 25272980 contado só em P2 (causa raiz = fatura vencida).

## P3 — Exemplos
- **Cliente 17015435 (P10):** "estou tentando fazer uma reserva... a partir do momento que pede a nacionalidade ele para e trava!" — sistema WebCorp fora do ar geral; vendedor confirmou erro conhecido ("a gente está atuando para corrigir") e prometeu avisar quando voltar. Cliente com medo de perder o único carro disponível na agência.
- **Cliente 17293211 (P8):** "marquei para pegar o carro às oito e o carro não estava lavado... me atrasei 40 minutos" — loja com falta de funcionário; cliente relata outro cliente que desistiu e "foi para a Movida ali do lado". Vendedor registrou feedback formal para a gestão da loja.
- **Cliente 25070786 (P2/P3):** recebeu notificações de Serasa por faturas de multa já pagas; baixa não processada. Atendente conferiu boletos um a um e encaminhou para o 0800 solicitar a baixa.

## P7 — Cross-sell/Upsell (tabela de frequência)
| Código | Produto | Vezes mencionado | Vezes ofertado ativamente | Janelas perdidas identificadas |
|---|---|---|---|---|
| PR1 | Aluguel mensal leve (core) | 17 | 11 | 0 |
| PR2 | Aluguel pesado | 3 | 2 | 1 (cliente 11760410 tem caminhão próprio, não sondado) |
| PR3 | Telemetria | 0 | 0 | 0 |
| PR4 | Proteção total | 7 | 4 | 0 |
| PR5 | Upgrade categoria | 1 | 0 | 1 (cliente 23459443 insatisfeito, aceita pagar mais por carro melhor — sem oferta) |
| PR6 | Km adicional | 2 | 0 | 0 |
| PR7 | Contrato anual (mensal fixo 12m) | 5 | 2 | 0 |
| PR8 | Elétrico | 0 | 0 | 0 |
| PR9 | ZARP | 0 | 0 | 0 |
| PR10 | Meoo/assinatura | 1 | 0 | 1 (cliente 11760410: 7 carros por assinatura com concorrentes — sem contraproposta) |
| PR11 | Seminovos | 0 | 0 | 1 (cliente 23969775 vai trocar utilitário próprio; ofertou só locação) |
| PR12 | Gestão de frotas | 3 | 1 | 1 (cliente 27221305 vai comprar frota própria de 8 veículos — sem oferta de gestão) |

## P7 — Exemplos
- **Oferta ativa bem feita — Cliente 01721282 (vendedor Matheus):** transportador com 45 caminhões de frota própria; vendedor identificou a operação, apresentou o "Localiza Pesados" com cenário concreto ("demanda de mais cinco caminhões por um ano sem imobilizar verba") e acionou o time especializado para dar sequência. Cross-sell PR2 completo: sondagem → produto → próximo passo.
- **Oferta ativa bem feita — Cliente 15184060:** cotação de Fiorino por 20 dias (R$ 4.811) convertida em mensal (R$ 4.363), com oferta adicional de proteção total de avarias na proposta e ainda sondagem espontânea de frota pesada ("a Localiza trabalha com frota pesada de caminhão, se precisar a gente cota").
- **Janela perdida — Cliente 11760410:** cliente detalhou 7 carros por assinatura com HP, LM e GM Fleet e disse que vai reestruturar ("vamos deixar 2-3 na assinatura e o resto rotativo"). Vendedor só acolheu o plano de diárias futuras; nenhuma contraproposta de assinatura/gestão de frotas Localiza para capturar os contratos que vencem em agosto.
- **Janela perdida — Cliente 23459443:** cliente explicitamente disposto a pagar mais por carro superior ("estou pagando mais caro por um negócio pior") e ameaçando cancelar; atendente não ofertou upgrade de categoria nem alternativa, e encerrou comprometendo-se apenas a enviar o valor da multa de cancelamento.

## Observações livres
Boa parte do lote (~10 ligações) é check-in de carteira/apresentação de executivo sem nenhuma tentativa de oferta além do "oi no WhatsApp" — o WhatsApp aparece como canal padrão de follow-up em quase todas as ligações. Chamou atenção a ligação do cliente 06495149: a executiva pede explicitamente nota NPS ≥9 ("nota 8 para baixo não é boa para o meu resultado"), prática que distorce o indicador. Os executivos também absorvem muito suporte operacional (reservas passo a passo no WebCorp, prorrogações, boletos), o que gera fidelização mas consome tempo de ligações longas (até 29 min) sem conversa comercial.
