import azure.cognitiveservices.speech as speechsdk
import time
import requests
import json

speech_config = speechsdk.SpeechConfig(subscription="94ae3801dd2147e39787c7b05e045899", region="westus")
ProductID = "3ac35d1779c6404bb1f9bdacbaff7d9e"

def NOMBRE():
    modelo = speechsdk.KeywordRecognitionModel("2c250f64-5d7d-48b3-89dd-c1625a472da1.table")
    keyword = "Emma"
    reconocimiento = speechsdk.KeywordRecognizer()
    hecho = False

    resultado_futuro = reconocimiento.recognize_once_async(modelo)
    print('Di algo iniciando con "{}" seguido de una acción por realizar'.format(keyword))
    resultado = resultado_futuro.get()

    if resultado.reason == speechsdk.ResultReason.RecognizedKeyword:
        time.sleep(0.2) 
        resultado_stream = speechsdk.AudioDataStream(resultado)
        resultado_stream.detach_input() 
        hecho = True

    print(hecho)

def S2TLUIS():
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

    IntentFinal = DevInt(responsed)
    SelectorAccion(responsed,IntentFinal)

def S2T():
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

    return resultado

def T2S(Mensaje):
    speech_config.speech_synthesis_language = "es-MX"
    speech_config.speech_synthesis_voice_name ="es-MX-DaliaNeural"

    audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    synthesizer.speak_text_async(Mensaje)

def T2SError():
    speech_config.speech_synthesis_language = "es-MX"
    speech_config.speech_synthesis_voice_name ="es-MX-DaliaNeural"

    audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    synthesizer.speak_text_async("Lo siento, no te entendí.")

def DevInt(respuesta):
    
    inti = respuesta['topScoringIntent']
    jsintint = json.dumps(inti)

    intin = json.loads(jsintint)
    intint = intin

    return intint

def DevEnt(respuesta):
    for entidad in respuesta['entities']:
        entent = entidad['children']

    iterador = iter(entent)
    
    iterone = json.dumps(next(iterador))
    jsiterone = json.loads(iterone)

    return jsiterone

def DevEnt2(respuesta):
    for entidad in respuesta['entities']:
        entent = entidad['children']

    iterador = iter(entent)
    
    iterone = json.dumps(next(iterador))
    itertwo = json.dumps(next(iterador))
    jsiterone = json.loads(iterone)
    jsitertwo = json.loads(itertwo)

    return jsiterone, jsitertwo

def SelectorAccion(ResBody, IntencionJSON):
    if IntencionJSON['intent'] == 'Pedidos':
        try: 
            EntUno, EntDos = DevEnt2(ResBody)
            print(EntUno)
            print(EntDos)
        except:
            T2SError()

    elif IntencionJSON['intent'] == 'Recordatorio':
        try:
            EntUno = DevEnt(ResBody)
            print(EntUno)
        except:
            T2SError()

    elif IntencionJSON['intent'] == 'DateTime':
        try:
            FH = PedisteFH()
            T2S(FH)
        except:
            T2SError

def TraductorFH(dia, mes):
    if dia == "Monday":
        diatrad = "Lunes"
    elif dia == "Tuesday":
        diatrad = "Martes"
    elif dia == "Wednesday":
        diatrad = "Miércoles"
    elif dia == "Thursday":
        diatrad = "Jueves"
    elif dia == "Friday":
        diatrad = "Viernes"
    elif dia == "Saturday":
        diatrad = "Sábado"
    elif dia == "Sunday":
        diatrad = "Domingo"

    if mes == "01":
        mestrad = "Enero"
    elif mes == "02":
        mestrad = "Febrero"
    elif mes == "03":
        mestrad = "Marzo"
    elif mes == "04":
        mestrad = "Abril"
    elif mes == "05":
        mestrad = "Mayo"
    elif mes == "06":
        mestrad = "Junio"
    elif mes == "07":
        mestrad = "Julio"
    elif mes == "08":
        mestrad = "Agosto"
    elif mes == "09":
        mestrad = "Septiembre"
    elif mes == "10":
        mestrad = "Octubre"
    elif mes == "11":
        mestrad = "Noviembre"
    elif mes == "12":
        mestrad = "Diciembre"

    return diatrad, mestrad

def PedisteFH():
    dialetra = time.strftime("%A")
    mesnumero = time.strftime("%m")

    dia, mes = TraductorFH(dialetra, mesnumero)

    FH = "Son las " + time.strftime("%I") + " con " + time.strftime("%M") + " minutos del " + dia + " " + time.strftime("%d") + " de " + mes + " del " + time.strftime("%Y")

    return FH

