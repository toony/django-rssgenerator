function Item(itemSummary) {
    this.itemSummary = itemSummary;
    this.thumbPreview;
    
    this.thumb = function() {
        return jQuery('<div/>')
            .addClass('thumb-content')
            .append(this.preview())
            .append(this.infos())
            .append(this.menu());
    }
    
    this.preview = function() {
        return jQuery('<img/>')
            .addClass('thumb-preview')
            .attr('id', 'picItem' + this.itemSummary['id']);
    }
    
    this.infos = function() {
        pubDate = jQuery('<div/>')
            .attr('id', 'infos-date-item' + this.itemSummary['id'])
            .addClass('thumb-infos-date')
            .append(this.itemSummary['pub_date']);
        
        title = jQuery('<div/>')
            .attr('id', 'infos-title-item' + this.itemSummary['id'])
            .addClass('thumb-infos-title')
            .append(this.itemSummary['title']);

        summary = jQuery('<div/>')
            .attr('id', 'infos-summary-item' + this.itemSummary['id'])
            .addClass('thumb-infos-summary')
            .append(this.itemSummary['summary']);
            
        totalLinks = jQuery('<div/>')
            .attr('id', 'infos-totallinks-item' + this.itemSummary['id'])
            .addClass('thumb-infos-totallinks')
            .append(jQuery('<span/>').append(this.itemSummary['totalLinks']));
            
        return jQuery('<div/>')
            .attr('id', 'infos-item' + this.itemSummary['id'])
            .addClass('thumb-infos')
            .append(pubDate)
            .append(title)
            .append(summary)
            .append(totalLinks);
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
            .hover( function() {
                        $('#infos-item'+ itemSummary['id']).attr('style', 'visibility: visible');
                    },
                    function() {
                        $('#infos-item'+ itemSummary['id']).removeAttr('style');
                    }
                  );

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
