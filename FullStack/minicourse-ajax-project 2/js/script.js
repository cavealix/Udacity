
function loadData() {

    var $body = $('body');
    var $wikiElem = $('#wikipedia-links');
    var $nytHeaderElem = $('#nytimes-header');
    var $nytElem = $('#nytimes-articles');
    var $greeting = $('#greeting');

    // clear out old data before new request
    $wikiElem.text("");
    $nytElem.text("");

    var streetStr = $('#street').val();
    var cityStr = $('#city').val();
    var address = streetStr + ', ' + cityStr;

    $greeting.text('So, you want to live at ' + address + '?');


    // load streetview
    var streetviewUrl = 'http://maps.googleapis.com/maps/api/streetview?size=600x400&location=' + address + '';
    $body.append('<img class="bgimg" src="' + streetviewUrl + '">');


    // load nytimes
    var url = "https://api.nytimes.com/svc/search/v2/articlesearch.json";
    url += '?' + $.param({
      'api-key': "46a7c370f29e4e6094fd492664e70a48",
      'q': cityStr,
      'sort': "newest"
    });

    $.getJSON( url, function( data ) {

        $nytHeaderElem.text('New York Times Articles About '+cityStr)
        articles = data.response.docs;
        for (var i=0; i < articles.length; i++){
            var article = articles[i];
            $nytElem.append('<li class="article">'+
                '<a href="'+article.web_url+'">'+article.headline.main+
                '</a>'+
                '<p>'+article.snippet+'</p>'+'</li>');
        };
    }).error(function(e){
        $nytHeaderElem.text('The New York Times could not be loaded')
    });


    //wiki jsonp error work around
    var wikiRequestTimeout = setTimeout(function(){
        $wikiElem.text('Failed to get Wiki resources');
    }, 8000);

    //load wikipedia
    var wikiUrl = "https://en.fdawikipedia.org/w/api.php?action=opensearch&search="+cityStr+"&format=json&callback=wikiCallback";
    $.ajax( {
        url: wikiUrl,
        dataType: 'jsonp',
        success: function(response){
            var articleList=response[1];

            for (var i=0; i < articleList.length; i++){
                articleStr = articleList[i];
                var url = 'http://en.wikipedia.org/wiki/'+articleStr;
                $wikiElem.append('<li><a href="'+url+'">'+articleStr+'</a></li>');
            };

            clearTimeout(wikiRequestTimeout);
        }
    });


    return false;
};


$('#form-container').submit(loadData);
