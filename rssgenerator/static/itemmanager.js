function Item(itemSummary) {
    this.itemSummary = itemSummary;
    
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

        return jQuery('<div/>')
            .addClass('thumb-menu')
            .append(gallery);
    }
    
    this.itemElement = jQuery('<figure/>')
        .attr('id', 'item' + this.itemSummary['id'])
        .addClass('thumb')
        .css('opacity', '0')
        .append(this.thumb());
//        .click(itemSummary['gallery'], displayGallery);
};
