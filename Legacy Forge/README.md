# Legacy Forge — análise estática do APK 49.4

## Amostra analisada

- Arquivo recebido: `LegacyForge-49.4.apk`
- SHA-256: `629e0ac137968e9fed2e0ad567a229ce062e89ebd33f2901eb9c23b3553fae80`
- Tamanho: 89,394,617 bytes
- Package ID: `com.legacyforge.ark`
- Version name: `2.0.29`
- Version code: `152`
- Engine declarado no Manifest: Unreal Engine `4.17.2`
- Build configuration: `Shipping`
- ABI presente: `arm64-v8a`
- `android:debuggable`: false nas Activities examinadas
- APK não foi alterado. Esta pasta guarda notas e resultados; não contém o APK nem dados privados de contas.

## Estrutura observada

- 66 arquivos DEX (`classes.dex` até `classes66.dex`).
- `lib/arm64-v8a/libUE4.so` (~120.8 MB descompactado).
- `lib/arm64-v8a/libmenu.so` (~54.2 MB descompactado).
- `lib/arm64-v8a/libgnustl_shared.so`.
- O APK não inclui os grandes pacotes de conteúdo do jogo como assets normais; as mensagens do próprio cliente indicam download posterior dos OBBs/pacotes.

## Achados fortes no código nativo (`libmenu.so`)

1. Existe uma camada específica Legacy Forge integrada ao cliente. Strings encontradas incluem:
   - `LegacyForge account`
   - `gameApiUrl`
   - `joinTicket`
   - `legacyforge.pak`
   - `/ShooterGame/Saved/LegacyForge/`
   - `/sdcard/Documents/LegacyForge`

2. O fluxo de conta/dispositivo é próprio:
   - O cliente pede login com conta do site LegacyForge.
   - O texto do cliente diz que o multiplayer só abre após login.
   - Há estados de ativação do telefone, revogação de ativação, conta desabilitada/banida, sessão encerrada, login em outro telefone e limite de um telefone por vez.
   - Há estado de verificação Discord; texto do cliente instrui obter um código no dashboard do site e usar `/verify` no Discord.
   - Mensagem explícita: após login, os dados baixados são o OBB principal, o patch e o pacote de animações Legacy Forge.

3. O browser de servidores foi modificado:
   - Opção `LegacyForge servers only`.
   - Texto: ligado mostra apenas servidores LegacyForge; desligado mostra os servidores não oficiais do próprio jogo.
   - Há símbolos nativos `UUIServerView::DownloadStatsByURL`, `DownloadStatsByEntry`, `StatDownloadResponse`, `StatsDownloaded` e `StatsError`.
   - Isso confirma código para buscar/receber estatísticas de servidores por URL/entrada. Ainda não revela, sozinho, o endereço do backend nem prova que exista um executável de servidor dedicado no APK.

4. Há referências a `Server Transfer Ticket` e `joinTicket`. Não concluir ainda que são o mesmo mecanismo do ticket de autenticação de sessão: é necessário rastrear os usos/call sites.

5. A biblioteca `libmenu.so` é ELF64 AArch64 e depende de bibliotecas Android comuns (EGL, GLESv3, android, log, m, dl, c). Build ID:
   `7a8d7d1a15978b0c95a68be74d4a87ff6e485295`.

## Achados do Manifest

- Package ID: `com.legacyforge.ark`.
- Min SDK 24; target SDK 37.
- `BuildConfiguration=Shipping`.
- `bHasOBBFiles=true`, `bVerifyOBBOnStartUp=true`, `bPackageDataInsideApk=false`.
- Mantém componentes Google Play Services/Firebase no Manifest, mas isso não significa que o login de conta Forge use Google.
- O Manifest declara o app como não-debuggable nas Activities examinadas.

## O que ainda não está comprovado

- Domínio/base URL exato da API Legacy Forge. A string `gameApiUrl` existe, mas não apareceu como URL literal legível na extração ASCII inicial. Pode ser carregada de configuração remota, montada em runtime, armazenada em outro formato ou obtida do conteúdo baixado.
- Formato dos endpoints, esquema de autenticação, geração/validação de tokens e política de ativação.
- Como a lista Legacy Forge é obtida e como os servidores são identificados/filtrados.
- Se o projeto fornece um servidor dedicado próprio, um fork do servidor ARK, ou apenas uma camada de autenticação/listagem em cima do protocolo existente.
- Se o conteúdo de servidor é baixado separadamente e quais arquivos são necessários para hospedar um mundo compatível.

## Próximas etapas técnicas

1. Decompilar os 66 DEX com JADX e identificar classes próprias, componentes de login, downloader, Firebase/OneSignal e carregamento de arquivos.
2. Analisar `libmenu.so` no Ghidra: xrefs para `gameApiUrl`, `joinTicket`, `legacyforge-`, estados de conta e funções `UUIServerView`.
3. Comparar o fluxo de server browser do cliente com a lista oficial/unofficial padrão do ARK.
4. Inspecionar metadados e estrutura dos OBBs/pacotes baixados, sem publicar tokens, credenciais ou conteúdo privado.
5. Só então desenhar uma arquitetura de servidor independente, se o protocolo e os arquivos necessários permitirem.

## Ferramentas de referência

- JADX: https://github.com/skylot/jadx
- Apktool: https://github.com/iBotPeaches/Apktool
- Ghidra: https://github.com/NationalSecurityAgency/ghidra

## Nota de método

Este relatório separa strings/símbolos efetivamente observados de hipóteses. A análise atual é estática e parcial; não foi feita captura de tráfego, login real, nem execução do jogo. Não armazenar aqui senhas, tokens, chaves privadas ou dados pessoais.
