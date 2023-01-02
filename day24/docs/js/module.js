function fnc1() {
  const pModule = document.createElement('p');
  pModule.textContent = 'module.fnc1 より😎️';
  console.log('module');
  return pModule;
}

export { fnc1 };
