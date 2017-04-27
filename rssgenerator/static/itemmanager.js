function Item(itemSummary) {
    this.itemSummary = itemSummary;
    
    this.thumb = function() {
        var img = jQuery('<img/>')
            .attr('id', 'picItem' + this.itemSummary['id']);
        
        return jQuery('<a/>')
            .attr('href', '#')
            .append(img);
    }
    
    // <div class="divItem" style="display:none">...</div>
    this.itemElement = jQuery('<figure/>')
        .attr('id', 'item' + this.itemSummary['id'])
        .addClass('thumb')
        .css('opacity', '0')
        .append(this.thumb())
        .click(itemSummary['gallery'], displayGallery);
};
