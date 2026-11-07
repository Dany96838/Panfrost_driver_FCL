# FCL 1.3.4.5 APK — análise inicial

Data da análise: 2026-11-07  
Arquivo analisado: Fold Craft Launcher_1.3.4.5.apk  
Tamanho: 168.725.101 bytes

## Evidências verificadas no APK

- O APK contém bibliotecas nativas em `lib/arm64-v8a/`, portanto inclui binários ARM64.
- Bibliotecas relevantes encontradas:
  - `libEGL_mesa.so`
  - `libfcl.so`
  - `libvkshim.so`
  - `libvulkan_check.so`
  - `libvulkan_freedreno.so`
- Não existe arquivo `libvulkan_panfrost.so` no APK analisado.
- A biblioteca `libvulkan_freedreno.so` tem ELF64 / AArch64 e tamanho aproximado de 9,4 MB.
- As classes DEX contêm referências a `com.mio.plugin.DriverPlugin`, `driverGpu`, `driverLib`, `driverPath`, `driver_gpu`, `driver_lib`, `GPU_MALI`, `GPU_ADRENO`, `fclPlugin` e `fclPlugin_V2`. Isso confirma que há código relacionado a plugins de driver e seleção de GPU no aplicativo.
- O APK contém `libvulkan_check.so`; a presença desse arquivo, isoladamente, não prova que o carregamento de um driver de terceiros funcione.

## O que ainda não está comprovado

- O formato completo e a versão exata do manifesto de plugin aceito pelo FCL 1.3.4.5.
- O fluxo de instalação/importação de um plugin de driver externo.
- Se o processo do FCL consegue carregar uma implementação PanVK/Panfrost no Android 16 deste dispositivo.
- A compatibilidade do PanVK com o kernel, UAPI e driver Mali/Kbase/CSF do POCO X7 Pro.
- Inicialização Vulkan real, criação de dispositivo, execução de shaders e estabilidade em Minecraft.
- Assinatura, permissões e empacotamento final do APK plugin.

## Conclusão

O FCL 1.3.4.5 possui código relacionado a plugins de driver e GPU, mas o APK analisado não contém PanVK/Panfrost. Não se deve declarar compatibilidade nem produzir um pacote que apenas renomeie outra biblioteca. A próxima etapa é identificar o contrato completo de DriverPlugin e obter/construir uma biblioteca PanVK Android ARM64 compatível, com todas as dependências e licenças verificadas.

## Restrições do projeto

- Único repositório GitHub do projeto: `Dany96838/Panfrost_driver_FCL`.
- Alvo: Fold Craft Launcher 1.3.4.5.
- Dispositivo-alvo informado: POCO X7 Pro, MediaTek Dimensity 8400-Ultra, GPU Mali-G720 MC7, Android 16, sem root.
- Não substituir nem modificar o driver Vulkan do sistema.
- Não importar código-fonte de outros repositórios GitHub. Documentação técnica pública pode ser consultada, respeitando licenças.
