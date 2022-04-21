const nombre = document.querySelector('[nombre]');
const sexo = document.querySelector('[sexo]');
const edad = document.querySelector('[edad]');
const altura = document.querySelector('[altura]');
const peso = document.querySelector('[peso]');
const alergias = document.querySelector('[alergias]');
const enfermedades = document.querySelector('[enfermedades]');
const contacto = document.querySelector('[contacto]');

const paciente = "-Mryro7TSaIlYV7cMJns";

fetch('https://emma-asistente-default-rtdb.firebaseio.com/ID/3ac35d1779c6404bb1f9bdacbaff7d9e/Pacientes.json')
  .then(response => response.json())
  .then(data => datosPaciente(data))

const datosPaciente = (data) => {
    nombre.textContent = data[paciente]["Nombre(s)"] + " " + data[paciente]["Apellido-Paterno"] + " " + data[paciente]["Apellido-Materno"];
    sexo.textContent = data[paciente]["Sexo"];
    edad.textContent = `${(data[paciente]["Edad"])} años`;
    altura.textContent = `${(data[paciente]["Estatura"])} cm`;
    peso.textContent = `${(data[paciente]["Peso"])} kg`;
    alergias.textContent = data[paciente]["Alergias"];
    enfermedades.textContent = data[paciente]["Enfermedades"];
    contacto.textContent = data[paciente]["Tel"];
}