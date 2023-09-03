var singleLink = document.querySelector("a[href='single.html']");
  	singleLink.href += "?" + username;

  	var categoryLink = document.querySelector("a[href='category.html']");
  	categoryLink.href += "?" + username;

  	var searchLink = document.querySelector("a[href='search.html']");
  	searchLink.href += "?" + username;

  	var archiveLink = document.querySelector("a[href='archive.html']");
  	archiveLink.href += "?" + username;

  	var genericLink = document.querySelector("a[href='Write.html']");
  	genericLink.href += "?" + username;

  	var elementsLink = document.querySelector("a[href='elements.html']");
  	elementsLink.href += "?" + username;

	  function redirectToIndex(event) {
		window.location.href = "index.html?" + encodeURIComponent(username);
	  }



