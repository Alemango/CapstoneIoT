import azure.cognitiveservices.speech as speechsdk

hola = "Hola."

def from_mic():
    speech_config = speechsdk.SpeechConfig(subscription="2b8110f589a14d9e8636dda17cce99e9", region="southcentralus")
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, language="es-MX")
    
    print("Speak into your microphone.")
    result = speech_recognizer.recognize_once_async().get()

    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print("Recognized: {}".format(result.text))
    elif result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized: {}".format(result.no_match_details))
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech Recognition canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))

    if result.text == hola:
        print("Hecho")

from_mic()