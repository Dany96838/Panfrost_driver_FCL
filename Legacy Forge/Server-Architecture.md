# Legacy Forge 49.4 — foco em login e infraestrutura multiplayer

Amostra: `LegacyForge-49.4.apk`
SHA-256: `629e0ac137968e9fed2e0ad567a229ce062e89ebd33f2901eb9c23b3553fae80`

## 1. Identidade e assinatura

| Campo | Observação |
|---|---|
| Package | `com.legacyforge.ark` |
| Versão | `2.0.29` |
| versionCode | `152` |
| Certificado | autoassinado, sujeito `O=LegacyForge, CN=LegacyForge` |
| SHA-256 do certificado | `9F:9F:12:8B:F9:5A:E5:D8:02:74:66:0C:5C:6A:30:B2:81:13:FB:5E:11:A8:29:EE:2C:8B:2F:4E:82:F2:4A:CB` |
| Build | Unreal Engine 4.17.2 / Shipping |
| Debuggable | false |

O APK é uma distribuição separada do app oficial: o package ID é `com.legacyforge.ark`, embora várias classes Android antigas do downloader ainda usem o namespace `com.studiowildcard.wardrumstudios.ark`. Isso não é prova de que o login seja Google; é compatibilidade/legado do projeto Android.

## 2. Fluxo de conta e ativação

Strings de interface presentes em `libmenu.so` indicam:

- `Sign in with your LegacyForge website account. Multiplayer opens once you are signed in.`
- `This phone is not activated yet. Complete the download gateway on the website with this account, then tap Check again.`
- `This phone's activation was revoked. Complete the download gateway on the website again to activate it.`
- `Your account was signed in on another phone. One phone at a time: sign in here again to move it back.`
- Estados separados para credenciais inválidas, conta desativada/banida, sessão encerrada, rate limit, erro de rede e necessidade de verificação Discord.
- O fluxo de verificação Discord manda abrir o dashboard no site, obter um código e executar `/verify` no Discord.

**Conclusão comprovada:** o cliente implementa uma camada de conta/ativação própria do LegacyForge, com controle por dispositivo e verificação Discord para multiplayer.

**Ainda não comprovado:** se a ativação é vinculada a Android ID, chave gerada no Keystore, fingerprint do APK, token de instalação ou combinação desses fatores. A string `AccountDeviceId` existe, mas não revela sozinha qual identificador é enviado.

## 3. Download de conteúdo

Mensagem literal no cliente:

`Sign in with your LegacyForge account first. Then the game data downloads: the main OBB, the patch, then the LegacyForge animation pack.`

Também aparecem `legacyforge.pak`, prefixo `legacyforge-`, `animation pak` e diretório local `/ShooterGame/Saved/LegacyForge/`.

**Conclusão comprovada:** o APK é apenas uma parte da distribuição. O cliente espera baixar conteúdo grande depois do login, incluindo OBB principal, patch e pacote de animações. Portanto, analisar só o APK não revela todo o conteúdo nem toda a lógica do jogo.

## 4. Server browser e conexão

Strings/símbolos relevantes:

- `LegacyForge servers only`
- `On: show only LegacyForge servers. Off: show the game's unofficial servers.`
- `gameApiUrl`
- `joinTicket`
- `LegacyForge server ticket`
- `UUIServerView::DownloadStatsByURL`
- `UUIServerView::DownloadStatsByEntry`
- `UUIServerView::StatDownloadResponse`
- `UUIServerView::StatsDownloaded`
- `UUIServerView::StatsError`
- `FCurlHttpRequest::SetURL`
- `&port=`

Interpretação com níveis de confiança:

- **Alta:** o cliente tem filtro próprio para mostrar somente servidores LegacyForge ou, desligado, mostrar a lista de servidores não oficiais do jogo.
- **Alta:** há código para baixar estatísticas/metadata de servidor por URL ou entrada.
- **Média:** `gameApiUrl` parece ser uma configuração/identificador usado pela camada de API, mas a string isolada não demonstra seu valor nem endpoint.
- **Baixa/aberta:** `joinTicket` pode estar ligado ao ingresso/transferência de servidor; precisamos seguir referências de código antes de afirmar que seja token de autenticação.

A extração ASCII encontrou apenas o convite público do Discord e não encontrou uma URL HTTP(S) literal da API LegacyForge. Isso não prova que não exista backend: o endereço pode vir de configuração remota, ser montado em runtime, estar codificado/encriptado ou ser recebido após a autenticação.

O APK também contém referências herdadas às listas padrão do ARK:
- `arkdedicated.com/mobile/cache/officialserverlist.json`
- `arkdedicated.com/mobile/cache/unofficialserverlist.json`

Isso é coerente com a interface que alterna entre servidores LegacyForge e servidores não oficiais do jogo. Não prova, por si só, se os servidores Forge são listados por API própria, por metadados adicionados à lista padrão ou por um serviço intermediário.

## 5. O que o APK não contém

O inventário do ZIP mostra `libUE4.so`, `libmenu.so` e bibliotecas de suporte Android, mas nenhum executável de servidor dedicado separado. A amostra é um cliente Android ARM64, não um pacote de hospedagem de servidor.

Isso não impede a existência de servidores externos: apenas significa que o APK cliente não nos entrega o binário de servidor dedicado.

## 6. Próxima investigação

Prioridade técnica:

1. Usar JADX nos 66 DEX para separar dependências Google/Firebase/OneSignal das classes de aplicação e identificar o downloader Android.
2. Abrir `libmenu.so` no Ghidra e seguir referências cruzadas de `gameApiUrl`, `joinTicket`, `AccountDeviceId`, `AccountNeedsActivation` e funções `UUIServerView`.
3. Identificar o fluxo de chamada que monta URLs e parâmetros `port`, sem tentar reutilizar tokens ou contornar autenticação.
4. Depois de autorização e login legítimos, observar somente o tráfego da própria instalação de teste para registrar hostnames, caminhos e formato de resposta; remover tokens e IDs pessoais dos relatórios.
5. Descobrir se existe um pacote oficial de servidor ou documentação pública do LegacyForge. Se não houver, avaliar um servidor independente compatível com o protocolo público, sem imitar endpoints privados nem acessar servidores de terceiros.

## 7. Limites desta etapa

Análise estática local do APK e dos metadados ELF/Manifest. Nenhuma sessão foi iniciada, nenhum tráfego foi capturado e nenhum endpoint privado foi acessado. Strings de interface não equivalem a prova de implementação; conclusões acima foram rotuladas conforme a evidência disponível.
