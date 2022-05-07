function search(input) {
    const data = [
        {
            "BusinessId": "123456789",
            "BusinessName": "155 Barber Shop",
            "Address": "155 Manhattan Ave, New York, NY 10025",
            "PhoneNumber": "(646) 422-7200",
            "Image": "https://diana-cdn.naturallycurly.com/Articles/BP_NY-Salons-.jpg"
        },
        {
            "BusinessId": "123456789",
            "BusinessName": "155 Barber Shop",
            "Address": "155 Manhattan Ave, New York, NY 10025",
            "PhoneNumber": "(646) 422-7200",
            "Image": "https://diana-cdn.naturallycurly.com/Articles/BP_NY-Salons-.jpg"
        },
        {
            "BusinessId": "123456789",
            "BusinessName": "155 Barber Shop",
            "Address": "155 Manhattan Ave, New York, NY 10025",
            "PhoneNumber": "(646) 422-7200",
            "Image": "https://diana-cdn.naturallycurly.com/Articles/BP_NY-Salons-.jpg"
        },
        {
            "BusinessId": "123456789",
            "BusinessName": "155 Barber Shop",
            "Address": "155 Manhattan Ave, New York, NY 10025",
            "PhoneNumber": "(646) 422-7200",
            "Image": "https://diana-cdn.naturallycurly.com/Articles/BP_NY-Salons-.jpg"
        },
        {
            "BusinessId": "123456789",
            "BusinessName": "155 Barber Shop",
            "Address": "155 Manhattan Ave, New York, NY 10025",
            "PhoneNumber": "(646) 422-7200",
            "Image": "https://diana-cdn.naturallycurly.com/Articles/BP_NY-Salons-.jpg"
        },
        {
            "BusinessId": "123456789",
            "BusinessName": "155 Barber Shop",
            "Address": "155 Manhattan Ave, New York, NY 10025",
            "PhoneNumber": "(646) 422-7200",
            "Image": "https://diana-cdn.naturallycurly.com/Articles/BP_NY-Salons-.jpg"
        }
    ]
    return data
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
        var results = search(search_text)
        console.log(results)
        display_search_result(results)
    })
})