function displayGallery(event) {
    if ('itemsIdList' in event['data']) {
        getThenDisplayGalleryInfos(event['data']['url'], event['data']['shuffle'], new Array(0), event['data']['itemsIdList'], 0);
    }
}

function getThenDisplayGalleryInfos(url, shuffle, galleryInfos, itemsIdList, startPos) {
    var maxLength = 200;
    var max = itemsIdList.length - 1;
    
    if(startPos <= max) {
        $.post(
            url,
            {
                'csrfmiddlewaretoken': $('[name="csrfmiddlewaretoken"]').val(),
                'itemsIdList': itemsIdList.slice(startPos, startPos + maxLength)
            },
            function(queryGalleryInfos, textStatus) {
                getThenDisplayGalleryInfos(url, shuffle, galleryInfos.concat(queryGalleryInfos), itemsIdList, startPos + maxLength);
            },
            "json"
        );
        
        return;
    }
    
    displayGalleryInfos(galleryInfos, shuffle);
}

function displayGalleryInfos(galleryInfos, shuffle) {
    if(shuffle === 'true') {
        galleryInfos = shuffleArray(galleryInfos);
    }
    
    var pswpElement = document.querySelectorAll('.pswp')[0];
    
    // define options (if needed)
    var options = {
        // optionName: 'option value'
        // for example:
        index: 0 // start at first slide
    };
    
    var gallery = new PhotoSwipe(pswpElement, PhotoSwipeUI_Default, galleryInfos, options);
    gallery.init();
}

function shuffleArray(array) {
    var currentIndex = array.length, temporaryValue, randomIndex;

    // While there remain elements to shuffle...
    while (0 !== currentIndex) {
        // Pick a remaining element...
        randomIndex = Math.floor(Math.random() * currentIndex);
        currentIndex -= 1;

        // And swap it with the current element.
        temporaryValue = array[currentIndex];
        array[currentIndex] = array[randomIndex];
        array[randomIndex] = temporaryValue;
    }

    return array;
}

function setFocus(e, checkBoxId, textBoxId) {
    var checkBox = document.getElementById(checkBoxId);
    if (checkBox.checked == true) {
        document.getElementById(textBoxId).focus();
    }
}
