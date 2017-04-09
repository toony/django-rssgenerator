function ContentManager() {
    this.itemManager = new ItemManager();
    
    this.totalItemsVisible = function() {
        return this.rows() * this.columns();
    };

	this.columns = function() {
		var columns = Math.floor($('#content').get(0).scrollWidth/310);
		if(columns == 0) {
			columns = 1;
		}
        
        return columns;
    };

    this.rows = function() {
		var rows = Math.floor($('#content').height()/110);
		if(rows == 0) {
			rows = 1;
		}else {
			rows++;
		}
        
        return rows;
	};
    
    this.fill = function(numberOfItems) {
        if(numberOfItems === undefined) {
            numberOfItems = this.totalItemsVisible();
        }

        for(var i=0; i < numberOfItems; i++) {
            this.itemManager.loadItem();
        }
    };
    
    this.resized = function() {
        if(this.itemManager.getTotalLoaded() < this.totalItemsVisible()) {
            this.fill(this.totalItemsVisible() - this.itemManager.getTotalLoaded());
            return
        }
        
        var lastRowItemsCount = this.itemManager.getTotalLoaded() % this.columns();
        if(lastRowItemsCount != 0) {
            this.fill(this.columns() - lastRowItemsCount);
        }
    };
    
    this.addRow = function(numberOfRow) {
        numberOfItems = this.columns();
        
        if(numberOfRow !== undefined) {
            numberOfItems = numberOfRow * numberOfItems;
        }
        
        for(var i=0; i<numberOfItems; i++) {
            this.itemManager.loadItem();
        }
    };
    
    this.addItem = function(item) {
	this.itemManager.addItem(item);
    };
};

var contentManager = new ContentManager();
