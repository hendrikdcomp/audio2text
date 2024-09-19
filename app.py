# -*- coding: utf-8 -*-
import streamlit as st
import whisper
import os

# Carregar modelo Whisper para transcrição
def whisper_get_text(path: str) -> str:
    model = whisper.load_model("large")  # Pode ser "small", "medium", ou "large"
    audio = whisper.load_audio(path)
    result = model.transcribe(audio, language="pt")
    return str(result["text"])

# Função para salvar a transcrição em um arquivo .txt
def save_transcription(text: str, audio_filename: str):
    base_filename = os.path.splitext(audio_filename)[0]  # Remove a extensão do arquivo de áudio
    txt_filename = f"{base_filename}.txt"
    with open(txt_filename, "w", encoding="utf-8") as txt_file:
        txt_file.write(text)
    return txt_filename

# Função principal do aplicativo
def main():
    st.subheader("Transcrição de Áudio para Texto")

    # Verificação do estado de sessão para saber se a transcrição foi realizada
    if "transcription" not in st.session_state:
        st.session_state.transcription = None
        st.session_state.transcription_filename = None

    # Upload do arquivo de áudio
    uploaded_file = st.file_uploader("Escolha um arquivo de áudio (.mp3)", type=["mp3"])

    # Verificação se o arquivo foi carregado
    if uploaded_file is not None:
        # Salvando o áudio carregado
        temp_audio_path = uploaded_file.name
        with open(temp_audio_path, "wb") as f:
            f.write(uploaded_file.getvalue())

        st.write("Áudio carregado com sucesso.")

        # Adiciona a opção de escutar o áudio
        st.audio(temp_audio_path, format="audio/mp3")

        # Checkbox para mostrar transcrição na página
        show_transcription = st.checkbox("Exibir transcrição na página")

        # Adiciona botão para iniciar a transcrição manualmente
        if st.button("Iniciar Transcrição"):
            # Transcrição do áudio
            with st.spinner("Transcrevendo..."):
                text_extracted = whisper_get_text(temp_audio_path)
            st.write("Texto transcrito com sucesso!")

            # Salvar a transcrição como arquivo .txt
            txt_filename = save_transcription(text_extracted, uploaded_file.name)
            st.session_state.transcription = text_extracted
            st.session_state.transcription_filename = txt_filename
            st.success(f"Transcrição salva como {txt_filename}")

        # Mostrar transcrição na página, se checkbox estiver marcado
        if show_transcription and st.session_state.transcription:
            st.write("Transcrição do Áudio:")
            st.write(st.session_state.transcription)

        # Botão para fazer download do arquivo .txt, se a transcrição existir
        if st.session_state.transcription_filename:
            with open(st.session_state.transcription_filename, "r", encoding="utf-8") as txt_file:
                st.download_button(f"Baixar Transcrição: {st.session_state.transcription_filename}", txt_file, file_name=st.session_state.transcription_filename)

    else:
        st.write("Por favor, carregue um arquivo de áudio.")

# Executar a função principal
if __name__ == "__main__":
    main()