def VerifConfigInic():
    urla = "https://prod-90.westus.logic.azure.com:443/workflows/98b8369cf1124757be9371b37d31a8f2/triggers/manual/paths/invoke?api-version=2016-10-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=aPhKiPLu4mvPVh4N4Jnp5W7e8fZI-zagvpm8ctzhm_4"
    header = {"Content-Type": "application/json"}

    obj = {'ID': ProductID}

    r = requests.post(url = urla, headers = header, json = obj)
    
    if r.text == "FALSE":
        Configura = True
    elif r.text =="TRUE":
        Configura = False

    return Configura

def PresentacionCero():
    T2S(Mensaje="¡Hola! Me llamo Emma, ahora soy tu asistente virtual auxiliar en cuidados médicos.")
    T2S(Mensaje="Vamos a configurar el idioma. ¿Es correcto español de México? Responde con: Sí o no.")

def PrimerUsoIdioma():

    resultado = S2T()

    if resultado.text == "No.":
        T2S(Mensaje="Lo siento, por ahora sólo está disponible en este idioma, contacta a servicio al cliente. Seguiremos con la configuración en este idioma.")
        idioma = True
    elif resultado.text == "Sí.":
        T2S(Mensaje="Muy bien, español de México está configurado para este dispositivo.")
        idioma = True
    else:
        T2S("Lo siento, contesta sólo con sí o no. ¿Es correcto español de México?")
        idioma = False

    return idioma

def SiTuto():
    T2S(Mensaje="Me pondré en modo espera, háblame usando mi nombre.")
    T2S(Mensaje="Verás que cambia de color la luz del dispositivo. En ese momento podrás pedirme algo.")
    T2S(Mensaje="Por ejemplo, pídeme la hora.")

    NOMBRE()
    S2TLUIS()

    T2S(Mensaje="¡Muy bien! Has finalizado el tutorial. Podrás consultar más funciones con la frase: Dime tus funciones")

def Tutorial():
    T2S(Mensaje="¡Muy bien! Has configurado el idioma.")
    T2S(Mensaje="¿Deseas hacer el tutorial?")

    resp = S2T()

    if resp.text == "Sí.":
        SiTuto()
        uso = TipoUso()
    else:
        T2S(Mensaje="Puedes consultar mis funciones con la frase: Dime tus funciones")

    return uso

def CambiaConfigInic():
    urla = "https://prod-189.westus.logic.azure.com:443/workflows/c9be7d6e4789427cafd89f3a1410f32d/triggers/manual/paths/invoke?api-version=2016-10-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=E9IgbDx9CIK8iX5ijpfF8knJBUYghFKlT31S_U-vp7c"
    header = {"Content-Type": "application/json"}

    obj = {'ID': ProductID}

    r = requests.post(url = urla, headers = header, json = obj)
    
def TipoUso():
    T2S(Mensaje="Ahora selecciona el tipo de uso. Doméstico o centro de cuidados")
    resultado = S2T()

    if resultado.text == "Doméstico":
        uso = "DOM"
    elif resultado.text == "Centro de cuidados":
        uso = "CC"
    else:
        T2S(Mensaje="Se ha configurado el uso predeterminado. Doméstico")
        uso = "DOM"

    return uso

def CambiaUso(usodefinido):
    urla = "https://prod-126.westus.logic.azure.com:443/workflows/c157c7fe9b9c42b1be5f8ab718a2c53a/triggers/manual/paths/invoke?api-version=2016-10-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=sL5RJbAXUSUnXnv7cPOcWPvDxIugsvQ3xA8xX7EYgTg"
    header = {"Content-Type": "application/json"}

    obj = {'ID': ProductID, 'Uso': usodefinido}

    r = requests.post(url = urla, headers = header, json = obj)
    print(r)
#ConfigInicial = VerifConfigInic()
#if ConfigInicial == True:
#    PresentacionCero()
#    idioma = PrimerUsoIdioma()
#    while idioma == False:
#        idioma = PrimerUsoIdioma()
#    uso = Tutorial()
    CambiaUso(usodefinido= "CC")
#    CambiaConfigInic()
#elif ConfigInicial == False:
#    print("Yaztas")
#NOMBRE()
#T2S(Mensaje="Di algo")
#S2TLUIS()