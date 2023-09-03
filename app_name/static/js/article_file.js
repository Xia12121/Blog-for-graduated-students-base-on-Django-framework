// 获取文章id
const urlParams = new URLSearchParams(window.location.search);
const params = urlParams.toString().split('%3F'); // 将 URL 参数转换为字符串并拆分成数组
const id = params[0].replace(/^id=/, ''); // 获取第一个参数作为文章 ID

// 使用fetch获取文章API数据
fetch(`http://software.engineering.project.testing.cpolar.top/articles/${id}/?format=json`)
  .then(response => response.json())
  .then(data => {
    // 获取文章标题、内容、作者、点赞数、创建时间
    const title = data.title;
    const content = data.content;
    const author = data.author;
    const likes = data.likes.length;
    const created_at = new Date(data.created_at).toLocaleString();

    // 输出文章标题
    const titleElem = document.querySelector('.about-title');
    titleElem.textContent = title;

    const contentElem = document.querySelector('.img-text');
    contentElem.innerHTML = `<p style="color: black;">${content.replace(/\n/g, '<br/>')}</p>`;

    // 输出文章作者、点赞数、创建时间
    const infoElem = document.querySelector('.article-info');
    const authorElem = document.createElement('div');
    authorElem.textContent = `Author: ${author}\r\n`;
    infoElem.appendChild(authorElem);

    const likesElem = document.createElement('div');
    likesElem.textContent = `Likes: ${likes}\r\n`;
    infoElem.appendChild(likesElem);

    const createdAtElem = document.createElement('div');
    createdAtElem.textContent = `Created at: ${created_at}\r\n`;
    infoElem.appendChild(createdAtElem);
  })
  .catch(error => console.error(error));

// 使用fetch获取评论API数据
fetch(`http://software.engineering.project.testing.cpolar.top/articles/${id}/comments/`)
  .then(response => response.json())
  .then(data => {
    // 获取评论列表
    const comments = data;

    // 输出评论
    const commentsElem = document.querySelector('#comments');

if (comments.length > 0) {
  comments.forEach(comment => {
    const commentElem = document.createElement('div');
    commentElem.classList.add('comment');
    commentElem.innerHTML = `
      <div class="comment__user">${comment.user}</div>
      <div class="comment__content">${comment.content.replace(/\n/g, '<br/>')}</div>
      <div class="comment__date">${new Date(comment.created_at).toLocaleString()}</div>
    `;
    commentsElem.appendChild(commentElem);
  });
} else {
  commentsElem.textContent = 'No comments yet.';
}

  })
  .catch(error => console.error(error));

  // 获取文章id

// 获取发布按钮
const publishBtn = document.querySelector('.button');

// 点击发布按钮时，提交评论并刷新页面
publishBtn.addEventListener('click', () => {
  // 获取评论内容
  const content = encodeURIComponent(document.querySelector('#content-input').value);


  // 使用fetch提交评论
  fetch(`http://software.engineering.project.testing.cpolar.top/articles/${id}/comments/create/?username=Xia_Linhan&content=${content}`)
    .then(response => response.json())
    .then(data => {
      // 刷新页面
      window.location.reload();
    })
    .catch(error => console.error(error));
});

