// Lightweight browser smoke checks, run via console on the published site.
// The project also has deterministic Python schema tests in tests/validate.py.
console.assert(document.querySelector('header')!==null,'navigation exists');
console.assert(document.querySelector('#main')!==null,'main exists');
