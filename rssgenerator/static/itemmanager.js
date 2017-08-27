function Item(itemSummary) {
    this.itemSummary = itemSummary;
    this.thumbPreview;
    
    this.thumb = function() {
        return jQuery('<div/>')
            .addClass('thumb-content')
            .append(this.preview())
            .append(this.menu());
    }
    
    this.preview = function() {
        return jQuery('<img/>')
            .addClass('thumb-preview')
            .attr('id', 'picItem' + this.itemSummary['id']);
    }
    
    this.menu = function() {
        var gallery = jQuery('<div/>')
            .addClass('thumb-menu-item')
            .addClass('fa')
            .addClass('fa-play-circle-o')
            .addClass('fa-2x')
            .click(itemSummary['gallery'], displayGallery);
            
        var infos = jQuery('<div/>')
            .addClass('thumb-menu-item')
            .addClass('fa')
            .addClass('fa-info-circle')
            .addClass('fa-2x')
            .click( {
                        'itemId': 'picItem' + this.itemSummary['id'],
                        'summary': itemSummary
                    },
                    displayItemInfos);

        return jQuery('<div/>')
            .addClass('thumb-menu')
            .append(gallery)
            .append(infos);
    }
    
    this.itemElement = jQuery('<figure/>')
        .attr('id', 'item' + this.itemSummary['id'])
        .addClass('thumb')
        .css('opacity', '0')
        .append(this.thumb());
};

function displayItemInfos(event) {
    console.log(event);
}
