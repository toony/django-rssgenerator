function GalleryManager(rssRootUrl) {
    this.rssRootUrl = rssRootUrl;
    this.loadOffset = 20;

    $('#gallery').append(jQuery('<div/>')
        .attr('id', 'progress')
        .addClass('divProgress'));

    $('#progress').append(jQuery('<div/>')
        .attr('id', 'progressBar')
        .addClass('divProgressBar'));

    $('#gallery').append(jQuery('<div/>')
        .attr('id', 'contentFix')
        .addClass('divContentFix'));

    $('#contentFix').append(jQuery('<div/>')
        .attr('id', 'content')
        .addClass('divContent'));

    $('#contentFix').on('scroll', function() {
        if($(this).scrollTop() + $(this).innerHeight() + 300 >= $(this)[0].scrollHeight) {
            galleryManager.fill();
        }
    });

    this.init = function(itemsIdList) {
        $('#gallery #content').empty();

        this.itemsIdList = itemsIdList;
        this.loadingItemsCount = 0;
        this.itemsDisplayed = 0;

        this.curentContentHeight = 0;

        this.itemsLoaded = {};
    }

    this.loadItem = function() {
        itemId = this.getIdToLoad();

        if( itemId == null ) {
            return null;
        }

        $.getJSON(this.getItemSummaryUrl(itemId), function(itemSummary) {
            galleryManager.addItem(new Item(itemSummary));
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
        if(this.loadingItemsCount != 0) {
            // Currently loading, do nothing
            return;
        }

        this.curentContentHeight = $('#gallery #content')[0].offsetHeight;

        for(var i=0; i < this.loadOffset; i++) {
            itemId = this.loadItem();
            if(itemId === null) {
                break;
            }

            this.loadingItemsCount++;
            this.itemsLoaded[itemId] = null;
        }
    };

    this.refreshProgressBar = function() {
        var progress = this.itemsDisplayed * 100 / this.itemsIdList.length;
        $('#gallery #progressBar').width(progress + '%');
    }

    this.itemVisible = function(item) {
        this.itemsDisplayed++;
        this.refreshProgressBar();

        this.loadingItemsCount--;

        if(this.loadingItemsCount == 0) {
            var galleryHeight = $('#gallery')[0].offsetHeight;
            var contentHeight = $('#gallery #content')[0].offsetHeight;

            if(contentHeight == this.curentContentHeight
             || (contentHeight - galleryHeight) < 250) {
                this.fill();
            }
        }
    };

    this.addItem = function(item) {
        this.itemsLoaded[item.itemSummary['id']] = item;
        $('#gallery #content').append(item.itemElement);

        var preLoadPic = new Image();
        preLoadPic.onload = function() {
            // Add src to picItem and display item
            $('#picItem' + item.itemSummary['id']).attr('src', this.src);
            //itemElement.css("display", "inline");
            $('#item' + item.itemSummary['id']).delay(500).show().animate({opacity:1},3000);
            galleryManager.itemVisible(item);
        };
        preLoadPic.src = item.itemSummary['pic'];
    };
};

var galleryManager = undefined;

var resized;
$(window).on('resize', function() {
    clearTimeout(resized);
    resized = setTimeout(function() { galleryManager.fill(); }, 1000);
});
