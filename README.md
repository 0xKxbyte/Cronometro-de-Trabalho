# Cronometro de Trabalho - Retorno atraves da Morte

[![Python Version](https://shields.io)](https://python.org)
[![Platform](https://shields.io)](https://microsoft.com)
[![License](https://shields.io)](https://opensource.org)

![Banner Re:Zero](https://pixelz.cc)

Cronometro de produtividade integrado ao sistema operacional Windows que utiliza elementos sonoros e visuais tematicos baseados na habilidade Return by Death do personagem Natsuki Subaru da obra Re:Zero - Starting Life in Another World.

---

## Funcionalidades

- Contagem regressiva customizavel para ciclos de trabalho.
- Disparo de notificacoes nativas atraves da API do Windows ao esgotar o tempo.
- Alarme sonoro obrigatorio utilizando o efeito sonoro de suspense e agonia do Return by Death (Call of the Witch).
- Interface em linha de comando otimizada para execucao rapida.

---

## Requisitos de Sistema

O ambiente de execucao exige configuracoes especificas de software:

- **Python 3.11 ou Python 3.12:** OBRIGATORIO ter uma destas duas versoes instaladas no sistema. Versoes anteriores ou posteriores nao possuem compatibilidade garantida com as bibliotecas de chamada de API utilizadas.
- **Sistema Operacional:** Windows 10 ou Windows 11 (devido ao uso da API de notificacoes `winrt` / `win10toast`).

---

## Dependencias e Bibliotecas

O projeto faz uso de pacotes especificos para interacao com o hardware e sistema operacional. As principais dependencias sao:

- **[Win10Toast](https://pypi.org):** Responsavel por enviar os alertas visuais para a central de notificacoes do Windows.
- **[Playsound](https://pypi.org):** Biblioteca utilizada para reproduzir o alarme sonoro em formato MP3/WAV de forma sincrona ou assincrona.

Instale todas as dependencias obrigatorias utilizando o comando:

---

## Estrutura do Arquivo de Audio

O alarme do cronometro funciona associado ao tema de morte do personagem. Para o funcionamento correto, o arquivo de audio deve ser mantido no diretorio correspondente:

- Caminho do arquivo: `Alarme1S.mp3`
- Origem do som: Trilha sonora oficial de Re:Zero (Efeito sonoro conhecido como *Call of the Witch* / *Whoaa Whoaa*).

---

## Como Executar o Projeto

1. Certifique-se de que o Python 3.11 ou 3.12 esta devidamente configurado nas variaveis de ambiente (PATH) do seu Windows.
2. Clone o repositorio para a sua maquina local:
   ```bash
   git clone https://github.com
   ```
3. Acesse a pasta do projeto:
   ```bash
   cd CronometroTrabalho
   ```
4. Execute o script principal:
   ```bash
   python hivax.py
   ```

---

## Licenca

Este projeto esta sob a licenca MIT. Veja o arquivo [LICENSE](https://opensource.org) para mais detalhes.
