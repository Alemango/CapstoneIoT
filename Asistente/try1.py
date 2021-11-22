import azure.cognitiveservices.speech as speechsdk #Importamos la librería de S2T de Azure

hola = "Hola." #Variable de control

def from_mic():
    speech_config = speechsdk.SpeechConfig(subscription="2b8110f589a14d9e8636dda17cce99e9", region="southcentralus") #Suscripción y región no activa, requiere autorización
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, language="es-MX") #Configuramos para español de México
    
    print("Di algo.")
    resultado = speech_recognizer.recognize_once_async().get() #Toma de datos por voz

    if resultado.reason == speechsdk.ResultReason.RecognizedSpeech: #Si se reconoce
        print("Dijiste: {}".format(resultado.text))                 #imprimelo
    elif resultado.reason == speechsdk.ResultReason.NoMatch:                    #Si no se reconoce
        print("No pudo ser reconocido: {}".format(resultado.no_match_details))  #imprime los detalles de fallo  
    elif resultado.reason == speechsdk.ResultReason.Canceled:                               #Si se cancela el reconocimiento
        cancellation_details = resultado.cancellation_details                               #ponlo en una variable
        print("El reconocimiento fue cancelado: {}".format(cancellation_details.reason))    #imprime la razón de la cancelación
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))           #imprime los detalles del error de la cancelación

    if resultado.text == hola:     #Comparalo con la variable de control
        print("Hecho")

from_mic() #Inicia la funcion
