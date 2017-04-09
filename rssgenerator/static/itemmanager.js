function Item(itemSummary) {
    this.itemSummary = itemSummary;
    
    this.display = function() {
        // <div class="divItem" style="display:none">...</div>
        this.itemElement = jQuery('<div/>')
            .attr('id', 'item' + this.itemSummary['number'])
            .addClass('divItem')
            .css('display', 'none')
            .append(this.leftPartElement())
            .append(this.rightPartElement());

        var itemElement = this.itemElement;
        var preLoadPic = new Image();
        preLoadPic.onload = function() {
            // Add src to picItem and display item
            $('#content').append(itemElement);
            $('#picItem' + itemSummary['number']).attr('src', this.src);
            itemElement.css("display", "inline");
            itemElement.delay(500).show().animate({opacity:1},3000);
        };
        preLoadPic.src = itemSummary['pic'];
    };
    
    this.leftPartElement = function() {
        //<div class="divItemLeft">
        //    <img class="itemImage pointer" src="${pic}"/>
        //    <div class="itemLinksBubble">
        //        <div class="itemLinksCount">${totalLinks}</div>
        //    </div>
        //</div>
        var left = jQuery('<div/>')
            .addClass('divItemLeft')
            .append(this.picElement(this.itemSummary['number']))
            .append(this.bubbleElement(this.itemSummary['totalLinks']));
            
        if(typeof this.itemSummary['gallery'] != 'undefined') {
            $(left).click(itemSummary['gallery'], displayGallery);
        }
        
        return left;
    };
    
    this.picElement = function(itemNumber) {
        // <img id=... class="itemImage pointer"/>
        return jQuery('<img/>')
            .attr('id', 'picItem' + itemNumber)
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
};

function ItemManager() {
    this.itemNumberRootUrl = itemNumberRootUrl;
    this.totalItems = totalItems;
    this.itemsLoaded = {};
    
    this.loadItem = function(number) {
        if(number == null) {
            number = this.getNumberToLoad();
        }
        
        if(number < 0 || number >= this.totalItems) {
            return;
        }

        if(number in this.itemsLoaded) {
            return;
        }
        
        this.itemsLoaded[number] = null;
        $.getJSON(this.itemNumberRootUrl + number, function(itemSummary) {
            contentManager.addItem(new Item(itemSummary));
        });
    };
    
    this.getNumberToLoad = function() {
        // Todo: search missing in keys
        return Object.keys(this.itemsLoaded).length;
    };
    
    this.getTotalLoaded = function() {
        return Object.keys(this.itemsLoaded).length;
    }
    
    this.addItem = function(item) {
        item.display();
        this.itemsLoaded[item.itemSummary['number']] = $(item.itemElement);
    };
};
