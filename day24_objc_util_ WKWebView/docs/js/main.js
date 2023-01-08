import { fnc1 } from './module.js';

const pTag = document.createElement('p');
pTag.textContent = 'js より☺️';

document.body.appendChild(pTag);

const pImport = fnc1();
document.body.appendChild(pImport);

console.log('main');
