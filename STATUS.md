# Status de desenvolvimento

Atualizado em 2026-11-07.

## Feito nesta sessão

- Analisado o APK do Fold Craft Launcher 1.3.4.5 enviado pelo usuário.
- Confirmada a presença de código DEX relacionado a `DriverPlugin`, `driverLib`, `driverPath`, `driverGpu`, `GPU_MALI` e `fclPlugin_V2`.
- Inventariadas as bibliotecas ARM64 do APK.
- Confirmado que o APK não inclui `libvulkan_panfrost.so`.
- Registrada a auditoria em `AUDIT/FCL-1.3.4.5-APK-AUDIT.md`.

## Bloqueadores para gerar um APK de driver real

- Contrato completo do manifesto/instalador FCL ainda precisa ser confirmado.
- Não há no repositório uma biblioteca PanVK Android ARM64 pronta para empacotar.
- Não foi comprovada compatibilidade com a UAPI/kernel Mali do POCO X7 Pro.
- Dependências, símbolos ELF, alinhamento, licença e carregamento em processo ainda precisam ser verificados.

## Critério para chamar o APK de funcional

Só marcar como funcional depois de confirmar instalação pelo FCL 1.3.4.5, carregamento da biblioteca ARM64, inicialização Vulkan, criação de dispositivo e teste real no POCO X7 Pro. Até lá, qualquer APK é apenas protótipo experimental e deve ser rotulado assim.