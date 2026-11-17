# Legacy Forge 49.4 — análise aprofundada 02 (server browser, API e cliente)

## Amostra e integridade

- Arquivo: `LegacyForge-49.4.apk`
- SHA-256: `629e0ac137968e9fed2e0ad567a229ce062e89ebd33f2901eb9c23b3553fae80`
- 89,394,617 bytes; ZIP íntegro, 235 entradas.
- 66 DEX (`classes.dex` até `classes66.dex`).
- Bibliotecas nativas ARM64: `libUE4.so` (120,782,624 bytes), `libmenu.so` (54,200,728 bytes), `libgnustl_shared.so` (1,514,928 bytes).
- Nenhum OBB, PAK de jogo ou executável de servidor dedicado foi encontrado dentro do APK.

## 1. Achado novo: a camada de server browser padrão do ARK continua presente

A biblioteca `libUE4.so` contém símbolos nativos com nomes completos para:

- `UServerListMobileInterface::Initialize`
- `UServerListMobileInterface::DownloadServerList`
- `UServerListMobileInterface::GetServerList`
- `UServerListMobileInterface::JoinServer`
- `UServerListMobileInterface::PlatformLogin`
- `UServerListMobileInterface::GetPlatformLoggedIn`
- `UServerListMobileInterface::OnFindServerListComplete`
- `AShooterGameSession::RequestUnreservedServerList`
- `AShooterGameSession::HttpGetUnreservedServerListRequestComplete`
- `UUIServerView::DownloadStatsByURL`
- `UUIServerView::DownloadStatsByEntry`
- `UUIServerView::StatDownloadResponse`

A mesma biblioteca contém literalmente os endereços de lista padrão:

- `http://arkdedicated.com/mobile/cache/officialserverlist.json`
- `http://arkdedicated.com/mobile/cache/unofficialserverlist.json`

**Interpretação:** o binário do jogo ainda inclui o mecanismo tradicional de descoberta/listagem do ARK Mobile. Isso é uma evidência concreta de que o Legacy Forge não substituiu simplesmente todo o sistema nativo de server browser por outro binário independente.

## 2. O filtro LegacyForge é uma camada separada

Na `libmenu.so` aparecem:

- `SettingsLegacyForgeServersOnly`
- `legacyforge_servers_only`
- `LegacyForge servers only`
- `On: show only LegacyForge servers. Off: show the game's unofficial servers.`
- `follow the selected server list`

O texto confirma a existência de um filtro de interface/configuração que alterna entre mostrar apenas servidores LegacyForge e mostrar a lista de servidores não oficiais do jogo.

**O que isso prova:** o cliente possui um modo de filtragem próprio para a lista de servidores.

**O que isso não prova:** que o Forge tenha um protocolo de rede totalmente novo, um master server próprio independente ou que tenha removido todas as dependências da infraestrutura original. O filtro pode selecionar/filtrar entradas recebidas, consultar uma API própria, ou combinar as duas coisas. É preciso seguir as chamadas de código para decidir.

## 3. A API própria não revela o host na amostra estática

Em `libmenu.so` foram encontrados os identificadores:

- `gameApiUrl`
- `joinTicket`
- `LegacyForge server ticket`
- `Server Transfer Ticket`
- `FCurlHttpRequest::SetURL`
- `UUIServerView::DownloadStatsByURL`

A busca por strings de URL na `libmenu.so` encontrou somente:
- `https://discord.gg/Z5cRBwKq55` (convite público do Discord do projeto)
- URLs de documentação/licenças de bibliotecas embutidas (ImGui e fontes)

Não foi encontrada uma URL HTTP(S) literal que possa ser atribuída à API do LegacyForge. A string `gameApiUrl` é apenas um nome/identificador; não é o valor da URL.

Possibilidades que continuam em aberto:
1. O host é recebido por configuração remota após login.
2. O host é montado dinamicamente no código.
3. O host está em um OBB/PAK baixado após login.
4. O host está codificado/transformado de forma que não aparece como URL ASCII simples.
5. `gameApiUrl` é apenas uma chave de configuração e não necessariamente o endpoint do browser.

Nenhuma dessas possibilidades foi provada ainda.

## 4. A camada de conta está na biblioteca nativa personalizada

A `libmenu.so` contém as mensagens de interface em inglês, português e indonésio relativas a:
- login com conta do site LegacyForge;
- ativação do telefone pelo gateway de download do site;
- revogação da ativação;
- uma conta por telefone por vez;
- conta banida/desabilitada;
- necessidade de verificação Discord;
- download posterior do OBB principal, patch e pacote de animações.

