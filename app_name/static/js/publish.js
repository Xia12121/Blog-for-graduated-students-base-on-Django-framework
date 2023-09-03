function publishBlog() {
    const title = document.getElementById("title-input").value;
    const content = encodeURIComponent(document.getElementById("content-input").value);
    const author_username = username; // 替换为您的用户名
    alert(username)
    const url = `http://software.engineering.project.testing.cpolar.top/create_article/?author_username=${author_username}&title=${title}&content=${content}`;
    fetch(url)
      .then(response => {
          if (!response.ok) {
              throw new Error("Failed to publish blog.");
          }
          alert("Blog published successfully.");
          window.location.href = "index.html?"+username;
      })
      .catch(error => alert(error.message));
}