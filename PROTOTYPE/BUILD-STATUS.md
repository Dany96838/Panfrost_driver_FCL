# Protótipo PanVK — estado

O projeto fonte experimental foi preparado localmente a partir do ZIP FCLDriverPlugin-Turnip fornecido pelo usuário. Foi substituído o binário nativo Freedreno/Turnip pelo `libvulkan_panfrost.so` do pacote PanVK fornecido. O manifesto conserva os campos observados no template: `fclPlugin=true` e `driver`. O applicationId e o nome de exibição foram alterados para identificar o protótipo PanVK.

O binário foi inspecionado como ELF64 AArch64; SHA-256 e dependências estão em `AUDIT/PANVK-AND-FCL-INPUTS-2026-11-07.md`.

**Importante:** ainda não é APK compilado nem comprovadamente funcional. O ambiente atual não tem Gradle nem Android SDK/AAPT/apksigner/zipalign. O contrato completo do plugin e a resolução de dependências em runtime precisam ser confirmados. O teste no FCL 1.3.4.5 e no POCO X7 Pro é obrigatório.