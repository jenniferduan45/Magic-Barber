function display_result_button(){
    let button_row = $('<div class="row">')
    let button_container = $('<div class="col-md-12">')
    let button_item = $('<button id="haircolors_results">')
    button_item.html("Get Recommendations")
    button_container.append(button_item)
    button_row.append(button_container)
    let waiting_row = $('<div class="row">')
    let waiting_container = $('<div class="col-md-12">')
    let waiting_item = $('<div class="waiting_time">')
    waiting_item.html("Wait for 20 seconds and then click button to get dyed hair photos")
    waiting_container.append(waiting_item)
    waiting_row.append(waiting_container)
    $(".returnedhaircolors").append(button_row)
    $(".returnedhaircolors").append(waiting_row)
}

function send_request_get_result(){
    var additionalParams = {
        'headers': {
            'Access-Control-Allow-Origin': '*'
        }
    };
    apigClient.resultsGet({}, {}, additionalParams)
        .then(function(result) {
            console.log("Result : ", result);
            $(".returnedhaircolors").empty()
            display_photo(result["data"]["results"])
        }).catch(function(result) {
            console.log(result);
        });
}

function display_photo(list){
    var content_row = $('<div class="row">')
    $.each(list, function(index, value){
        let item_container = $('<div class="col-md-4">')
        let hair_color_item = $('<div class="hair_color">')
        let image_link = $('<img class="hairImageLink">')
        image_link.attr("src", value)
        image_link.attr("alt", "Image for hair color")
        hair_color_item.append(image_link)
        item_container.append(hair_color_item)
        content_row.append(item_container)
    })
    $(".returnedhaircolors").append(content_row)
}

$(document).ready(function(){
    display_result_button()
    $("#haircolors_results").click(function(){
        send_request_get_result()
    })
})