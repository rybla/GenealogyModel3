var current_result;
function checkposint(num_str){
    return /^(0|[1-9]\d*)$/.test(num_str)
}
function check_num(num_str){
    return num_str
}
function check_non_neg(num_str){
    return num_str && Number(num_str) >= 0
}
function check_proportion(num_str){
    return num_str && Number(num_str) >= 0 &&  Number(num_str) <= 1
}
function verify_user_args(result){
    retval = true;
    if(!(checkposint(result['Mval']))){
        $("#Mvalerr").show()
        retval = false
    }
    if(!(checkposint(result['Nval']))){
        $("#Nvalerr").show()
        retval = false
    }
    if(!(checkposint(result['Pval']))){
        $("#Pvalerr").show()
        retval = false
    }
    /*if(!(checkposint(document.getElementById('RedSurvival').value) &&
         checkposint(document.getElementById('BlueSurvival').value))){
        $("#Survivalerr").show()
        retval = false
    }*/
    /*if(!(checkposint(document.getElementById('RedStart').value) &&
         checkposint(document.getElementById('BlueStart').value))){
        $("#Starterr").show()
        retval = false
    }*/
    if(!(check_proportion(result['RedPropStart']))){
        $("#StartPropErr").show()
        retval = false
    }
    if(!(check_proportion(result['DarkPropStart']))){
        $("#StartPropErr").show()
        retval = false
    }
    if(!(check_non_neg(result['Aval']))){
        $("#Avalerr").show()
        retval = false
    }
    if(!(check_num(result['Cval']))){
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
    //$("#Starterr").hide()
    $("#Cvalerr").hide()
}
function place_text_on_svg(text){
    $("#downloadbutton").hide()
    document.getElementById("svg_item").innerHTML = text
}
function get_result(){
    return {
        'Mval': document.getElementById('Mval').value,
        'Nval': document.getElementById('Nval').value,
        'Pval': document.getElementById('Pval').value,
        'WithReplacement': document.getElementById('with_replacement').checked ? "true" : "false",
        'DarkBlueSurv': document.getElementById('DarkBlueSurv').value,
        'DarkRedSurv': document.getElementById('DarkRedSurv').value,
        'LightBlueSurv': document.getElementById('LightBlueSurv').value,
        'LightRedSurv': document.getElementById('LightRedSurv').value,
        //'DarkBlueStart': document.getElementById('DarkBlueStart').value,
        //'DarkRedStart': document.getElementById('DarkRedStart').value,
        //'LightBlueStart': document.getElementById('LightBlueStart').value,
        //'LightRedStart': document.getElementById('LightRedStart').value,
        'RedPropStart': document.getElementById('RedPropStart').value,
        'DarkPropStart': document.getElementById('DarkPropStart').value,
        'RedSurvival': document.getElementById('RedSurvival').value,
        'BlueSurvival': document.getElementById('BlueSurvival').value,
        //'RedStart': document.getElementById('RedStart').value,
        //'BlueStart': document.getElementById('BlueStart').value,
        'Aval': document.getElementById('Aval').value,
        'Cval': document.getElementById('Cval').value,
        'should_run_fast': document.getElementById('fast_checkbox').checked ? "true" : "false",
        'use_single_trait': document.getElementById("single_trait_id").checked ? "true" : "false",
    }
}
function load_svg(){
    var result = get_result()
    console.log(JSON.stringify(result))
    hide_all()
    if(!verify_user_args(result)){
        place_text_on_svg("Bad user input")
        return false;
    }
    place_text_on_svg("Loading...")
    console.log("kjnasdasd");

    current_result = result
    get_svg(result)
    return true;
}
function download_data(filename, data) {
    var blob = new Blob([data], {type: 'text/svg'});
    if(window.navigator.msSaveOrOpenBlob) {
        window.navigator.msSaveBlob(blob, filename);
    }
    else{
        var elem = window.document.createElement('a');
        elem.href = window.URL.createObjectURL(blob);
        elem.download = filename;
        document.body.appendChild(elem);
        elem.click();
        document.body.removeChild(elem);
    }
}
function on_download_click(){
    download_data($.param(current_result)+".svg",document.getElementById("svg_item").innerHTML)
}
function radio_change(){
    document.getElementById("single_trait_id").onclick = function(){
        $(".single_trait_survival").show()
        $(".two_trait_survival").hide()
    }
    document.getElementById("two_trait_id").onclick = function(){
        $(".single_trait_survival").hide()
        $(".two_trait_survival").show()
    }
}
$( document ).ready(function(){
    load_svg()
    radio_change()
    console.log("lakfjlaksdjl")
    document.getElementById("submitbutton").onclick = load_svg
    document.getElementById("downloadbutton").onclick = on_download_click
})
