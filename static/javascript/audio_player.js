var player = document.getElementById("audio_player");
var category_interval = 5000
var resp
var get_current_category = function() {
    $.ajax({
        url: "get_current_category",
        success: function(response) {
            resp = JSON.parse(response)
            document.getElementById("category_value").innerHTML = resp['prediction']
            document.getElementById("music_probability_value").innerHTML = 'Music: ' + resp['probabilities']['Music'] + '%'
            document.getElementById("speech_probability_value").innerHTML = 'Speech: ' + resp['probabilities']['Speech'] + '%'
            document.getElementById("ads_probability_value").innerHTML = 'Ads: ' + resp['probabilities']['Ads'] + '%'
        }
    })
}

function get_category() {
    var name_array = document.getElementById("sample_name").src.split('/')
    sample_name = name_array[name_array.length - 1]
    $.ajax({
        // type: "GET",
        url: "get_category/"+sample_name,
        data: JSON.stringify({'file_name' : sample_name}),
        contentType: 'application/json;charset=UTF-8',
        dataType: "json",
        success: function(response) {
            // var r = JSON.parse(response)
            var resp = response
            document.getElementById("category_value").innerHTML = response['prediction']
            document.getElementById("music_probability_value").innerHTML = 'Music: ' + response['probabilities']['Music'] + '%'
            document.getElementById("speech_probability_value").innerHTML = 'Speech: ' + response['probabilities']['Speech'] + '%'
            document.getElementById("ads_probability_value").innerHTML = 'Ads: ' + response['probabilities']['Ads'] + '%'
        }
    })
}

var category_interval_id

function play() {
    player.load();
    player.play();
}

function startPlayer() {
    player.load();
    player.play();
    category_interval_id = setInterval(get_current_category, category_interval)
}

function stopPlayer() {
    player.pause();
    clearInterval(category_interval_id);
}
