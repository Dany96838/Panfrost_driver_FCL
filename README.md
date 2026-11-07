# Panfrost Driver Plugin for Fold Craft Launcher

Projeto experimental para investigar e integrar PanVK/Panfrost como plugin de driver Vulkan no Fold Craft Launcher (FCL) 1.3.4.5.

## Alvo de teste

- POCO X7 Pro
- MediaTek Dimensity 8400-Ultra
- GPU ARM Mali-G720 MC7
- Android 16
- Sem root
- Não substituir nem modificar bibliotecas Vulkan do sistema

## Estado atual

A análise do APK oficial está em [AUDIT/FCL-1.3.4.5-APK-AUDIT.md](AUDIT/FCL-1.3.4.5-APK-AUDIT.md).

O APK do FCL contém código relacionado a DriverPlugin e seleção de GPU (incluindo os identificadores `driverLib`, `driverPath`, `driverGpu`, `GPU_MALI` e `fclPlugin_V2`). Não contém `libvulkan_panfrost.so`.

**Ainda não existe neste repositório um binário PanVK Android ARM64 comprovadamente compatível.** Portanto, este repositório não deve produzir ou distribuir um APK que apenas declare compatibilidade ou empacote uma biblioteca Vulkan diferente com outro nome.

## Próximas etapas

1. Extrair/confirmar o contrato completo de metadados e instalação de DriverPlugin no FCL 1.3.4.5.
2. Inspecionar os arquivos-fonte e binários PanVK que o usuário forneceu, incluindo arquitetura, dependências, símbolos e licenças.
3. Determinar se o PanVK disponível implementa a interface necessária para Android e para a UAPI do kernel Mali do dispositivo.
4. Preparar o projeto Android/Gradle e o empacotamento ARM64 somente após confirmar os requisitos.
5. Compilar, assinar e validar o APK do plugin.
6. Testar instalação e carregamento no FCL; depois testar Vulkan e Minecraft no dispositivo real.

## Regra de procedência

Este é o único repositório GitHub autorizado para o projeto: `Dany96838/Panfrost_driver_FCL`. Não copiar código-fonte de outros repositórios GitHub. Documentação técnica pública pode ser consultada e citada.