# Tradutor de Áudio Avançado

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.38.0-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

Um aplicativo web construído com **Streamlit** que transcreve áudios em português e traduz o texto para diversos idiomas usando **Google Speech Recognition** e **Gemini AI**. O projeto suporta arquivos de áudio MP3 e WAV (máximo de 1 minuto) e oferece uma interface moderna e intuitiva com tema escuro futurista.

## 🎯 Funcionalidades
- **Transcrição de Áudio**: Converte áudios em português para texto usando Google Speech Recognition.
- **Tradução de Texto**: Traduz o texto transcrito para idiomas como inglês, espanhol, francês, alemão, japonês, entre outros, usando Gemini AI.
- **Pré-visualização de Áudio**: Permite ouvir o áudio carregado antes do processamento.
- **Download de Resultados**: Baixe a transcrição e a tradução como arquivos de texto.
- **Interface Intuitiva**: Layout centralizado com expanders para resultados e informações, estilizado com um tema escuro e efeitos visuais modernos.

## 📸 Captura de Tela
*(Adicione uma captura de tela da interface aqui, se desejar. Exemplo: `<img src="screenshots/interface.png" alt="Interface do Tradutor de Áudio" width="600"/>`)*

## 🚀 Como Usar

### Pré-requisitos
- **Python 3.8+**
- **FFmpeg** instalado e adicionado ao PATH do sistema
- **Chave API do Gemini** (obtida no Google Cloud Console ou plataforma Gemini)
- Conexão com a internet

### Instalação
1. **Clone o repositório**:
   ```bash
   git clone https://github.com/seu-usuario/seu-repositorio.git
   cd seu-repositorio
Crie e ative um ambiente virtual:
bash
```
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate   # Windows
```
Instale as dependências:
```
pip install -r requirements.txt
```
Configure a chave API do Gemini:
Crie um arquivo .env na raiz do projeto com o seguinte conteúdo:
```
GEMINI_API_KEY=sua_chave_api_aqui
```
Substitua sua_chave_api_aqui pela sua chave obtida na plataforma Gemini.

Instale o FFmpeg:
Windows: Baixe em ffmpeg.org e adicione ao PATH.
Mac: brew install ffmpeg
Linux: sudo apt install ffmpeg
Verifique a instalação: ffmpeg -version
Executando o Aplicativo

Inicie o aplicativo Streamlit:
```
streamlit run main.py
```
Acesse a interface no navegador em http://localhost:8501.
Uso
Faça upload de um arquivo de áudio (MP3 ou WAV, até 1 minuto).
Selecione o idioma de destino (ex.: Inglês, Espanhol, Japonês).
Clique em Processar Áudio para transcrever e traduzir.
Visualize os resultados nos expanders e baixe a transcrição e/ou tradução.
Clique em Mostrar Informações e Instruções para mais detalhes ou para reiniciar o aplicativo.
📂 Estrutura do Projeto
text

```
seu-repositorio/
├── main.py              # Código principal do aplicativo Streamlit
├── requirements.txt     # Dependências do projeto
├── .env                # Arquivo de configuração da chave API (não versionado)
├── temp_audio/         # Diretório temporário para arquivos de áudio (criado automaticamente)
├── venv/               # Ambiente virtual (não versionado)
├── README.md           # Este arquivo
```
🛠️ Dependências
As dependências estão listadas no requirements.txt:
```
streamlit==1.38.0
speechrecognition==3.10.4
pydub==0.25.1
google-generativeai==0.8.2
python-dotenv==1.0.1
```
🔧 Tecnologias Utilizadas
Streamlit: Framework para construção da interface web.
Google Speech Recognition: Para transcrição de áudio.
Gemini AI: Para tradução de texto.
FFmpeg: Para processamento de arquivos de áudio.
Pydub: Para manipulação de áudio em Python.
Python-dotenv: Para gerenciamento de variáveis de ambiente.
🤝 Como Contribuir
Faça um fork do repositório.
Crie um branch para sua feature: git checkout -b minha-feature.
Commit suas alterações: git commit -m "Adiciona minha feature".
Faça push para o branch: git push origin minha-feature.
Abra um Pull Request no GitHub.
⚠️ Notas
O áudio deve ter no máximo 1 minuto para melhor desempenho na transcrição.
Certifique-se de que a chave API do Gemini está configurada corretamente.
Arquivos temporários são criados em temp_audio/ e removidos automaticamente após o processamento.
📜 Licença
Este projeto está licenciado sob a MIT License.
