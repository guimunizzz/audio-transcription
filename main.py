import streamlit as st
import speech_recognition as sr
import os
import uuid
import shutil
from pydub import AudioSegment
import google.generativeai as genai
import dotenv
import subprocess

# Configuração da página Streamlit
st.set_page_config(
    page_title="Tradutor de Áudio",
    page_icon="🎙️",
    layout="centered"
)

# Estilo personalizado (tema escuro futurista)
st.markdown("""
    <style>
    /* Tema geral */
    .main {
        background: linear-gradient(135deg, #0d1117 0%, #1c2526 100%);
        color: #e0e0e0;
        font-family: 'Montserrat', sans-serif;
        padding: 30px;
        min-height: 100vh;
    }
    /* Títulos */
    h1 {
        color: #60a5fa;
        font-weight: 700;
        font-size: 3rem;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 0 0 10px rgba(96, 165, 250, 0.5);
    }
    h2 {
        color: #a3bffa;
        font-weight: 500;
        font-size: 1.8rem;
        margin-bottom: 1rem;
    }
    /* Texto padrão */
    .stMarkdown, .stText, .stInfo, .stSuccess, .stError, .stWarning {
        color: #d1d5db;
        font-size: 1.1rem;
    }
    /* Botões */
    .stButton>button {
        background: linear-gradient(45deg, #0284c7, #60a5fa);
        color: #ffffff;
        font-weight: 600;
        font-size: 1.1rem;
        padding: 14px 30px;
        border-radius: 12px;
        border: none;
        transition: all 0.3s ease;
        box-shadow: 0 0 15px rgba(2, 132, 199, 0.5);
    }
    .stButton>button:hover {
        background: linear-gradient(45deg, #0369a1, #3b82f6);
        transform: scale(1.08);
        box-shadow: 0 0 20px rgba(2, 132, 199, 0.7);
    }
    /* File Uploader */
    .stFileUploader {
        background-color: #161b22;
        border: 2px solid #374151;
        border-radius: 12px;
        padding: 20px;
        color: #d1d5db;
        transition: border-color 0.3s ease, box-shadow 0.3s ease;
    }
    .stFileUploader:hover {
        border-color: #60a5fa;
        box-shadow: 0 0 15px rgba(96, 165, 250, 0.3);
    }
    /* Selectbox */
    .stSelectbox {
        background-color: #161b22;
        border-radius: 12px;
        color: #d1d5db;
    }
    .stSelectbox [data-baseweb="select"] {
        background-color: #161b22;
        color: #d1d5db;
        border: 1px solid #374151;
        border-radius: 12px;
        padding: 10px;
    }
    .stSelectbox [data-baseweb="select"]:hover {
        border-color: #60a5fa;
        box-shadow: 0 0 10px rgba(96, 165, 250, 0.3);
    }
    /* Expander */
    .stExpander {
        background-color: #161b22;
        border: 1px solid #374151;
        border-radius: 12px;
        color: #d1d5db;
    }
    .stExpander [data-baseweb="accordion"] {
        background-color: #161b22;
        color: #d1d5db;
    }
    /* Resultados */
    .result-card {
        background-color: #161b22;
        border: 1px solid #374151;
        border-radius: 12px;
        padding: 25px;
        margin: 20px 0;
        color: #d1d5db;
        box-shadow: 0 0 15px rgba(0, 0, 0, 0.4);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .result-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 0 20px rgba(96, 165, 250, 0.3);
    }
    /* JSON display */
    .stJson {
        background-color: #161b22;
        border: 1px solid #374151;
        border-radius: 12px;
        padding: 15px;
        color: #d1d5db;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);
    }
    /* Spinner */
    .stSpinner>span {
        color: #60a5fa;
    }
    /* Alertas */
    .stAlert {
        background-color: #161b22;
        border: 1px solid #374151;
        color: #d1d5db;
        border-radius: 12px;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);
    }
    /* Botão de informações */
    .info-button {
        background: linear-gradient(45deg, #dc2626, #f87171);
        color: #ffffff;
        font-weight: 600;
        font-size: 1rem;
        padding: 10px 20px;
        border-radius: 10px;
        border: none;
        transition: all 0.3s ease;
        box-shadow: 0 0 10px rgba(220, 38, 38, 0.5);
        cursor: pointer;
        text-align: center;
        display: block;
        margin: 20px auto;
    }
    .info-button:hover {
        background: linear-gradient(45deg, #b91c1c, #ef4444);
        transform: scale(1.05);
        box-shadow: 0 0 15px rgba(220, 38, 38, 0.7);
    }
    </style>
""", unsafe_allow_html=True)

