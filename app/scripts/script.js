const inputSenha = document.getElementById('senha');

function mostrarSenha(){
    if(inputSenha.type === 'password'){
        inputSenha.type = 'text';
    }
    else{
        inputSenha.type = 'password';
    }
}