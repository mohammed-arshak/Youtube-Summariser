#-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x
# Importing Libraries

# Running Streamlit
import streamlit as st
st.set_page_config( # Added favicon and title to the web app
     page_title="Youtube Summariser",
     page_icon='favicon.ico',
     layout="wide",
     initial_sidebar_state="expanded",
 )
import base64

# Extracting Transcript from YouTube
import pafy
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse
from textwrap import dedent

#-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x
# All Funtions

# Gensim Summarization
from gensim.summarization.summarizer import summarize
def gensim_summarize(text_content, percent):
    
    summary = summarize(text_content, ratio=(int(percent) / 100), split=False).replace("\n", " ")
    return summary


#-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x

# Hide Streamlit Footer and buttons
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

# Adding logo for the App
file_ = open("app_logo.gif", "rb")
contents = file_.read()
data_url = base64.b64encode(contents).decode("utf-8")
file_.close()

st.sidebar.markdown(
    f'<img src="data:image/gif;base64,{data_url}" alt="" style="height:300px; width:400px;">',
    unsafe_allow_html=True,
)

# Input Video Link
url = st.sidebar.text_input('Video URL', 'https://www.youtube.com/watch?v=T-JVpKku5SI')

# Display Video and Title
video = pafy.new(url)
value = video.title
st.info("### " + value)
st.video(url)

# Specify the summarization algorithm
sumalgo = st.sidebar.selectbox(
     'Select a Summarisation Algorithm',
     options=['Gensim', 'NLTK', 'Spacy'])

# Specify the summary length
length = st.sidebar.select_slider(
     'Specify length of Summary',
     options=['10', '20', '30', '40', '50'])


#-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x
# If Summarize button is clicked
if st.sidebar.button('Summarize'):
    st.success(dedent("""### \U0001F4D6 Summary
> Success!
    """))

    # Generate Transcript by slicing YouTube link to id 
    url_data = urlparse(url)
    id = url_data.query[2::]
    
    def generate_transcript(id):
            transcript = YouTubeTranscriptApi.get_transcript(id)
            script = ""

            for text in transcript:
                    t = text["text"]
                    if t != '[Music]':
                            script += t + " "
                    
            return script, len(script.split())
    transcript, no_of_words = generate_transcript(id)

    # Transcript Summarization is done here
    if sumalgo == 'Gensim':
        summ = gensim_summarize(transcript, length)

    #if sumalgo == 'NLTK':
        # Call that function

    #if sumalgo == 'Spacy':
        # Call that function

    else:
        summ = "\U0001F6A7 Work in Progress \U0001F6A7"

    # Priting Summary (summ) in "JUSTIFY" alignment
    html_str = f"""
<style>
p.a {{
text-align: justify;
}}
</style>
<p class="a">{summ}</p>
"""
    st.markdown(html_str, unsafe_allow_html=True)


#-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x


# Add Sidebar Info
st.sidebar.info(
        dedent(
            """
        This web [app][#streamlit-app] is made by\n
        [Diksha Dutt][#linkedin1] and [Soman Yadav][#linkedin2].
        
        [#linkedin1]: https://www.linkedin.com/in/dikshadutt08/
        [#linkedin2]: https://www.linkedin.com/in/somanyadav/
        [#streamlit-app]: https://github.com/somanyadav/Youtube-Summariser/
        
        """
        )
    )
