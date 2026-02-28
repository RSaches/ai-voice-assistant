# Assistente de Voz com IA - JARVIS

## Sobre o Projeto
O **JARVIS** é um assistente de voz inteligente desenvolvido para facilitar a interação com dispositivos e realizar tarefas automatizadas. Utilizando tecnologias de ponta como **SpeechRecognition**, **PyAudio**, e **IA generativa** (Google GenAI e Anthropic), o JARVIS é capaz de entender comandos de voz, responder perguntas e executar ações de forma eficiente e segura.

---

## Recursos Principais
- **Reconhecimento de Fala**: Com o uso do SpeechRecognition e PyAudio, o JARVIS pode entender comandos de voz com alta precisão.
- **Síntese de Voz**: Utiliza o `edge-tts` para gerar respostas em áudio com vozes naturais.
- **Integração com IA**: Conecte-se a APIs de IA como Google GenAI e Anthropic para respostas inteligentes e personalizadas.
- **Controle de Dispositivos**: Controle dispositivos conectados e realize tarefas automatizadas com comandos de voz.
- **Personalização de Voz**: Escolha entre diferentes vozes para personalizar a experiência do usuário.

---

## Pré-requisitos
Certifique-se de que você possui os seguintes requisitos instalados:

- **Python 3.10+**
- **Pip** (gerenciador de pacotes do Python)
- **PortAudio** (para suporte ao PyAudio)

### Instalação do PortAudio
#### **Windows**
1. Instale o Python 3.10+.
2. Instale o PortAudio e o PyAudio:
   ```powershell
   pip install pip setuptools wheel
   pip install pyaudio
   ```

#### **Linux (Ubuntu)**
1. Atualize os pacotes e instale as dependências do sistema:
   ```bash
   sudo apt-get update
   sudo apt-get install -y portaudio19-dev python3-pyaudio
   ```
2. Instale as dependências do Python:
   ```bash
   python3 -m pip install --upgrade pip setuptools wheel
   python3 -m pip install -r requirements.txt
   ```

#### **macOS**
1. Instale o PortAudio via Homebrew:
   ```bash
   brew install portaudio
   export LDFLAGS="-L/usr/local/opt/portaudio/lib"
   export CPPFLAGS="-I/usr/local/opt/portaudio/include"
   ```
2. Instale as dependências do Python:
   ```bash
   python3 -m pip install --upgrade pip setuptools wheel
   python3 -m pip install -r requirements.txt
   ```

---

## Configuração

### 1️⃣ **Adicione suas Chaves de API**
O JARVIS utiliza APIs de IA para fornecer respostas inteligentes. Para configurar as chaves de API:

1. Crie um arquivo `.env` na raiz do projeto.
2. Adicione as seguintes variáveis ao arquivo `.env`:
   ```env
   GOOGLE_GENAI_API_KEY=your_google_genai_api_key
   ANTHROPIC_API_KEY=your_anthropic_api_key
   ```
3. Substitua `your_google_genai_api_key` e `your_anthropic_api_key` pelas suas chaves de API.

### 2️⃣ **Escolha a Voz do Assistente**
Você pode personalizar a voz do JARVIS utilizando o `edge-tts`. Para isso:

1. No arquivo de configuração `config/settings_manager.py`, localize a seção de configuração de voz.
2. Altere o valor da variável `VOICE` para a voz desejada. Exemplo:
   ```python
   VOICE = "en-US-JennyNeural"
   ```
3. Consulte a [documentação do edge-tts](https://github.com/rany2/edge-tts) para uma lista completa de vozes disponíveis.

---

## Como Usar

1. **Inicie o JARVIS**:
   ```bash
   python avatar_ia.py
   ```
2. **Diga um comando**: Fale com o JARVIS e ele responderá com base nos seus comandos e nas APIs configuradas.
3. **Personalize**: Ajuste as configurações no arquivo `config/settings_manager.py` para personalizar a experiência.

---

## Segurança

O JARVIS foi projetado com segurança em mente. Aqui estão algumas práticas recomendadas:

- **Proteja suas chaves de API**: Nunca compartilhe o arquivo `.env` publicamente.
- **Atualize regularmente**: Mantenha suas dependências e o JARVIS atualizados para garantir a segurança.
- **Revise permissões**: Certifique-se de que as permissões das suas chaves de API estão configuradas corretamente.

---

## Contribuindo
Contribuições são bem-vindas! Siga os passos abaixo para contribuir:

1. Faça um fork do repositório.
2. Crie um branch para sua feature ou correção de bug:
   ```bash
   git checkout -b minha-feature
   ```
3. Faça suas alterações e commit:
   ```bash
   git commit -m "Adiciona minha nova feature"
   ```
4. Envie suas alterações:
   ```bash
   git push origin minha-feature
   ```
5. Abra um Pull Request no repositório original.

---

## Licença
Este projeto está licenciado sob a licença [MIT](LICENSE).

---

## Contato
Se você tiver dúvidas ou sugestões, entre em contato:

- **Autor**: Sanches Rafael
- **Email**: isanchess.ia@gmail.com

---

Aproveite o JARVIS e torne sua vida mais produtiva com a ajuda da inteligência artificial! 🚀
