# Legacy Forge 49.4 — análise aprofundada, etapa 2

Data da análise: 2026-11-17
Amostra: `LegacyForge-49.4.apk`
SHA-256: `629e0ac137968e9fed2e0ad567a229ce062e89ebd33f2901eb9c23b3553fae80`
Tamanho: 89,394,617 bytes

## Resumo executivo

A segunda passada confirma que a maior parte da personalização LegacyForge visível nas strings analisadas está na biblioteca nativa Unreal `libmenu.so`, e não em código Java/Kotlin próprio facilmente identificável nos DEX.

O APK contém código cliente que:
- exige uma conta LegacyForge para liberar multiplayer;
- exige ativação do telefone para recursos single-player;
- baixa dados externos (OBB principal, patch e pacote de animações);
- oferece filtro para exibir apenas servidores LegacyForge ou servidores não oficiais padrão;
- possui funções de download de estatísticas de servidor e strings associadas a ticket de transferência.

A amostra ainda não revela um domínio HTTP(S) explícito para a API LegacyForge. A única URL HTTP(S) de serviço claramente encontrada na biblioteca nativa é o convite Discord; outras URLs são documentação/fontes de bibliotecas incorporadas. Isso não exclui endpoint montado em runtime, entregue por configuração remota ou presente no conteúdo baixado.

## 1. Rechecagem do inventário

- 66 DEX: `classes.dex` até `classes66.dex`.
- `libUE4.so`: 120,782,624 bytes.
- `libmenu.so`: 54,200,728 bytes.
- `libgnustl_shared.so`: 1,514,928 bytes.
- `libmenu.so` é ELF64, little-endian, AArch64, shared object.
- `libmenu.so` declara dependências Android EGL, GLESv3, android, log, m, dl e libc.
- O inventário ZIP não mostrou OBB nem arquivo `.pak` embarcado como entrada do APK. O código, entretanto, contém strings que apontam para `legacyforge.pak` e para conteúdo baixado separadamente.

## 2. Descoberta adicional: ativação também condiciona single-player

String literal no cliente:

`Single-player features open once this phone is activated: download LegacyForge from the website, install it, then sign in on the Account page.`

Isso corrige uma suposição possível da primeira análise: a ativação não é descrita apenas como requisito para multiplayer. A mensagem do cliente afirma explicitamente que recursos single-player só abrem depois da ativação do telefone e login na página Account.

Outras mensagens:
- `This phone is not activated yet. Complete the download gateway on the website with this account, then tap Check again.`
- `This phone's activation was revoked. Complete the download gateway on the website again to activate it.`
- `This phone could not create or use its activation key.`
- `Your account was signed in on another phone. One phone at a time: sign in here again to move it back.`
- `Cannot reach the LegacyForge server. Trying again every minute.`

Interpretação: existe uma etapa de ativação/download gateway e um mecanismo de estado de conta/dispositivo. A frase “one phone at a time” indica política de sessão/ativação por telefone, mas não revela qual identificador de hardware é usado.

## 3. Distribuição de dados do jogo

String literal:

`Sign in with your LegacyForge account first. Then the game data downloads: the main OBB, the patch, then the LegacyForge animation pack.`

Também aparecem referências a:
- `legacyforge.pak`
- prefixo de arquivos `legacyforge-`
- diretório `/ShooterGame/Saved/LegacyForge/`
- armazenamento de backups em `/sdcard/Documents/LegacyForge`
- função nativa de montagem de OBB `FAndroidPlatformFile::MountOBB`.

Conclusão: a instalação não está completa apenas com o APK. A distribuição tem ao menos três categorias de conteúdo baixado após login. Para analisar as criaturas, estruturas e animações, será necessário obter os arquivos de dados autorizadamente a partir da instalação do próprio usuário; o APK sozinho não contém esses assets completos.

## 4. Navegador de servidores

Strings e símbolos observados em `libmenu.so`:
- `LegacyForge servers only`
- `On: show only LegacyForge servers. Off: show the game's unofficial servers.`
- `gameApiUrl`
- `joinTicket`
- `LegacyForge server ticket`
- `UUIServerView::DownloadStatsByURL(FString const&)`
- `UUIServerView::DownloadStatsByEntry(FServerListEntry const&)`
- `UUIServerView::StatDownloadResponse(...)`
- `UUIServerView::StatsDownloaded()`
- `UUIServerView::StatsError()`
- `FCurlHttpRequest::SetURL(FString const&)`
- `&port=`

