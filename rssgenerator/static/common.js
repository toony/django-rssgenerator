function displayGallery(event) {
    var pswpElement = document.querySelectorAll('.pswp')[0];

    // define options (if needed)
    var options = {
        // optionName: 'option value'
        // for example:
        index: 0 // start at first slide
    };
    
    $.getJSON(event['data'], function(galleryInfos) {
        var gallery = new PhotoSwipe(pswpElement, PhotoSwipeUI_Default, galleryInfos, options);
        gallery.init();
    });
}
