const showTimeNow = () =>{
    //Selecinando a tag de destino
      const clockTag = document.querySelector('time');
      
    //Instanciando a classe Date
      let dateNow = new Date();
    //pegando os valores desejados
      let hh = dateNow.getHours();
      let mm = dateNow.getMinutes();
      let ss = dateNow.getSeconds();
      
    //validando a necessidade de adicionar zero na exibição
      hh = hh < 10 ? '0'+ hh : hh; 
      mm = mm < 10 ? '0'+ mm : mm; 
      ss = ss < 10 ? '0'+ ss : ss; 
       
    // atribuindo os valores e montando o formato da hora a ser exibido
      clockTag.innerText = hh +':'+ mm +':'+ ss;
    }
    //executando a funcao a cada 1 segundo
    showTimeNow()
    setInterval(showTimeNow, 1000);