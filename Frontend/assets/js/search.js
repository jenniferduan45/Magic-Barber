function search(input) {
    var params = {
        'q' : input
    };

    var additionalParams = {
        'headers': {
            'Access-Control-Allow-Origin': '*'
        }
    };
    
    apigClient.searchGet(params, {}, additionalParams)
        .then(function(result) {
            console.log("Result : ", result);
            display_search_result(result["data"]["results"])
        }).catch(function(result) {
            console.log(result);
        });
}

function display_search_result(list){
    $(".results").empty()
    if (list.length== 0){
        let result_item = $('<div class="displayResultItem">')
        result_item.html("No results found")
        $(".results").append(result_item)
    } else {
        var content_row = $('<div class="row">')
        $.each(list, function(index, value){
            let item_container =  $('<div class="col-md-4">')
            let result_item = $('<div class="displayResultItem">')
            let name = $('<div class="entryName">')
            name.html(value["BusinessName"])
            let rating = $('<div class="entryRating">')
            rating.html("Rating: " + value["Rating"])
            let address = $('<div class="entryAddress">')
            address.html(value["Address"])
            let phone = $('<div class="entryPhone">')
            phone.html(value["PhoneNumber"])
            let image = $('<div class="entryImage">')
            let image_link = $('<img class="entryImageLink">')
            image_link.attr("src", value["Image"])
            image_link.attr("alt", "Image for "+value["BusinessName"])
            image.append(image_link)
            result_item.append(name)
            result_item.append(rating)
            result_item.append(address)
            result_item.append(phone)
            result_item.append(image)
            item_container.append(result_item)
            content_row.append(item_container)
            console.log("One item added")
        })
        $(".results").append(content_row)
    }
}

$(document).ready(function(){
    $(".results").empty()
    
    $("#submit_search").click(function(){
        var search_text = $("#searchInput").val()
        search(search_text)
    })
})