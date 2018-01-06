function showBlogStatus(status) {
    const statusElement = document.querySelector('.js-status');
    if (status === 'SUCCESS') {
        statusElement.classList.remove('fnt--orange')
        statusElement.classList.add('fnt--green')
    }
    if (status === 'FAILURE') {
        statusElement.classList.remove('fnt--orange')
        statusElement.classList.add('fnt--red')
    }
    statusElement.style.display = 'block';
    statusElement.textContent = status;
}

function showDownload(url) {
    document.querySelector('.js-status').style.display = 'none';
    const downloadElement = document.querySelector('.js-download');
    downloadElement.setAttribute('href', url);
    downloadElement.style.display = 'block';
}

function startJob() {
    const formData = new FormData(document.querySelector('.js-form'));
    window.fetch('/convert', { method: 'POST', body: formData }).then((response) => {
        response.text().then((data) => {
            getBlogStatus(data);
        });
    });
}

function getBlogStatus(blog_id) {
    window.fetch(`/converted/${blog_id}/status`).then((response) => {
        response.json().then((data) => {
            showBlogStatus(data.status);
            if (data.status === 'SUCCESS') {
                showDownload(data.download);
            } else {
                window.setTimeout(() => getBlogStatus(blog_id), 2000);
            }
        });
    });
}

document.addEventListener('DOMContentLoaded', () => {
    document.querySelector('.js-trigger').addEventListener('click', startJob);
});