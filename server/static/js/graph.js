function verify_user_args(){
    retval = true;
    if(!(Number(document.getElementById('Mval').value) > 0)){
        $("#Mvalerr").show()
        retval = false
    }
    if(!(Number(document.getElementById('Nval').value) > 0)){
        $("#Nvalerr").show()
        retval = false
    }
    if(!(Number(document.getElementById('Pval').value) > 0)){
        $("#Pvalerr").show()
        retval = false
    }
    if(!(Number(document.getElementById('RedSurvival').value) > 0 &&
         Number(document.getElementById('BlueSurvival').value) > 0)){
        $("#Survivalerr").show()
        retval = false
    }
    if(!(Number(document.getElementById('RedStart').value) > 0 &&
         Number(document.getElementById('BlueStart').value) > 0)){
        $("#Starterr").show()
        retval = false
    }
    if(!(Number(document.getElementById('Cval').value) >= 0)){
        $("#Cvalerr").show()
        retval = false
    }
    return retval
}
function hide_all(){
    $("#Mvalerr").hide()
    $("#Nvalerr").hide()
    $("#Pvalerr").hide()
    $("#Survivalerr").hide()
    $("#Starterr").hide()
    $("#Cvalerr").hide()
}
function load_svg(){
    hide_all()
    if(!verify_user_args()){
        return false;
    }
    console.log("kjnasdasd");

    var result = {
        'Mval': document.getElementById('Mval').value,
        'Nval': document.getElementById('Nval').value,
        'Pval': document.getElementById('Pval').value,
        'RedSurvival': document.getElementById('RedSurvival').value,
        'BlueSurvival': document.getElementById('BlueSurvival').value,
        'RedStart': document.getElementById('RedStart').value,
        'BlueStart': document.getElementById('BlueStart').value,
        'Aval': document.getElementById('Aval').value,
        'Cval': document.getElementById('Cval').value,
    }
    $.ajax({
        type: 'POST',
        url: "/get_plot",
        data: result,
        dataType: "text",
        cache: false,
        success: function(data){
            var container = document.getElementById("svg_item");
            container.innerHTML = data;
        }
    })
    return true;
}

$( document ).ready(function(){
    load_svg()
    console.log("lakfjlaksdjl")
    document.getElementById("submitbutton").onclick = load_svg
})
