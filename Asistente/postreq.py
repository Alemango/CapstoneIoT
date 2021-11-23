import azure.cognitiveservices.speech as speechsdk
import requests

urla = "https://prod-16.westus.logic.azure.com:443/workflows/fbf4ceb5c57d4c0c855c5eee69903ced/triggers/manual/paths/invoke?api-version=2016-10-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=0h2xGqODvg1PKcdPX6Or8_ogRFiWIO1sK0MlOSeoh-Q"
header = {"Content-Type": "application/json"}

#inid = input("Introduce tu nombre: ")
#inaw = input("Te gustan los elotes? ")

speech_config = speechsdk.SpeechConfig(subscription="94ae3801dd2147e39787c7b05e045899", region="westus")
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