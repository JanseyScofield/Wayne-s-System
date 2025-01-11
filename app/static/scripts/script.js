const urlPagina = 'https://glorious-space-xylophone-v6prw5vq7rp6h6pg5-5000.app.github.dev/';
const inputSenha = document.getElementById('senha');

function mostrarSenha(){
    if(inputSenha.type === 'password'){
        inputSenha.type = 'text';
    }
    else{
        inputSenha.type = 'password';
    }
}