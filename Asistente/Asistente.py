import azure.cognitiveservices.speech as speechsdk
import time
import requests
import json

speech_config = speechsdk.SpeechConfig(subscription="KEY", region="REGION")

def NOMBRE():
    modelo = speechsdk.KeywordRecognitionModel("2c250f64-5d7d-48b3-89dd-c1625a472da1.table")
    keyword = "Emma"
    reconocimiento = speechsdk.KeywordRecognizer()
    hecho = False

    resultado_futuro = reconocimiento.recognize_once_async(modelo)
    print('Dialgo iniciando con "{}" seguido de una acción por realizar'.format(keyword))
    resultado = resultado_futuro.get()

    if resultado.reason == speechsdk.ResultReason.RecognizedKeyword:
        time.sleep(0.2) 
        resultado_stream = speechsdk.AudioDataStream(resultado)
        resultado_stream.detach_input() 
        hecho = True

    print(hecho)

def S2T():
    urla = "https://prod-16.westus.logic.azure.com:443/workflows/fbf4ceb5c57d4c0c855c5eee69903ced/triggers/manual/paths/invoke?api-version=2016-10-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=0h2xGqODvg1PKcdPX6Or8_ogRFiWIO1sK0MlOSeoh-Q"
    header = {"Content-Type": "application/json"}

    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, language="es-MX")
    print("Habla en tu micrófono") 
    resultado = speech_recognizer.recognize_once_async().get()
    if resultado.reason == speechsdk.ResultReason.RecognizedSpeech:
        print("Dijiste: {}".format(resultado.text))
    elif resultado.reason == speechsdk.ResultReason.NoMatch:
        print("No se pudo reconocer:  {}".format(resultado.no_match_details))
    elif resultado.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = resultado.cancellation_details
        print("Reconocimiento cancelado: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))

    obj = {'Mensaje': resultado.text}

    r = requests.post(url = urla, headers = header, json = obj)

    respuesta = r.content
    responsed = json.loads(respuesta)

    print(respuesta)

def T2S():
    speech_config.speech_synthesis_language = "es-MX"
    speech_config.speech_synthesis_voice_name ="es-MX-DaliaNeural"

    audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    synthesizer.speak_text_async("Dígame.")


NOMBRE()
T2S()
S2T()
