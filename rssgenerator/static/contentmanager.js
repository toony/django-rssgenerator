function ContentManager(rssRootUrl, itemsIdList) {
    this.rssRootUrl = rssRootUrl;
    this.itemsIdList = itemsIdList;
    this.loadOffset = 20;
    
    this.itemsLoaded = {};
    
    this.loadItem = function() {
        itemId = this.getIdToLoad();
        
        if( itemId == null ) {
            return;
        }

        $.getJSON(this.getItemSummaryUrl(itemId), function(itemSummary) {
            console.log(itemSummary);
            contentManager.addItem(new Item(itemSummary));
        });
    };
    
    this.getIdToLoad = function() {
        for( i in this.itemsIdList ) {
            itemId = this.itemsIdList[i];
            
            if( !(itemId in this.itemsLoaded) ) {
                this.itemsLoaded[itemId] = null;
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
            this.loadItem();
        }
    };
    
    this.addRow = function(numberOfRow) {
        numberOfItems = numberOfRow * this.loadOffset;
        
        for(var i=0; i<numberOfItems; i++) {
            this.itemManager.loadItem();
        }
    };
    
    this.addItem = function(item) {
        this.itemsLoaded[item.itemSummary['id']] = item;
        $('#content').append(item.itemElement);
    };
};

var contentManager = undefined;
