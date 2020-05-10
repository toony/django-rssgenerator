<script type="text/javascript">
window.addEventListener('load', onLoad());

function onLoad() {
    $.getJSON("{% url 'rss:searchItem' rss.id %}?q=", function(itemsIdList) {
        galleryManager = new GalleryManager("{% url 'rss:rssSummary' rss.id %}");
        galleryManager.init("{{ rss.title }}", itemsIdList);
        galleryManager.fill()
    });
}

function getGalleryManagerItemsIdList() {
    return galleryManager.itemsIdList;
}

function search(e) {
    if(e.keyCode === 13){
        var query = document.getElementById("itemSearch").value;
        $.getJSON("{% url 'rss:searchItem' rss.id %}?q=" + query, function(itemsIdList) {
            galleryManager.init("{{ rss.title }}", itemsIdList);
            galleryManager.fill()
        });

        document.getElementById("tag-menu").checked = false;
    }
}
</script>
