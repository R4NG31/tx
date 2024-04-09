function listadoSitios(){
    $.ajax({
        url:"/sitios/listarSitios",
        type:"get",
        dataType: "json",
        success: function(response){
            console.log(response);

        },
        error: function(error){
            console.log(error);
        }
    });
}

$(document).ready(function () {
    listadoSitios();
});