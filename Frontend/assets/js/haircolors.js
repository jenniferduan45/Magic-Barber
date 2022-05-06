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
    imgsrc = ["https://content.latest-hairstyles.com/wp-content/uploads/dark-neon-blue-hair-color.jpg", 
            "https://content.latest-hairstyles.com/wp-content/uploads/dark-neon-blue-hair-color.jpg",
            "https://content.latest-hairstyles.com/wp-content/uploads/dark-neon-blue-hair-color.jpg"]
    display_photo(imgsrc)
})