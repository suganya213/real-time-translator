import io
import openai
from gtts import gTTS
import streamlit as st
from io import BytesIO
from audiorecorder import audiorecorder

#---------------------------------#
# Set page configuration
#---------------------------------#
st.set_page_config(page_title='Real Time Translation', 
					page_icon='🌎', 
					layout='wide', 
					initial_sidebar_state='auto')
hide_streamlit_style = """
			<style>
			footer {visibility: hidden;}
			</style>
			"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

#---------------------------------#
# Main
#---------------------------------#
def main():
	st.header('Real Time Translation')
	st.caption('Written by LPM')

	# OpenAI API key
	openai.api_key = st.secrets["OPENAI_API_KEY"]

	audio = audiorecorder("Click to record", "Recording...")
	if len(audio) > 0:
		audio_bytes = audio.tobytes()
		if audio_bytes:
			st.audio(audio_bytes, format="audio/wav")
			st.session_state.audio_bytes = audio_bytes\

	if 'audio_bytes' in st.session_state:
		# st.info('Audio successfully recorded, translating...')
		if len(st.session_state.audio_bytes) > 0:
			# Translate audio bytes into English
			audio_file = io.BytesIO(st.session_state.audio_bytes)
			audio_file.name = "temp_audio_file.wav"
			transcript = openai.Audio.translate("whisper-1", audio_file)
			st.markdown("*See translation below:*")
			st.code(transcript['text'])
			if len(transcript['text']) > 0: 
				# Convert text to speech
				sound_file = BytesIO()
				tts = gTTS(transcript['text'], lang='en')
				tts.write_to_fp(sound_file)
				st.audio(sound_file)
			else:
				st.warning('No text to convert to speech.')
		else:
			st.warning('No audio recorded, please make sure your audio got recorded correctly.')
			# else:
			# 	st.warning('No audio recorded, please make sure your audio got recorded correctly.')

	# Just play text to speech
	with st.form('text_to_speech'):
		st.subheader('Text to Speech')
		text_to_speech = st.text_area('Enter text to convert to speech')
		submit_button = st.form_submit_button(label='Convert')
		if submit_button and len(text_to_speech) > 0:
			# Convert text to speech
			sound_file = BytesIO()
			tts = gTTS(text_to_speech, lang='en')
			tts.write_to_fp(sound_file)
			st.audio(sound_file)

def check_password():
	"""
	A function that return True if the password is correct, False otherwise.
	"""

	def password_entered():
		"""
		Checks whether a password entered by the user is correct.
		"""
		if st.session_state["password"] == st.secrets["user_pass"]:
			st.session_state["password_correct"] = True
			del st.session_state["password"]  # don't store password
		else:
			st.session_state["password_correct"] = False

	if "password_correct" not in st.session_state:
		# First run, show input for password.
		st.text_input(
			"Password", type="password", on_change=password_entered, key="password"
		)
		return False
	
	elif not st.session_state["password_correct"]:
		# Password not correct, show input + error.
		st.text_input(
			"Password", type="password", on_change=password_entered, key="password"
		)
		st.error("Password incorrect")
		return False
	else:
		# Password correct.
		return True
	
#---------------------------------#
# Run the main function
#---------------------------------#
if __name__ == '__main__':
	# if check_password():
		main()
