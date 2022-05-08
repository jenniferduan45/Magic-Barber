function upload_photo_and_get_recommendation(){
    var user_photo = $("#userphoto").prop('files')[0]
    console.log('Photo file : ', user_photo)
    var filepath = ($("#userphoto").val()).split("\\")
    var fileName = filepath[filepath.length - 1]
    console.log(fileName)

    var params = {
        'item': fileName,
        'folder': 'ccbd-hair-input-photos',
        'Content-Type': user_photo.type
    };
    var additionalParams = {
        'headers': {
            'Access-Control-Allow-Origin': '*'
        }
    };

    var reader = new FileReader()
    reader.onload = function (event) {
        body = btoa(event.target.result)
        console.log('Reader body : ', body)
        return apigClient.uploadFolderObjectPut(params, body, additionalParams)
        .then(function(result) {
            console.log(result);
        })
        .catch(function(error) {
            console.log(error);
        })
    }
    reader.readAsBinaryString(user_photo)
}

function redirect(){
    var url = "haircolors.html"
    $(location).attr('href', url)
}

$(document).ready(function(){
    $("#submit_photo").click(function(){
        upload_photo_and_get_recommendation()
        // redirect()
    })
})