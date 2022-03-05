// % Diplomado Internet de las cosas | Samsung Innovation Campus | Código IoT

// % Proyecto Capstone: Asistente Médico
// % Alumno: Juan Jesús Alemán Espriella

// % Script para ThingSpeak - MatLab Analysis

readChannelID = 1648132; // % Canal del cual se leerá la información

// % Campos de los cuales se leerá la información
bpmFieldID = 1; 
spoFieldID = 2;
tempFieldID = 3;
humFieldID = 4;
ppmFieldID = 5;

// % Clave para leer información del canal
readAPIKey = ''; 

// % Guardamos en las varieables los datos de las lecturas de 10 min de información anterior
bpm = thingSpeakRead(readChannelID,'Fields',bpmFieldID,'NumMinutes',10,'ReadKey',readAPIKey); 
spo2 = thingSpeakRead(readChannelID,'Fields',spoFieldID,'NumMinutes',10,'ReadKey',readAPIKey); 
temp = thingSpeakRead(readChannelID,'Fields',tempFieldID,'NumMinutes',10,'ReadKey',readAPIKey); 
hum = thingSpeakRead(readChannelID,'Fields',humFieldID,'NumMinutes',10,'ReadKey',readAPIKey); 
ppm = thingSpeakRead(readChannelID,'Fields',ppmFieldID,'NumMinutes',10,'ReadKey',readAPIKey); 

// % Calculamos sus promedios y los mostramos en pantalla
avgBPM = mean(bpm); 
display(avgBPM,'Average BPM'); 

avgSPO = mean(spo2); 
display(avgSPO,'Average SPO2'); 

avgTemp = mean(temp); 
display(avgTemp,'Average °C'); 

avgHum = mean(hum); 
display(avgHum,'Average % Hum'); 

avgPPM = mean(ppm); 
display(avgPPM,'Average PPM'); 

// % ID del canal donde escribiremos los datos
writeChannelID = 1651186; 

// % Clave para escribir los datos en el canal
writeAPIKey = 'XF5UR7HIJIEF6DTY'; 

// % Escribimos en el canal indicado, los promedios, en los respectivos campos usando la clave
thingSpeakWrite(writeChannelID,[avgBPM,avgSPO,avgTemp,avgHum,avgPPM],'Fields',[1,2,3,4,5],'WriteKey',writeAPIKey);