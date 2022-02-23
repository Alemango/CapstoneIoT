/*
  Diplomado Internet de las cosas | Samsung Innovation Campus

  Proyecto Capstone: Asistente Médico
  Alumno: Juan Jesús Alemán Espriella

  Dispositivo: ESP32 (38 Pines)

  Descripción: Código para la inicialización y lectura del sensor MAX30100. Así como el envío de datos a ThingSpeak.
*/

#include <Wire.h> //Biblioteca que nos permite la creación de un objeto Wire.
#include "MAX30105.h" //Biblioteca que nos permite el manejo del sensor MAX.
#include "spo2_algorithm.h" //Biblioteca para la obtención del SPO2 con el sensor MAX.
#include "ThingSpeak.h" //Biblioteca para la comunicación con ThingSpeak. Autor: MathWorks

unsigned long chanelID = 1648132; //Canal de ThingSpeak
const char* WriteKey = "3BZO9QOJ5C6OBWF1"; //Clave de escritura para la API de Thingspeak

MAX30105 particleSensor; //Creación del objeto MAX

#define MAX_BRIGHTNESS 255 //Definición del brillo en el led del sensor. Influye en la corriente utilizada.

#if defined(__AVR_ATmega328P__) || defined(__AVR_ATmega168__) //Especificaciones para el chip ATMega

uint16_t irBuffer[100]; //infrared LED sensor data
uint16_t redBuffer[100];  //red LED sensor data
#else
uint32_t irBuffer[100]; //infrared LED sensor data
uint32_t redBuffer[100];  //red LED sensor data
#endif

int32_t bufferLength; //Tamaño del dato
int32_t spo2; //valor SPO2
int8_t validSPO2; //Indicador para la lectura válida de SPO2
int32_t heartRate; //Valor del BPM
int8_t validHeartRate; //Indicador para la lectura válida de BPM

byte pulseLED = 12; //Debe ser un pin PWM
byte readLED = 13; //Parpadea con cada lectura 

/*
  Función setup 
*/
void setMAX(){
  //Definición de pines a utilizar
  pinMode(pulseLED, OUTPUT);
  pinMode(readLED, OUTPUT);

  //Creamos el objeto Wire
   Wire.begin (14,15);

  //Verificamos la conexión del sensor
  if (!particleSensor.begin(Wire, I2C_SPEED_FAST)) //Usamos el puerto I2C por default, 400kHz 
  {
    Serial.println(F("MAX30105 was not found. Please check wiring/power."));
    while (1);
  }

  Serial.println(F("Attach sensor to finger with rubber band. Readings Will Start after 5 seconds"));
  delay (5000);
  
  byte ledBrightness = 60; //Opciones: 0=Off to 255=50mA
  byte sampleAverage = 32; //Opciones: 1, 2, 4, 8, 16, 32
  byte ledMode = 2; //Opciones: 1 = Red only, 2 = Red + IR, 3 = Red + IR + Green
  byte sampleRate = 100; //Opciones: 50, 100, 200, 400, 800, 1000, 1600, 3200
  int pulseWidth = 411; //Opciones: 69, 118, 215, 411
  int adcRange = 16384; //Opciones: 2048, 4096, 8192, 16384

  //Iniciamos el sensor
  particleSensor.setup(ledBrightness, sampleAverage, ledMode, sampleRate, pulseWidth, adcRange);

   bufferLength = 100;

   for (byte i = 0 ; i < bufferLength ; i++)
  {
    while (particleSensor.available() == false) //Verificamos si hay nuevos datos
      particleSensor.check(); //Checamos los datos

    redBuffer[i] = particleSensor.getRed();
    irBuffer[i] = particleSensor.getIR();
    particleSensor.nextSample(); 

    Serial.print(F("red="));
    Serial.print(redBuffer[i], DEC);
    Serial.print(F(", ir="));
    Serial.println(irBuffer[i], DEC);
  }

  maxim_heart_rate_and_oxygen_saturation(irBuffer, bufferLength, redBuffer, &spo2, &validSPO2, &heartRate, &validHeartRate);
}

/*
  Función loop para el sensor MAX
*/
void MAXloop(){
  for (byte i = 25; i < 100; i++)
    {
      redBuffer[i - 25] = redBuffer[i];
      irBuffer[i - 25] = irBuffer[i];
    }

    //Toma 25 samples antes de dar el BPM
    for (byte i = 75; i < 100; i++)
    {
      while (particleSensor.available() == false) //Nuevos datos?
        particleSensor.check(); //Checamos por nuevos datos
      digitalWrite(readLED, !digitalRead(readLED)); //Parpadea para cada dato nuevo

      redBuffer[i] = particleSensor.getRed();
      irBuffer[i] = particleSensor.getIR();
      particleSensor.nextSample(); //Se finaliza

      Serial.print(F("HR="));
      Serial.print(heartRate, DEC);

      Serial.print(F(", SPO2="));
      Serial.println(spo2, DEC);

      //Envío de datos a ThingSpeak
      ThingSpeak.setField (1,heartRate); 
      ThingSpeak.setField (2,spo2);
    }

    //Después de 25 muestras, recalcula el BPM y SPO2
    maxim_heart_rate_and_oxygen_saturation(irBuffer, bufferLength, redBuffer, &spo2, &validSPO2, &heartRate, &validHeartRate);

  ThingSpeak.writeFields(chanelID,WriteKey);
  //Fin de lectura del sensor  
}
