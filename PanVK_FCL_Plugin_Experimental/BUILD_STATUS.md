# Estado do protótipo

## Projeto Android

Estrutura Android preparada a partir do template FCLDriverPlugin-Turnip fornecido pelo usuário. O binário Freedreno do template foi excluído; o driver correto para este alvo é o `libvulkan_panfrost.so` extraído do pacote PanVK Android recebido.

O projeto preserva apenas os metadados de plugin observados no template (`fclPlugin=true` e `driver`). A compatibilidade completa do contrato FCL 1.3.4.5 ainda precisa ser confirmada no launcher real.

## Binário PanVK

Arquivo esperado no repositório:

`app/src/main/jniLibs/arm64-v8a/libvulkan_panfrost.so`

SHA-256 esperado:

`62c2b3f98ca987d5ab50b6f01e2d2c1c5b3ee995fe93666aa5da9415f65c3348`

O binário extraído do pacote fornecido foi conferido: ELF64 AArch64 Android, SONAME `libvulkan_panfrost.so`, tamanho 34,850,936 bytes e SHA-256 correspondente. O arquivo ainda não foi enviado ao caminho acima no GitHub; por isso, nenhum APK foi produzido.

## GitHub Actions

O workflow `.github/workflows/build-panvk-apk.yml` foi ajustado para:
- instalar Android SDK 35 e Build Tools 35.0.0;
- verificar SHA-256 e arquitetura ELF do driver antes de compilar;
- compilar a variante Release sem assinatura embutida;
- gerar uma chave RSA aleatória e temporária por execução;
- assinar e verificar o APK com essa chave;
- publicar o APK como artefato por 14 dias.

O build automático é disparado quando o arquivo binário exato é adicionado ou atualizado no caminho esperado. Alterações somente em documentação ou workflow não disparam builds inúteis.

## Compatibilidade no aparelho

O pacote anuncia suporte arquitetural universal Mali v6-v14 e exige Android API 35. O POCO X7 Pro com Immortalis-G720 MC7 é v12 e Android 16 satisfaz a API mínima, mas isso não prova compatibilidade específica. A validação fornecida informa que o build 122h passou 41/41 em outro dispositivo v12; o build 122i deste pacote não foi rerodado em v12.

Após compilar, ainda será necessário instalar o APK no FCL 1.3.4.5, confirmar que o launcher reconhece o plugin e testar a inicialização Vulkan no POCO X7 Pro. Não substituir o driver Vulkan do sistema.
