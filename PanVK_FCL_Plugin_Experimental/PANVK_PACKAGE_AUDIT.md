# Auditoria do pacote PanVK recebido

- Binário: `libvulkan_panfrost.so` (34,850,936 bytes)
- SHA-256: `62c2b3f98ca987d5ab50b6f01e2d2c1c5b3ee995fe93666aa5da9415f65c3348`
- ELF: 64-bit AArch64 Android; SONAME `libvulkan_panfrost.so`
- minApi declarado: 35; ABI `android-aarch64-bionic`
- Backend/kernel interface: `panvk-kbase` / `mali_kbase`
- Perfil declarado: `universal-v6-v14`; patch p0175; prerelease=true; published=false
- A validação incluída relata testes v9, v11, v14 e um build anterior v12; não confirma o binário atual 122i no v12.

## Alvo POCO X7 Pro

A GPU Mali-G720 é arquitetura v12 e está na faixa declarada, mas não há comprovação de teste do binário atual neste aparelho/kernel/FCL. O pacote declara v15 não totalmente suportada.

## Dependências

`DT_NEEDED`: liblog.so, libnativewindow.so, libsync.so, libm.so, libz.so, libdl.so, libc.so. RUNPATH: `$ORIGIN/../../android_stub`. A resolução em runtime precisa ser testada no sandbox Android/FCL.

Este pacote é prerelease. A inspeção estática não comprova inicialização Vulkan real.