O APK também contém bibliotecas Android padrão de Google Play Services/Firebase/OneSignal, mas a presença dessas dependências não demonstra que o login LegacyForge seja feito pelo Google. O texto do cliente aponta para conta própria do site.

## 5. Recursos administrativos e tickets

Na `libmenu.so` há strings de uma interface de comandos administrativos de servidor, incluindo:
- `ServerCommands`
- `ServerCommandsVerified`
- `ServerCommandsUnverified`
- `ServerCommandsWaiting`
- `ServerCommandsDisabled`
- `Request dropped: not confirmed as admin, disabled, expired, invalid, or the server session changed.`
- `The server confirmed you as its admin.`
- `Sends commands to the joined server. Only a player the server itself confirms as its admin can use it`

Isso sugere uma interface que envia pedidos ao servidor e espera confirmação do próprio servidor para habilitar comandos. Não é prova de que o cliente consiga criar ou administrar um servidor por conta própria.

As strings `joinTicket`, `LegacyForge server ticket` e `Server Transfer Ticket` também aparecem, mas sem análise de referências cruzadas não é seguro afirmar que sejam o mesmo ticket nem descrever sua estrutura.

## 6. O que isso significa para hospedar um servidor

Estado atual da evidência:

| Pergunta | Resultado |
|---|---|
| O APK contém um servidor dedicado? | Não foi encontrado executável/binário de servidor no APK. |
| O cliente mantém o server browser padrão do ARK? | Sim, símbolos e URLs padrão estão presentes em `libUE4.so`. |
| Existe filtro próprio LegacyForge? | Sim, confirmado por strings de configuração e interface em `libmenu.so`. |
| Existe conta/ativação própria? | Sim, mensagens específicas confirmam o fluxo do site e ativação por telefone. |
| O host da API Forge está identificado? | Não. |
| Foi identificado o protocolo para um servidor Forge independente? | Ainda não. |
| Já é possível montar um servidor que apareça na lista oficial Forge? | Não com as informações disponíveis. |

## 7. Próximos passos que podem resolver as lacunas

1. **DEX:** decompilar os 66 DEX com JADX e identificar se algum downloader/serviço Android recebe configuração ou arquivos adicionais. A busca inicial não encontrou URL Forge nos DEX; os textos específicos estão concentrados na biblioteca nativa.
2. **ELF:** abrir `libmenu.so` e `libUE4.so` no Ghidra ou ferramenta equivalente; localizar referências cruzadas (XREFs) para `gameApiUrl`, `joinTicket`, `SettingsLegacyForgeServersOnly`, `AccountDeviceId`, `DownloadServerList` e `JoinServer`.
3. **Conteúdo baixado:** analisar, com uma conta legítima do usuário, os OBB/PAK recebidos pelo fluxo oficial do site. Não compartilhar tokens, credenciais ou dados pessoais.
4. **Tráfego autorizado:** observar somente a instalação de teste do próprio usuário durante login e abertura do server browser, registrando hostnames/caminhos e removendo tokens e identificadores pessoais antes de documentar.
5. **Servidor independente:** procurar documentação ou pacote de servidor disponibilizado pelo projeto. Sem binário de servidor e sem protocolo confirmado, não é correto prometer compatibilidade.

## 8. Ferramentas e limitações

- JADX é indicado para decompilar DEX/APK em Java aproximado, mas o próprio projeto alerta que nem todo código é recuperado perfeitamente: https://github.com/skylot/jadx
- A análise desta etapa foi estática: inventário ZIP, strings ASCII, cabeçalhos ELF e tabela dinâmica de símbolos.
- Não houve execução do jogo, autenticação, captura de tráfego, desmontagem de função nativa em Ghidra, nem acesso a endpoints privados.
- Este relatório não contém tokens, senhas, cookies, chaves privadas ou dados de contas.

## Conclusão desta etapa

A evidência mais sólida até agora é uma arquitetura híbrida: o cliente mantém as classes e endpoints de lista tradicionais do ARK Mobile, enquanto uma biblioteca personalizada adiciona conta/ativação LegacyForge, conteúdo próprio e filtro para servidores Forge. Ainda não há prova estática suficiente para afirmar que o Forge opera um master server totalmente independente ou para montar um servidor compatível.
