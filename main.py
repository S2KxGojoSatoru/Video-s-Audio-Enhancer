import streamlit as st
import moviepy.editor as mp
import speech_recognition as sr
from gtts import gTTS
import tempfile
import requests
azure_openai_key = "22ec84421ec24230a3638d1b51e3a7dc"
azure_openai_endpoint = "https://internshala.openai.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2024-08-01-preview"  


def transcribe_audio(video_path):
    audio_clip = mp.VideoFileClip(filename=video_path).audio
    audio_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
    audio_clip.write_audiofile(audio_file.name, codec='pcm_s16le')

    r = sr.Recognizer()

    with sr.AudioFile(audio_file.name) as source:
        audio_data = r.record(source)
        transcription = r.recognize_google(audio_data)
    
    return transcription

def correct_transcription(transcription):
    if azure_openai_key and azure_openai_endpoint:
        try:
            headers = {
                "Content-Type":"application/json",
                "api-key":azure_openai_key
            }
            data = {
                "messages":[{"role":"user", "content":f"Correct this text for grammatical errors: {transcription}"}]
            }
            response = requests.post(azure_openai_endpoint, headers=headers, json= data)
            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"].strip()
            else:
                st.error(f"Failed to connect or retrieve response: {response.status_code} - {response.text}")
        except Exception as e:
            st.error(f"Failed to connect or retrieve response: {str(e)}")

def generate_audio(text):
    tts = gTTS(text=text, lang='en')
    audio_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
    tts.save(audio_file.name)
    return audio_file.name

def replace_audio(video_path, new_audio_path):
    video_clip = mp.VideoFileClip(video_path)
    new_audio_clip = mp.AudioFileClip(new_audio_path)
    
    final_video = video_clip.set_audio(new_audio_clip)
    output_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
    final_video.write_videofile(output_file.name, codec='libx264')
    return output_file.name


st.title("Video Audio Replacement with AI Voice") 
uploaded_file = st.file_uploader("Upload Video File", type=["mp4", "mov"])
if uploaded_file:
    with open("temp_video.mp4", "wb") as f:
        f.write(uploaded_file.read())

    if st.button("Process Video"):
        st.write("Transcribing audio...")
        transcription = transcribe_audio("temp_video.mp4")
        st.success(body="Transcription completed.", icon="✅")
        st.write("Your Transcript:")
        st.write(transcription)

        st.write("Correcting transcription...")
        corrected_transcription = correct_transcription(transcription)
        st.success("Transcription corrected.", icon="✅")
        st.write("Corrected Transcript:")
        st.write(corrected_transcription)

        st.write("Generating new audio...")
        new_audio_path = generate_audio(corrected_transcription)
        st.success("New audio generated.", icon="✅")
        st.write("Generated Audio: ")
        st.audio(new_audio_path)

        st.write("Replacing audio in video...")
        final_video_path = replace_audio("temp_video.mp4", new_audio_path)
        st.write("Audio replaced successfully.")

        st.video(final_video_path)
