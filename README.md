Used Streamlit to build the UI and deploy the web app. This app takes in a video with audio that has gramatical mistakes and human errors (umm... aaahh).
The audio is extracted from the video, from which the text is extracted, using MoviePy and SpeechRecognition Module respetively.
This text is sent to Azure Open AI API to get it corrected and the corrected text is recieved.
Further this corrected improved text is converted to AI Speech using Pythons gTTS module.
Then finally this audio is replaced with the videos's original audio.


Better Alternatives for converting audio to text and text to AI audio is Google Cloud Speech-to-Text API and Google Cloud Text-to-Speech API, respectively.

Link for the web app - https://video-s-audio-enhancer.streamlit.app/

Screenshot:![FIrst Page](https://github.com/user-attachments/assets/3c1f1d3a-4273-4070-94b2-62c7e066be5c)

