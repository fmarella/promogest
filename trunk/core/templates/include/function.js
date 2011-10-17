function menu(id){
  if (document.getElementById){
    if(document.getElementById(id).style.display == 'none'){
        new Effect.BlindDown(id);
    }
    else {
        new Effect.BlindUp(id);
    }
  }
}


function visualizza(id){
  if (document.getElementById){
    if(document.getElementById(id).style.display == 'none'){
        new Effect.BlindDown(id);
    }
    else {
        new Effect.BlindUp(id);
    }
  }
}



var stile = "top=100, left=100, width=250, height=200, status=no, menubar=no, toolbar=no scrollbar=no";
    function Popup(url) {
        window.open(url, "", stile);
}
