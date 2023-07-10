import openai
import speech_recognition as sr
import pyttsx3

# salve es un asistente de voz con ChatGPT 

openai.api_key = "sk..." # aqui debes poner tu api_key 

# debes decir "salve" para iniciar

engine = pyttsx3.init()

def transcribe_audio_to_text(filename):
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)
        try:
            return recognizer.recognize_google(audio, language="es")
        except sr.UnknownValueError:
            print("No te entiendo")
        except sr.RequestError as e:
            print("Error al procesar la solicitud:", str(e))

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
    engine.say(text)
    engine.runAndWait()

def get_spanish_voice():
    voices = engine.getProperty("voices")
    for voice in voices:
        if "spanish" in voice.languages:
            return voice.id
    return None

def record_audio_to_file(filename):
    with sr.Microphone() as source:
        recognizer = sr.Recognizer()
        audio = recognizer.listen(source)
        try:
            transcription = recognizer.recognize_google(audio, language="es")
            if transcription.lower() == "salve":
                print("En qué te puedo ayudar")
                speak_text("En qué te puedo ayudar")
                source.pause_threshold = 1
                audio = recognizer.listen(source, phrase_time_limit=None, timeout=None)
                with open(filename, "wb") as f:
                    f.write(audio.get_wav_data())
                return True
        except sr.UnknownValueError:
            print("No se pudo reconocer el audio")
        except sr.RequestError as e:
            print("Error al procesar la solicitud:", str(e))
        return False

def main():
    spanish_voice = get_spanish_voice()
    if spanish_voice is not None:
        engine.setProperty("voice", spanish_voice)

    while True:
        print("Di 'salve' para empezar a grabar")
        filename = "input.wav"
        if record_audio_to_file(filename):
            text = transcribe_audio_to_text(filename)
            if text:
                print(f"Usuario: {text}")
                response = generate_response(text)
                print(f"El bot responde: {response}")
                speak_text(response)

if __name__ == "__main__":
    main()
