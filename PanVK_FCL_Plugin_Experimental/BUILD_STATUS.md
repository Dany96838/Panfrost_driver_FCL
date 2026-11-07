# Estado do protótipo

Estrutura Android preparada a partir do template FCLDriverPlugin-Turnip fornecido pelo usuário. O binário Freedreno não deve ser usado para Mali; o alvo correto é o `libvulkan_panfrost.so` recebido.

O projeto mantém os metadados observados no template (`fclPlugin=true` e `driver`), sem inventar campos de integração não confirmados.

O binário nativo PanVK ainda precisa ser colocado em `app/src/main/jniLibs/arm64-v8a/libvulkan_panfrost.so`. O projeto-fonte original contém esse arquivo, mas a API de conteúdo do GitHub disponível nesta sessão não oferece envio direto de arquivo binário local. Portanto, o workflow remoto não poderá produzir um APK funcional até o binário ser adicionado.

Mesmo após compilar, será necessário testar instalação e carregamento no FCL 1.3.4.5 e inicialização Vulkan no POCO X7 Pro.
