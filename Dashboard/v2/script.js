const pacUno = document.querySelector('[pacienteUno]');
const pacDos = document.querySelector('[pacienteDos]');
const pacTres = document.querySelector('[pacienteTres]');
const pacCuatro = document.querySelector('[pacienteCuatro]');
const pacCinco = document.querySelector('[pacienteCinco]');
const pacSeis = document.querySelector('[pacienteSeis]');

const edadUno = document.querySelector('[edadUno]');
const edadDos = document.querySelector('[edadDos]');
const edadTres = document.querySelector('[edadTres]');
const edadCuatro = document.querySelector('[edadCuatro]');
const edadCinco = document.querySelector('[edadCinco]');
const edadSeis = document.querySelector('[edadSeis]');

const pesoUno = document.querySelector('[pesoUno]');
const pesoDos = document.querySelector('[pesoDos]');
const pesoTres = document.querySelector('[pesoTres]');
const pesoCuatro = document.querySelector('[pesoCuatro]');
const pesoCinco = document.querySelector('[pesoCinco]');
const pesoSeis = document.querySelector('[pesoSeis]');

const estaturaUno = document.querySelector('[estaturaUno]');
const estaturaDos = document.querySelector('[estaturaDos]');
const estaturaTres = document.querySelector('[estaturaTres]');
const estaturaCuatro = document.querySelector('[estaturaCuatro]');
const estaturaCinco = document.querySelector('[estaturaCinco]');
const estaturaSeis = document.querySelector('[estaturaSeis]');


fetch('https://emma-asistente-default-rtdb.firebaseio.com/ID/3ac35d1779c6404bb1f9bdacbaff7d9e/Pacientes.json')
  .then(response => response.json())
  .then(data => datosPaciente(data))


const datosPaciente = (data) => {
    pacUno.textContent = data["-Mrd9wLWtzqRy3abL3Iv"]["Nombre(s)"] + " " + data["-Mrd9wLWtzqRy3abL3Iv"]["Apellido-Paterno"] + " " + data["-Mrd9wLWtzqRy3abL3Iv"]["Apellido-Materno"];
    pacDos.textContent = data["-Mryro7TSaIlYV7cMJns"]["Nombre(s)"] + " " + data["-Mryro7TSaIlYV7cMJns"]["Apellido-Paterno"] + " " + data["-Mryro7TSaIlYV7cMJns"]["Apellido-Materno"];
    pacTres.textContent = data["-MtKPf4S46fXu8oXNIfv"]["Nombre(s)"] + " " + data["-MtKPf4S46fXu8oXNIfv"]["Apellido-Paterno"] + " " + data["-MtKPf4S46fXu8oXNIfv"]["Apellido-Materno"];
    pacCuatro.textContent = data["-MtKQOjlf5ehHTtJV2BE"]["Nombre(s)"] + " " + data["-MtKQOjlf5ehHTtJV2BE"]["Apellido-Paterno"] + " " + data["-MtKQOjlf5ehHTtJV2BE"]["Apellido-Materno"];
    pacCinco.textContent = data["-MtKRepi4Zqo7C9PminP"]["Nombre(s)"] + " " + data["-MtKRepi4Zqo7C9PminP"]["Apellido-Paterno"] + " " + data["-MtKRepi4Zqo7C9PminP"]["Apellido-Materno"];

    edadUno.textContent = `Edad: ${data["-Mrd9wLWtzqRy3abL3Iv"]["Edad"]} años`;
    edadDos.textContent = `Edad: ${data["-Mryro7TSaIlYV7cMJns"]["Edad"]} años`;
    edadTres.textContent = `Edad: ${data["-MtKPf4S46fXu8oXNIfv"]["Edad"]} años`;
    edadCuatro.textContent = `Edad: ${data["-MtKQOjlf5ehHTtJV2BE"]["Edad"]} años`;
    edadCinco.textContent = `Edad: ${data["-MtKRepi4Zqo7C9PminP"]["Edad"]} años`;

    pesoUno.textContent = `Peso: ${data["-Mrd9wLWtzqRy3abL3Iv"]["Peso"]} kg`;
    pesoDos.textContent = `Peso: ${data["-Mryro7TSaIlYV7cMJns"]["Peso"]} kg`;
    pesoTres.textContent = `Peso: ${data["-MtKPf4S46fXu8oXNIfv"]["Peso"]} kg`;
    pesoCuatro.textContent = `Peso: ${data["-MtKQOjlf5ehHTtJV2BE"]["Peso"]} kg`;
    pesoCinco.textContent = `Peso: ${data["-MtKRepi4Zqo7C9PminP"]["Peso"]} kg`;

    estaturaUno.textContent = `Estatura: ${data["-Mrd9wLWtzqRy3abL3Iv"]["Estatura"]} cm`;
    estaturaDos.textContent = `Estatura: ${data["-Mryro7TSaIlYV7cMJns"]["Estatura"]} cm`;
    estaturaTres.textContent = `Estatura: ${data["-MtKPf4S46fXu8oXNIfv"]["Estatura"]} cm`;
    estaturaCuatro.textContent = `Estatura: ${data["-MtKQOjlf5ehHTtJV2BE"]["Estatura"]} cm`;
    estaturaCinco.textContent = `Estatura: ${data["-MtKRepi4Zqo7C9PminP"]["Estatura"]} cm`;
}