O que é possível afirmar:
1. O cliente possui uma opção que filtra a lista para mostrar somente servidores LegacyForge.
2. O cliente tem rotinas de download de estatísticas associadas a uma URL ou entrada da lista.
3. A biblioteca tem suporte a requisições HTTP via Unreal/Curl.
4. A presença de `gameApiUrl` indica um identificador/campo relacionado à API, mas não informa o valor da URL.
5. `joinTicket` e `LegacyForge server ticket` existem como strings; ainda não foi provado se são ticket de sessão, transferência de personagem, ou outro fluxo.

O APK também contém URLs padrão do ARK:
- `arkdedicated.com/mobile/cache/officialserverlist.json`
- `arkdedicated.com/mobile/cache/unofficialserverlist.json`

O texto da opção LegacyForge é consistente com um navegador que consegue alternar entre uma lista filtrada Forge e servidores não oficiais do jogo. Não é suficiente para concluir se a lista Forge vem de API própria, de uma lista padrão enriquecida, ou de uma camada proxy.

## 5. O que não apareceu na análise estática

Na extração de strings ASCII da biblioteca `libmenu.so`, não apareceu domínio HTTP(S) legível da API LegacyForge. Apareceram:
- convite público do Discord do projeto;
- links de documentação de bibliotecas incorporadas;
- URLs dos serviços OneSignal nos DEX (SDK de notificações);
- URLs e escopos Google Play Games nos DEX/SDKs.

A existência de escopos Google Play Games em dependências não prova que o login LegacyForge use Google. O cliente exibe claramente um fluxo de conta próprio.

A análise de strings é limitada: URLs podem estar codificadas, comprimidas, divididas, construídas dinamicamente ou recebidas do servidor depois do login.

## 6. DEX: evidência de código Java de terceiros/legado

Os DEX contêm principalmente referências a:
- classes Android antigas de downloader/OBB do namespace `com.studiowildcard.wardrumstudios.ark`;
- SDKs Google Play Games;
- OneSignal;
- dependências comuns de autenticação/social.

A busca por strings/classes próprias LegacyForge nos DEX não encontrou uma implementação Java evidente de `gameApiUrl`, `joinTicket` ou do fluxo de conta. Isso é consistente com a lógica principal ter sido implementada no código nativo Unreal (`libmenu.so`), mas não prova que toda a lógica esteja exclusivamente ali.

## 7. Próximos passos necessários para ir além de strings

1. **JADX**: decompilar os 66 DEX, confirmar as Activities/Services do downloader, permissões, OBB e dependências SDK. JADX suporta APK/DEX multi-DEX, mas pode falhar em parte da decompilação.
2. **Ghidra**: importar `libmenu.so` como AArch64 ELF, analisar strings e referências cruzadas para os textos de conta, `gameApiUrl`, `joinTicket` e métodos `UUIServerView`. O ELF parece stripped na tabela de símbolos dinâmica, então a análise exigirá autoanálise e busca de referências a strings.
3. **Dados baixados**: examinar metadados e arquivos OBB/PAK obtidos legitimamente após login, sem compartilhar tokens, credenciais ou arquivos de conta.
4. **Observação de rede da própria instalação**: com uma conta e aparelho autorizados, registrar apenas hostnames, caminhos e estrutura de resposta, removendo tokens, cookies, IDs e dados pessoais. Não tentar contornar login, ativação ou controles de acesso.
5. **Servidor**: localizar documentação ou binário de servidor distribuído pelo projeto. Até agora o APK analisado é um cliente Android ARM64 e não contém um executável de servidor dedicado separado.

## Conclusão técnica atual

O LegacyForge parece combinar um cliente ARK UE4 modificado com uma camada própria de conta/ativação, entrega de conteúdo e filtragem de servidores. O APK dá evidência concreta desses componentes, mas ainda não fornece o endereço da API nem o software de servidor. Portanto, ainda não há base técnica para afirmar que já podemos iniciar um servidor compatível apenas com esse APK.

## Ferramentas

- JADX: https://github.com/skylot/jadx
- Ghidra: https://github.com/NationalSecurityAgency/ghidra
- Apktool: https://github.com/iBotPeaches/Apktool

## Limite da etapa

Análise estática de ZIP, DEX strings, ELF headers/dependencies e strings ASCII. Não foi feita descompilação integral via JADX, análise de fluxo no Ghidra, captura de tráfego, login real ou execução do jogo. Este relatório não deve ser interpretado como confirmação de endpoints privados.
