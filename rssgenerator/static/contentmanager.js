function ContentManager(rssRootUrl, itemsIdList) {
    this.rssRootUrl = rssRootUrl;
    this.itemsIdList = itemsIdList;
    this.loadOffset = 20;
    this.loadingItemscount = 0;
    
    this.curentContentHeight = 0;
    
    this.itemsLoaded = {};
    
    this.loadItem = function() {
        itemId = this.getIdToLoad();
        
        if( itemId == null ) {
            return null;
        }

        $.getJSON(this.getItemSummaryUrl(itemId), function(itemSummary) {
            contentManager.addItem(new Item(itemSummary));
        });
        
        return itemId;
    };
    
    this.getIdToLoad = function() {
        for( i in this.itemsIdList ) {
            itemId = this.itemsIdList[i];
            
            if( !(itemId in this.itemsLoaded) ) {
                return itemId;
            }
        }
        
        return null;
    };
    
    this.getItemSummaryUrl = function(itemId) {
        return this.rssRootUrl + itemId + "/summary";
    }
    
    this.fill = function() {
        this.curentContentHeight = $('#content')[0].offsetHeight;
        
        for(var i=0; i < this.loadOffset; i++) {
            itemId = this.loadItem();
            if(itemId === null) {
                break;
            }
            
            this.loadingItemscount++;
            this.itemsLoaded[itemId] = null;
        }
    };
    
    this.itemVisible = function(item) {
        this.loadingItemscount--;
        
        if(this.loadingItemscount == 0) {
            var galleryHeight = $('#gallery')[0].offsetHeight;
            var contentHeight = $('#content')[0].offsetHeight;
            
            if(contentHeight == this.curentContentHeight
             || (contentHeight - galleryHeight) < 250) {
                this.fill();
            }
        }
    };
    
    this.addItem = function(item) {
        this.itemsLoaded[item.itemSummary['id']] = item;
        $('#content').append(item.itemElement);
        
        var preLoadPic = new Image();
        preLoadPic.onload = function() {
            // Add src to picItem and display item
            $('#picItem' + item.itemSummary['id']).attr('src', this.src);
            //itemElement.css("display", "inline");
            $('#item' + item.itemSummary['id']).delay(500).show().animate({opacity:1},3000);
            contentManager.itemVisible(item);
        };
        preLoadPic.src = item.itemSummary['pic'];
    };
};

var contentManager = undefined;
