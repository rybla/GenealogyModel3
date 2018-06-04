function get_svg(result){
    console.log(result)

    $.ajax({
        type: 'POST',
        url: "/get_plot",
        data: result,
        dataType: "text",
        cache: false,
        success: function(data){
            $("#downloadbutton").show()
            var container = document.getElementById("svg_item");
            container.innerHTML = data;
        }
    })
}
