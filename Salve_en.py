import openai
import speech_recognition as sr
import pyttsx3

# salve is a voice assistant with ChatGPT

openai.api_key = "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" # here you must put your api_key

# you must say "salve" to start

engine = pyttsx3.init()

def transcribe_audio_to_text(filename):
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)
        try:
            return recognizer.recognize_google(audio, language="en-US")
        except sr.UnknownValueError:
            print("I don't understand")
        except sr.RequestError as e:
            print("Error processing the request:", str(e))

def generate_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=4000,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response["choices"][0]["text"]

def speak_text(text):
    engine.setProperty("voice", get_english_voice())
    engine.say(text)
    engine.runAndWait()


def get_english_voice():
    voices = engine.getProperty("voices")
    for voice in voices:
        if "english" in voice.languages:
            return voice.id
    return None



def record_audio_to_file(filename):
    with sr.Microphone() as source:
        recognizer = sr.Recognizer()
        audio = recognizer.listen(source)
        try:
            transcription = recognizer.recognize_google(audio, language="en-US")
            if transcription.lower() == "salve":
                print("How can I assist you?")
                speak_text("How can I assist you?")
                source.pause_threshold = 1
                audio = recognizer.listen(source, phrase_time_limit=None, timeout=None)
                with open(filename, "wb") as f:
                    f.write(audio.get_wav_data())
                return True
        except sr.UnknownValueError:
            print("Could not recognize the audio")
        except sr.RequestError as e:
            print("Error processing the request:", str(e))
        return False
def main():
    english_voice = get_english_voice()
    if english_voice is not None:
        engine.setProperty("voice", english_voice)

    while True:
        print("Say 'salve' to start recording")
        filename = "input.wav"
        if record_audio_to_file(filename):
            text = transcribe_audio_to_text(filename)
            if text:
                print(f"User: {text}")
                response = generate_response(text)
                print(f"the bot responds: {response}")
                speak_text(response)

if __name__ == "__main__":
    main()

    
        

