$(document).ready(function() {
  $.get("http://localhost:8123/article_list/?format=json", function(data, status) {
    var articles = data.data;
    var articleHTML = "";
    
    for (var i = 0; i < articles.length; i++) {
      articleHTML += "<a href='/article/" + articles[i].id + "/'>" + articles[i].title + "</a>";
      articleHTML += "<p>Author: " + articles[i].author + " | Like Count: " + articles[i].like_count + "</p>";
      articleHTML += "<hr style='border-top: 1px solid #444444;'>";
    }
    $(".sample-text").html(articleHTML);
  });
});
