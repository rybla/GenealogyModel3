$( document ).ready(function(){
    console.log("lakfjlaksdjl")
    document.getElementById("submitbutton").onclick = function(){


        console.log("kjnasdasd");

        var result = {
            'fname': document.getElementById('fname').value,
            'lname': document.getElementById('lname').value,
        }
        $.ajax({
            type: 'POST',
            url: "/get_plot",
            data: result,
            dataType: "text",
            success: function(data){
                var container = document.getElementById("svg_item");
                container.innerHTML = data;
                //var img = document.getElementById('img');
                //var url = window.URL || window.webkitURL;
                //img.src = url.createObjectURL(data);
            }
        })
    }
})
