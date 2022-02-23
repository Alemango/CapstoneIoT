/*
  Diplomado Internet de las cosas | Samsung Innovation Campus

  Proyecto Capstone: Asistente Médico
  Alumno: Juan Jesús Alemán Espriella

  Dispositivo: ESP32 (38 Pines)

  Descripción: Código que implementa los sensores MAX30100, DHT11 y MQ-135 para la obtención de BPM, SPO2 en un paciente, Temperatura, Humedad
              y calidad de aire en una habitación. Esta información se enviará a un servidor de ThingSpeak donde se almacenará y analizará la
              información. Además de enviar un mensaje MQTT a través del broker de HiveMQ que nos servirá para mantener actualizada la información
              en vivo desde la aplicación móvil.
*/

#include <WiFi.h> //Biblioteca para la conexión WiFi.
#include <PubSubClient.h> //Biblioteca para la conexión MQTT. Autor: Nick O'Leary
#include "ThingSpeak.h" //Biblioteca para la comunicación con ThingSpeak. Autor: MathWorks
#include "SensorMAX.h" //Archivo para el funcionamiento del sensor MAX30100
#include "DHT.h" //Biblioteca para el funcionamiento del sensor DHT11. Autor: Adafruit

#define pin1 13 //Definición del pin usado para el sensor DHT11
#define MQ135_THRESHOLD_1   1000 //Definición del límite de partículas para el sensor MQ-135

const char* ssid = "ESPRIELLAS";  //Nombre de red
const char* password = "?uU:FE%P6s9d9b";  //Contraseña de red

WiFiClient espClient; // Este objeto maneja los datos de conexion WiFi
PubSubClient client(espClient); // Este objeto maneja los datos de conexion al broker
DHT dht1(pin1, DHT11);    //Objeto para el sensor DHT

IPAddress server(18,198,247,0); //Dirección IP del broker MQTT

unsigned long channelID = 1648132; //Canal de ThingSpeak
const char* WriteAPIKey = "3BZO9QOJ5C6OBWF1"; //Clave de escritura para la API de Thingspeak

/*
  Función SetUp para el microcontrolador. Se realizan las instrucciones que sólo se ejecutarán una vez, como son: Conexión WiFi, e inicio de sensores.
*/
void setup() {
  Serial.begin(115200); //Se inicializa la conexión a 115200 baudios
  
  //Se imprime el intento de conexión WiFi
  Serial.println();
  Serial.println();
  Serial.print("Conectar a ");
  Serial.println(ssid); 

  WiFi.begin(ssid, password); // Esta es la función que realiza la conexión a WiFi

  //Función que reintenta la conexión WiFi
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(100);
  }

  //Se imprime la conexión a WiFi y la IP asignada
  Serial.println();
  Serial.println("WiFi conectado");
  Serial.println("Direccion IP: ");
  Serial.println(WiFi.localIP());

  delay(5000); //Retraso de 5 segundos

  client.setServer(server,1883); //Se realiza la conexión MQTT
  ThingSpeak.begin(espClient); //Se realiza la conexión con ThingSpeak

 setMAX(); //Se inicia el sensor MAX30100
 DHTsetup(); //Se inicia el sensor DHT
}

/*
  Función reconnect que intenta y reintenta la conexión MQTT.
*/
void reconnect() {
  // Loop hasta que se conecte
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Intento de conexión
    if (client.connect("espClient")) {
      Serial.println("connected");
      // Una vez conectado publica...
      client.publish("emma/prototipo/-Mryro7TSaIlYV7cMJns","nuevo");
      // ...y se suscribe
      client.subscribe("emma/prototipo/-Mryro7TSaIlYV7cMJns");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Espera 5 segundos para la siguiente conexión
      delay(5000);
    }
  }
}

/*
  Función loop que repite una serie de instrucciones mientras el microcontrolador esta encendido. Se incluye la lectura del sensor y el envío de la 
  información MQTT y a ThingSpeak.
*/
void loop() {

  //Conexión y reconexión MQTT
  if(!client.connected()){
    reconnect();
  }
client.loop(); //Loop que mantiene viva la conexión con el broker MQTT

 MAXloop(); //Lectura y envíos del sensor MAX30100
 leerdht1(); //Lectura y envíos del sensor DHT
 MQloop(); //Lectura y envíos del sensor MQ135

 ThingSpeak.writeFields(channelID,WriteAPIKey); //Datos para la escritura de información en ThingSpeak
 Serial.println("Datos enviados a ThingSpeak!"); 
 delay(20000); //Espera de 20 segundos, debido a que ThingSpeak tiene un tiempo de aceptación de datos de 14 segundos.
}

/*
  Función setup para el sensor Dht
*/
void DHTsetup() {
  
  Serial.begin(115200);
  Serial.println("Test de sensores:");

  dht1.begin(); //Se inicia el sensor DHT
  
}

/*
  Función de lectura y envío de datos para el sensor DHT
*/
void leerdht1() {
  
  //Creamos 2 variables de tipo float para el almacenamiento de la temperatura y humedad
  float t1 = dht1.readTemperature();
  float h1 = dht1.readHumidity();

  //Bucle para obtener lecturas válidas del sensor
  while (isnan(t1) || isnan(h1)){
    Serial.println("Lectura fallida en el sensor DHT11, repitiendo lectura...");
    delay(2000);
    t1 = dht1.readTemperature(); //Se almacena el valor de temperatura
    h1 = dht1.readHumidity(); //Se almacena el valor de humedad
  }

  //Se imprime el valor en °C
  Serial.print("Temperatura DHT11: ");
  Serial.print(t1);
  Serial.println(" ºC.");

  //Se imprime el % de humedad
  Serial.print("Humedad DHT11: ");
  Serial.print(h1);
  Serial.println(" %."); 

  Serial.println("-----------------------");

  //Se escriben envían y almacenan los datos en ThingSpeak
  ThingSpeak.setField (3,t1);
  ThingSpeak.setField (4,h1);
}

/*
  Función para la lectura del sensor MQ135
*/
void MQloop() {

   //Se inicia una variable para la lectura análoga del sensor MQ135 
   int MQ135_data = analogRead(A6);

  //Se compara la lectura obtenida con el límite definido desde el inicio
  if(MQ135_data < MQ135_THRESHOLD_1){
    Serial.print("Buena Calidad de Aire: ");
  } else {
    Serial.print("Mala Calidad de Aire: "); 
  }
    Serial.print(MQ135_data); // Datos obtenidos
    Serial.println(" PPM"); //Partes por millón
  
  Serial.println("*****************************************************");

  ThingSpeak.setField (5,MQ135_data); // Se envía el dato a ThingSpeak
}