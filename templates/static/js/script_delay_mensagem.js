setTimeout(() => {
    const mensagemDiv = document.querySelector('#mensagem');
    if (mensagemDiv) {
      mensagemDiv.remove();
    }
  }, 5000);