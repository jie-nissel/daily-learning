import json 
import traceback 
import sys
from google.oauth2 import service_account
from pydub import AudioSegment
from pydub.silence import split_on_silence
import os 
PROJECT_ID = 'gcp-ushi-daci-analyze-qa'
svc_accts = {
    "digital-ds": "item-data-quality-gcp-ushi-digital-ds-qa-bq-service-account.json",
    "daci-analyze": "gcp-ushi-daci-analyze-qa-bg-ao-r-sa.json"
}
def getSecrets() -> json:
    try:
        # print('System platform:',sys.platform)
        if sys.platform == 'linux':
            with open('/etc/config/secrets', encoding='utf-8') as secret_file:
                secrets = json.load(secret_file)
            return secrets
        elif sys.platform == 'darwin':
            with open(svc_accts.get("daci-analyze"), encoding="utf-8") as secret_file:
                secrets = json.load(secret_file)
            return secrets
    except Exception:
        traceback_string = traceback.format_exc()
        print(f'Secrets File Error: {traceback_string}')
        raise

credentials = service_account.Credentials.from_service_account_info(
    info=getSecrets()
)
def transcribe_file(speech_file):
    """Transcribe the given audio file asynchronously."""
    from google.cloud import speech
    print("Speech Client:")
    client = speech.SpeechClient(credentials = credentials)

    with open(speech_file, "rb") as audio_file:
        print("Open Audio File:")
        content = audio_file.read()

    """
     Note that transcription is limited to a 60 seconds audio file.
     Use a GCS file for audio longer than 1 minute.
    """
    print("Recog Audio:")
    audio = speech.RecognitionAudio(content=content)
    print("config:")
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
#         sample_rate_hertz=16000,
        language_code="en-US",
        use_enhanced = False # not use the enhanced model 
    )


    operation = client.long_running_recognize(config=config, audio=audio)

    print("Waiting for operation to complete...")
    response = operation.result(timeout=30)

    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    for result in response.results:
        # The first alternative is the most likely one for this portion.
        print(u"Transcript: {}".format(result.alternatives[0].transcript))
        print("Confidence: {}".format(result.alternatives[0].confidence))
        return result.alternatives[0].transcript, result.alternatives[0].confidence
    return '', 0.0
def transcribe_audiodata(audio_data):
    """Transcribe the given audio file asynchronously."""
    from google.cloud import speech
    print("Speech Client:")
    client = speech.SpeechClient(credentials = credentials)

    """
     Note that transcription is limited to a 60 seconds audio file.
     Use a GCS file for audio longer than 1 minute.
    """
    print("Recog Audio:")
    audio = speech.RecognitionAudio(content=audio_data)
    print("config:")
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
#         sample_rate_hertz=16000,
        language_code="en-US",
        use_enhanced = False # not use the enhanced model 
    )


    operation = client.long_running_recognize(config=config, audio=audio)

    print("Waiting for operation to complete...")
    response = operation.result(timeout=30)

    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    for result in response.results:
        # The first alternative is the most likely one for this portion.
        print(u"Transcript: {}".format(result.alternatives[0].transcript))
        print("Confidence: {}".format(result.alternatives[0].confidence))
        return result.alternatives[0].transcript, result.alternatives[0].confidence
    return '', 0.0
# a function that splits the audio file into chunks
# and applies speech recognition
def get_large_audio_transcription(path):
    """
    Splitting the large audio file into chunks
    and apply speech recognition on each of these chunks
    """
    # open the audio file using pydub
    sound = AudioSegment.from_wav(path)  
    # split audio sound where silence is 700 miliseconds or more and get chunks
    chunks = split_on_silence(sound,
        # experiment with this value for your target audio file
        min_silence_len = 500,
        # adjust this per requirement
        silence_thresh = sound.dBFS-14,
        # keep the silence for 1 second, adjustable as well
        keep_silence=500,
    )
    folder_name = "audio-chunks"
    # create a directory to store the audio chunks
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    whole_text = ""
    # process each chunk 
    for i, audio_chunk in enumerate(chunks, start=1):
        # export audio chunk and save it in
        # the `folder_name` directory.
        chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
        audio_chunk.export(chunk_filename, format="wav")
        # recognize the chunk
        with sr.AudioFile(chunk_filename) as source:
            audio_listened = r.record(source)
            # try converting it to text
            try:
                text = r.recognize_google(audio_listened)
            except sr.UnknownValueError as e:
                print("Error:", str(e))
            else:
                text = f"{text.capitalize()}. "
                print(chunk_filename, ":", text)
                whole_text += text
    # return the text for all chunks detected
    return whole_text