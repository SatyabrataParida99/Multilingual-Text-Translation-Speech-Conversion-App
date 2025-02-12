import streamlit as st
from mtranslate import translate
import pandas as pd
import os
from gtts import gTTS
import base64

# Custom CSS for Styling
st.markdown("""
    <style>
        .main-title {
            font-size: 36px;
            font-weight: bold;
            color: #ff4b4b;
            text-align: center;
        }
        .sidebar .css-1aumxhk {
            background-color: #f4f4f4 !important;
            color: #333 !important;
        }
        .stTextArea textarea {
            font-size: 18px;
            padding: 10px;
            border-radius: 10px;
            border: 1px solid #ddd;
        }
        .translate-button {
            background-color: #ff4b4b;
            color: white;
            padding: 10px;
            border-radius: 8px;
            font-size: 18px;
            width: 100%;
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

# Read language dataset
df = pd.read_csv(r"D:\VS Code Project\NLP\language_updated.csv")
df.dropna(inplace=True)
lang = df['name'].to_list()
langlist = tuple(lang)
langcode = df['iso'].to_list()
lang_array = {lang[i]: langcode[i] for i in range(len(langcode))}

# Layout with HTML Title
st.markdown('<h1 class="main-title">🌍 Language Translation & Speech Generator</h1>', unsafe_allow_html=True)
inputtext = st.text_area("✍ Enter text to translate", height=100)

# Sidebar Selection
st.sidebar.markdown("## 🌐 Select Language")
choice = st.sidebar.radio('Choose Language:', langlist)

# Function to decode audio file for download
def get_binary_file_downloader_html(bin_file, file_label='Download Audio'):
    with open(bin_file, 'rb') as f:
        data = f.read()
    bin_str = base64.b64encode(data).decode()
    return f'<a class="translate-button" href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">{file_label}</a>'

c1, c2 = st.columns([4, 3])

# Processing Translation
if len(inputtext) > 0:
    try:
        output = translate(inputtext, lang_array[choice])
        with c1:
            st.text_area("🔁 Translated Text", output, height=200)
        
        # Speech Output
        aud_file = gTTS(text=output, lang=lang_array[choice], slow=False)
        aud_file.save("lang.mp3")
        audio_file_read = open('lang.mp3', 'rb')
        audio_bytes = audio_file_read.read()
        
        with c2:
            st.audio(audio_bytes, format='audio/mp3')
            st.markdown(get_binary_file_downloader_html("lang.mp3"), unsafe_allow_html=True)
    
    except Exception as e:
        st.error(f"⚠️ Error: {e}")
