function displayGallery(event) {
    var pswpElement = document.querySelectorAll('.pswp')[0];

    // define options (if needed)
    var options = {
        // optionName: 'option value'
        // for example:
        index: 0 // start at first slide
    };

    postData = {
        'csrfmiddlewaretoken': $('[name="csrfmiddlewaretoken"]').val()
    }
    
    if ('itemsIdList' in event['data']) {
        postData['itemsIdList'] = event['data']['itemsIdList'];
    }

    $.post(
        event['data']['url'],
        postData,
        function(galleryInfos, textStatus) {
            var gallery = new PhotoSwipe(pswpElement, PhotoSwipeUI_Default, galleryInfos, options);
            gallery.init();
        },
        "json"
    );
}
