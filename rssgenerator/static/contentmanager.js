function ContentManager() {
    this.loadOffset = 20;
    this.itemManager = null;
    
    this.fill = function() {
        for(var i=0; i < this.loadOffset; i++) {
            this.itemManager.loadItem();
        }
    };
    
    this.addRow = function(numberOfRow) {
        numberOfItems = numberOfRow * this.loadOffset;
        
        for(var i=0; i<numberOfItems; i++) {
            this.itemManager.loadItem();
        }
    };
    
    this.addItem = function(item) {
        this.itemManager.addItem(item);
    };
    
    this.initItemManager = function(itemsIdList) {
        this.itemManager = new ItemManager(itemsIdList);
    };
};

var contentManager = new ContentManager();
