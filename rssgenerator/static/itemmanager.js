function Item(itemSummary) {
    this.itemSummary = itemSummary;
    
    this.thumb = function() {
        var img = jQuery('<img/>')
            .attr('id', 'picItem' + this.itemSummary['id']);
        
        return jQuery('<a/>')
            .attr('href', '#')
            .append(img);
    }
    
    this.leftPartElement = function() {
        //<div class="divItemLeft">
        //    <img class="itemImage pointer" src="${pic}"/>
        //    <div class="itemLinksBubble">
        //        <div class="itemLinksCount">${totalLinks}</div>
        //    </div>
        //</div>
        var left = jQuery('<div/>')
            .addClass('divItemLeft')
            .append(this.picElement(this.itemSummary['id']))
            .append(this.bubbleElement(this.itemSummary['totalLinks']));
            
        if(typeof this.itemSummary['gallery'] != 'undefined') {
            $(left).click(itemSummary['gallery'], displayGallery);
        }
        
        return left;
    };
    
    this.picElement = function(itemId) {
        // <img id=... class="itemImage pointer"/>
        return jQuery('<img/>')
            .attr('id', 'picItem' + itemId)
            .addClass('itemImage').addClass('pointer');
    };
    
    this.bubbleElement = function(totalLinks) {
        // <div class="itemLinksBubble">
        //    <div class="itemLinksCount">${totalLinks}</div>
        // </div>
        var number = jQuery('<div/>')
            .addClass('itemLinksCount')
            .text(totalLinks);
            
        return jQuery('<div/>')
            .addClass('itemLinksBubble')
            .append(number);
    };
    
    this.rightPartElement = function() {
        // <div class="divItemRightParent">
        //     <div class="divItemRight">
        //         <p class="itemTitle">${title}</p>
        //         <p class="itemDate">${pub_date}</p>
        //         <p class="itemSummary">${summary}</p>
        //     </div>
        // </div>
        var divInfo = jQuery('<div/>')
            .addClass('divItemRight')
            .append(this.titleElement(this.itemSummary['title']))
            .append(this.pubDateElement(this.itemSummary['pub_date']))
            .append(this.summaryElement(this.itemSummary['summary']));
            
        return jQuery('<div/>')
            .addClass('divItemRightParent')
            .append(divInfo);
    };
    
    this.titleElement = function(title) {
        // <p class="itemTitle">${title}</p>
        return jQuery('<p/>')
            .addClass('itemTitle')
            .text(title);
    };
    
    this.pubDateElement = function(pubDate) {
        // <p class="itemDate">${pub_date}</p>
        return jQuery('<p/>')
            .addClass('itemDate')
            .text(pubDate);
    };
    
    this.summaryElement = function(summary) {
        // <p class="itemSummary">${summary}</p>
        return jQuery('<p/>')
            .addClass('itemSummary')
            .text(summary);
    };
    
    // <div class="divItem" style="display:none">...</div>
    this.itemElement = jQuery('<figure/>')
        .attr('id', 'item' + this.itemSummary['id'])
        .addClass('thumb')
        .css('opacity', '0')
        .append(this.thumb());

    var preLoadPic = new Image();
    preLoadPic.onload = function() {
        // Add src to picItem and display item
        $('#picItem' + itemSummary['id']).attr('src', this.src);
        //itemElement.css("display", "inline");
        $('#item' + itemSummary['id']).delay(500).show().animate({opacity:1},3000);
    };
    preLoadPic.src = itemSummary['pic'];
};
