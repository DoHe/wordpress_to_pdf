import re
from io import BytesIO

import weasyprint
import xmltodict
from PIL import Image

LOCAL_PROTOCOL = 'local://'

BLACKLIST = [
    'Über uns',
    'Neuer Blog',
    'Reisen',
    'hinflug',
    'Der Plan',
    'Extra Platz im Flieger 1'
]


def scale_image(img, image_size):
    img.thumbnail((image_size, image_size), Image.ANTIALIAS)
    image_buffer = BytesIO()
    img.save(image_buffer, "JPEG")
    image_buffer.seek(0)
    return image_buffer


def image_scaling_fetcher(url, image_size):
    if url.startswith(LOCAL_PROTOCOL):
        with open(url.replace(LOCAL_PROTOCOL, ''), 'rb') as img_file:
            img = Image.open(img_file)
            return {
                'mime_type': 'image/jpeg',
                'file_obj': scale_image(img, image_size)
            }

    fetched = weasyprint.default_url_fetcher(url)
    if fetched.get('mime_type').startswith('image'):
        img = Image.open(fetched['file_obj'])
        fetched['file_obj'] = scale_image(img, image_size)
    return fetched


def should_skip(post, blacklist):
    title = post.get('title')
    if not title or title in BLACKLIST + blacklist:
        return True
    title = title.lower()
    is_image = any(title.endswith(suf) for suf in ['jpg', 'mp4'])
    return not title or any(title.startswith(pre) for pre in ['wp', 'p1', 'cropped', 'dsc', 'img', 'icon']) or is_image


def generate_header(headline_color, font, image_size):
    return """
        <html>
        <head>
        <style>
        * {{
            font-family: {};
        }}
        h1 {{
            color: {};
        }}
        img {{
            display: block;
            max-width: {}px;
            height: auto;
        }}
        .caption {{
            font-size: small;
            font-style: italic
        }}
        </style>
        </head>
        <body>
    """.format(font, headline_color, image_size)


def wordpress_to_pdf(xml_path, pdf_path, headline_color, font, image_size, blacklist):
    with open(xml_path, 'rb') as blog_file:
        converted_buffer = buffer_to_buffer(blog_file, headline_color, font, image_size, blacklist)
    with open(pdf_path, 'wb') as pdf_file:
        pdf_file.write(converted_buffer.read())


def buffer_to_buffer(blog_buffer, headline_color, font, image_size, blacklist):
    blog = xmltodict.parse(blog_buffer)
    posts = [post for post in blog['rss']['channel']['item'] if not should_skip(post, blacklist)]
    posts.sort(key=lambda post: post['wp:post_date'])

    result = generate_header(headline_color, font, image_size)
    for idx, post in enumerate(posts):
        title = post['title']
        print('{}. {}'.format(idx + 1, title))
        result += "<br>\n<h1>{}</h1>".format(title)
        content = post.get('content:encoded')
        if not content:
            print("no content")
            continue
        result += content

    result += "\n</body>"
    result = re.sub(r'\[caption.*?]', '', result)
    result = re.sub(r'(/a)?>([\w\s(),\-"\.\?!:\']*?)\[/caption\]', r'\1><span class="caption">\2</span></br></br>',
                    result)
    result = re.sub(r'\[wpvideo ([\w\d]*?)\]', r'<img src="local://\1.jpg"></img>', result)
    with open('blog.html', 'w') as html_file:
        html_file.write(result)
    print('Rendering...')
    return weasyprint.HTML(string=result, url_fetcher=lambda url: image_scaling_fetcher(url, image_size)).write_pdf()


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description="Turns an exported wordpress xml file into a pdf")
    parser.add_argument('blog', type=str, help="The exported wordpress xml")
    parser.add_argument('pdf', type=str, help="The path to write the pdf to")
    parser.add_argument('-hc', '--headline-color', type=str, default='#00CED1',
                        help="The color for the headlines (HTML notation)")
    parser.add_argument('-f', '--font', type=str, default='"Georgia", serif',
                        help="The font to use for the whole document (HTML notation)")
    parser.add_argument('-i', '--image-size', type=int, default=450,
                        help="The maximum size of the largest side (in pixel)")
    parser.add_argument('-b', '--blacklist', type=str, default=[], nargs='*',
                        help="Titles of blog posts to be excluded")
    args = parser.parse_args()
    wordpress_to_pdf(args.blog, args.pdf, args.headline_color, args.font, args.image_size, args.blacklist)
