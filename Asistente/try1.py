import azure.cognitiveservices.speech as speechsdk

hola = "Hola."

def from_mic():
    speech_config = speechsdk.SpeechConfig(subscription="2b8110f589a14d9e8636dda17cce99e9", region="southcentralus")
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, language="es-MX")
    
    print("Di algo.")
    resultado = speech_recognizer.recognize_once_async().get()

    if resultado.reason == speechsdk.ResultReason.RecognizedSpeech:
        print("Dijiste: {}".format(resultado.text))
    elif resultado.reason == speechsdk.ResultReason.NoMatch:
        print("No pudo ser reconocido: {}".format(resultado.no_match_details))
    elif resultado.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = resultado.cancellation_details
        print("El reconocimiento fue cancelado: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))

    if result.text == hola:
        print("Hecho")

from_mic()
