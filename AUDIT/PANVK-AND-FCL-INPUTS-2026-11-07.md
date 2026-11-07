# Auditoria dos arquivos recebidos — PanVK / FCL

Data: 2026-11-07

## Biblioteca PanVK
- Arquivo: libvulkan_panfrost.so
- Tamanho: 34.850.936 bytes
- SHA-256: 62c2b3f98ca987d5ab50b6f01e2d2c1c5b3ee995fe93666aa5da9415f65c3348
- ELF64, AArch64, little-endian, shared object
- SONAME: libvulkan_panfrost.so
- NDK Android API 29; meta.json declara minApi 35
- backend: panvk-kbase; kernelInterface: mali_kbase
- profile: universal-v6-v14; patch p0175
- prerelease=true; published=false

O pacote declara suporte a Mali v6-v14. O Mali-G720 do POCO X7 Pro está na classe v12, portanto dentro da faixa declarada. Porém, o VALIDATION.json informa que v12 foi testado num build anterior (122h), não no build atual 122i. Não há validação no POCO X7 Pro específico.

Dependências ELF declaradas: liblog.so, libnativewindow.so, libsync.so, libm.so, libz.so, libdl.so, libc.so. RUNPATH: $ORIGIN/../../android_stub. A disponibilidade/resolução real dessas dependências no sandbox do FCL ainda precisa ser testada.

## Projeto FCLDriverPlugin-Turnip recebido
- Projeto Android Gradle/Kotlin.
- Manifesto contém meta-data fclPlugin=true e driver.
- O projeto original empacota lib/arm64-v8a/libvulkan_freedreno.so, ou seja, uma biblioteca Turnip/Freedreno, não PanVK.
- build.gradle.kts usa applicationIdSuffix .turnip2432 e nome Turnip 24.3.2.
- Não contém APK final dentro do ZIP; contém apenas output-metadata.json.
- O protótipo PanVK troca a biblioteca nativa e atualiza nome/applicationId, conservando somente os metadados observados no template.

## Limitações
- Não se inventou driver_lib ou driver_gpu no manifesto, pois o contrato exato não está confirmado.
- Não foi possível compilar neste ambiente: não há Gradle instalado, Android SDK, AAPT, apksigner ou zipalign.
- O projeto preparado é fonte experimental, não um APK instalável.
- Testes no FCL 1.3.4.5 e no POCO X7 Pro são obrigatórios antes de declarar funcionamento.
