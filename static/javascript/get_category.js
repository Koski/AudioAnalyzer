(function(){
    setInterval(
        (function() {
            $.ajax({
                url: "get_category",
                success: function(response) {
                    document.getElementById("content").innerHTML = response
                }
            })
        }), 5000)
})()