# Carregar variáveis de ambiente
dotenv.load_dotenv()

# Configurar a API Gemini
try:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    if not GEMINI_API_KEY:
        st.error("⚠️ Chave API Gemini não encontrada. Configure a variável GEMINI_API_KEY no arquivo .env.")
        st.stop()
    
    genai.configure(api_key=GEMINI_API_KEY)
except Exception as e:
    st.error(f"Erro ao configurar a API Gemini: {str(e)}")
    st.stop()

# Verificar e configurar FFmpeg
try:
    subprocess.run(['ffmpeg', '-version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
except (subprocess.SubprocessError, FileNotFoundError):
    st.error("""
    FFmpeg não foi encontrado. É necessário para processar áudios.
    Instale com:
    - Windows: Baixe em https://ffmpeg.org/download.html e adicione ao PATH
    - Mac: brew install ffmpeg
    - Linux: sudo apt install ffmpeg
    """)
    st.stop()

try:
    test_audio = AudioSegment.silent(duration=1000)
    test_audio.export("test_conversion.wav", format="wav")
    os.remove("test_conversion.wav")
except Exception as e:
    st.error(f"Erro na configuração do FFmpeg: {str(e)}")
    st.stop()

# Função para verificar e converter áudio
def processar_audio(input_path, output_path):
    try:
        subprocess.run([
            'ffmpeg', '-y', '-i', input_path,
            '-acodec', 'pcm_s16le',
            '-ar', '16000',
            '-ac', '1',
            '-loglevel', 'error',
            output_path
        ], check=True)
        return True, None
    except subprocess.CalledProcessError as e:
        return False, f"Erro na conversão do áudio: {str(e)}"

# Função para transcrever áudio
def transcrever_audio(arquivo_audio):
    recognizer = sr.Recognizer()
    try:
        if os.path.getsize(arquivo_audio) < 1024:
            return None, "Arquivo de áudio muito pequeno ou inválido."
            
        with sr.AudioFile(arquivo_audio) as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio_data = recognizer.record(source, duration=60)
            
            if len(audio_data.get_raw_data()) == 0:
                return None, "Não foi possível capturar áudio do arquivo."
            
            texto = recognizer.recognize_google(
                audio_data,
                language="pt-BR",
                show_all=False
            )
            return texto, None
    except sr.UnknownValueError:
        return None, "Não foi possível entender o áudio. Tente com um áudio mais claro."
    except sr.RequestError as e:
        return None, f"Erro no serviço de reconhecimento: {str(e)}"
    except Exception as e:
        return None, f"Erro ao transcrever o áudio: {str(e)}"

# Função para traduzir texto
def traduzir_texto(texto, idioma_destino):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"Traduza o seguinte texto do português para {idioma_destino}: {texto}"
        response = model.generate_content(prompt)
        return response.text, None
    except Exception as e:
        return None, f"Erro ao traduzir o texto: {str(e)}"

# Interface principal
st.title("🎙️ Tradutor de Áudio Avançado")

with st.container():
    st.markdown("""
    <div style='text-align: center; color: #d1d5db; font-size: 1.2rem; margin-bottom: 2rem;'>
        Transcreva áudios em português e traduza para diversos idiomas usando IA.<br>
        Suporta arquivos MP3 ou WAV (máximo de 1 minuto).
    </div>
    """, unsafe_allow_html=True)

# Seção de upload e configuração
with st.container():
    st.subheader("🎵 Upload e Configuração")
    arquivo_audio = st.file_uploader(
        "Selecione um arquivo de áudio (MP3 ou WAV)",
        type=["mp3", "wav"],
        accept_multiple_files=False
    )
    
    idiomas = {
        "Inglês": "inglês",
        "Espanhol": "espanhol",
        "Francês": "francês",
        "Alemão": "alemão",
        "Italiano": "italiano",
        "Japonês": "japonês",
        "Coreano": "coreano",
        "Chinês": "chinês (simplificado)",
        "Russo": "russo",
        "Árabe": "árabe"
    }
    
    idioma_destino = st.selectbox(
        "Selecione o idioma de destino",
        list(idiomas.keys()),
        index=0
    )

# Seção de pré-visualização
if arquivo_audio:
    with st.container():
        st.subheader("🔊 Pré-visualização do Áudio")
        st.audio(arquivo_audio)
        
        file_details = {
            "Nome": arquivo_audio.name,
            "Tipo": arquivo_audio.type,
            "Tamanho": f"{arquivo_audio.size / 1024:.2f} KB"
        }
        st.json(file_details)

# Botão de processamento
if arquivo_audio:
    if st.button("🔊 Processar Áudio", type="primary"):
        with st.spinner("Processando áudio..."):
            try:
                temp_dir = "temp_audio"
                os.makedirs(temp_dir, exist_ok=True)
                
                unique_id = str(uuid.uuid4())
                temp_input = os.path.join(temp_dir, f"input_{unique_id}")
                temp_wav = os.path.join(temp_dir, f"output_{unique_id}.wav")
                
                with open(temp_input, "wb") as f:
                    f.write(arquivo_audio.getbuffer())
                
                success, error = processar_audio(temp_input, temp_wav)
                if not success:
                    st.error(error)
                    st.stop()
                
                texto_transcrito, error = transcrever_audio(temp_wav)
                if error:
                    st.error(f"Transcrição: {error}")
                    st.stop()
                
                texto_traduzido, error = traduzir_texto(texto_transcrito, idiomas[idioma_destino])
                if error:
                    st.error(f"Tradução: {error}")
                    st.stop()
                
                st.success("Processamento concluído com sucesso!")
                
                # Seção de resultados
                with st.container():
                    st.subheader("📝 Resultados")
                    with st.expander("Texto Original (Português)", expanded=True):
                        st.markdown(f'<div class="result-card">{texto_transcrito}</div>', unsafe_allow_html=True)
                        st.download_button(
                            "Baixar Transcrição",
                            texto_transcrito,
                            file_name="transcricao_original.txt",
                            key="download_transcription"
                        )
                    
                    with st.expander(f"Tradução ({idioma_destino})", expanded=True):
                        st.markdown(f'<div class="result-card">{texto_traduzido}</div>', unsafe_allow_html=True)
                        st.download_button(
                            "Baixar Tradução",
                            texto_traduzido,
                            file_name=f"traducao_{idioma_destino.lower()}.txt",
                            key="download_translation"
                        )
                
            except Exception as e:
                st.error(f"Erro no processamento: {str(e)}")
            finally:
                try:
                    if os.path.exists(temp_input):
                        os.remove(temp_input)
                    if os.path.exists(temp_wav):
                        os.remove(temp_wav)
                except Exception as e:
                    st.warning(f"Não foi possível limpar arquivos temporários: {str(e)}")

# Botão para informações adicionais
st.markdown(
    '<button class="info-button">Mostrar Informações e Instruções</button>',
    unsafe_allow_html=True
)

# Seção de informações (expander)
with st.expander("ℹ️ Sobre e Instruções"):
    st.markdown("""
    ### Sobre
    Esta aplicação utiliza:
    - **Google Speech Recognition** para transcrição de áudio
    - **Gemini AI** para tradução de texto
    - **FFmpeg** para processamento de arquivos de áudio

    ### Instruções
    1. Faça upload de um arquivo de áudio em português (MP3 ou WAV)
    2. Selecione o idioma de destino
    3. Clique em "Processar Áudio"
    4. Visualize e baixe a transcrição e a tradução

    ### Requisitos
    - Python 3.8+
    - FFmpeg instalado
    - Chave API Gemini configurada no arquivo `.env`
    - Conexão com a internet
    """, unsafe_allow_html=True)

    if st.button("🔄 Reiniciar Aplicativo"):
        st.rerun()