#include <WiFi.h>
#include <PubSubClient.h>
#include "ThingSpeak.h"
#include "SensorMAX.h"
#include "DHT.h"

#define pin1 13

const char* ssid = "ESPRIELLAS";  // Aquí debes poner el nombre de tu red
const char* password = "?uU:FE%P6s9d9b";  // Aquí debes poner la contraseña de tu red

WiFiClient espClient; // Este objeto maneja los datos de conexion WiFi
PubSubClient client(espClient); // Este objeto maneja los datos de conexion al broker
DHT dht1(pin1, DHT11);    //El azul.

IPAddress server(18,198,247,0);

unsigned long channelID = 1648132;
const char* WriteAPIKey = "3BZO9QOJ5C6OBWF1";

void setup() {
  Serial.begin(115200);
  
  Serial.println();
  Serial.println();
  Serial.print("Conectar a ");
  Serial.println(ssid);

  WiFi.begin(ssid, password); // Esta es la función que realiza la conexión a WiFi

  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(100);
  }

  Serial.println();
  Serial.println("WiFi conectado");
  Serial.println("Direccion IP: ");
  Serial.println(WiFi.localIP());

  delay(5000);

  client.setServer(server,1883);
  ThingSpeak.begin(espClient);

 setMAX();
 DHTsetup();
}

void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Attempt to connect
    if (client.connect("espClient")) {
      Serial.println("connected");
      // Once connected, publish an announcement...
      client.publish("emma/prototipo/-Mryro7TSaIlYV7cMJns","nuevo");
      // ... and resubscribe
      client.subscribe("emma/prototipo/-Mryro7TSaIlYV7cMJns");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}

void loop() {

  if(!client.connected()){
    reconnect();
  }
client.loop();

 MAXloop();
 leerdht1();

 ThingSpeak.writeFields(channelID,WriteAPIKey);
 Serial.println("Datos enviados a ThingSpeak!");
 delay(20000);
}

void DHTsetup() {
  
  Serial.begin(115200);
  Serial.println("Test de sensores:");

  dht1.begin();
  
}

void leerdht1() {
  
  float t1 = dht1.readTemperature();
  float h1 = dht1.readHumidity();

  while (isnan(t1) || isnan(h1)){
    Serial.println("Lectura fallida en el sensor DHT11, repitiendo lectura...");
    delay(2000);
    t1 = dht1.readTemperature();
    h1 = dht1.readHumidity();
  }

  Serial.print("Temperatura DHT11: ");
  Serial.print(t1);
  Serial.println(" ºC.");

  Serial.print("Humedad DHT11: ");
  Serial.print(h1);
  Serial.println(" %."); 

  Serial.println("-----------------------");

  ThingSpeak.setField (3,t1);
  ThingSpeak.setField (4,h1);
}
