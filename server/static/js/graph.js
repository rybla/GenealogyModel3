function load_svg(){
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
}

$( document ).ready(function(){
    load_svg()
    console.log("lakfjlaksdjl")
    document.getElementById("submitbutton").onclick = load_svg
})
