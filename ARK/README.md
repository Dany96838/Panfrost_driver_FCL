# ARK Mobile Legacy — build auxiliar

Esta pasta é independente do projeto Panfrost/FCL. Ela contém somente o fluxo auxiliar para reconstruir o APK legado do ARK com `android:debuggable="true"`, alinhar e assinar com APK Signature Scheme v2/v3.

## Entrada

Envie o APK original para `ARK/ark-original.apk`. Não desinstale a instalação original do jogo: o APK recompilado terá uma chave de assinatura diferente.

## Compilação

No GitHub, abra **Actions** → **Build ARK debuggable APK** → **Run workflow**. Ao terminar, baixe o artefato `ark-debuggable-signed`.

A compilação usa Apktool e Android Build Tools no runner do GitHub e verifica a assinatura antes de publicar o artefato.

**Limitações:** ativar `debuggable` não garante que o ARK aceite configurações INI nem que o controle Xbox possa ser remapeado. O pacote também pode ter verificações próprias de integridade/assinatura. Faça backup dos dados antes de qualquer reinstalação.
