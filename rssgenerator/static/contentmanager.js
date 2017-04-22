function ContentManager(rssRootUrl, itemsIdList) {
    this.rssRootUrl = rssRootUrl;
    this.itemsIdList = itemsIdList;
    this.loadOffset = 20;
    
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
        for(var i=0; i < this.loadOffset; i++) {
            itemId = this.loadItem();
            if(itemId === null) {
                break;
            }
            
            this.itemsLoaded[itemId] = null;
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
            console.log($('#content')[0].offsetHeight);
        };
        preLoadPic.src = item.itemSummary['pic'];
    };
};

var contentManager = undefined;
