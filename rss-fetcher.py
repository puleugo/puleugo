import feedparser, time, ssl;


# 게시글 읽어오기
ssl._create_default_https_context = ssl._create_unverified_context;
url = "https://puleugo.tistory.com/rss";
raw = feedparser.parse(url)['entries'];


# 게시글 필터링
post = [];

ignoreCategories = {'도서 리뷰'};
for idx, post in enumerate(raw):
    isIgnored = False;
    for tag in post['tags']:
        if tag['term'] in ignoreCategories:
            isIgnored = True;
        break

    if not isIgnored:
        posts.append(post);

# 게시글 슬라이싱
postLimit = 6
posts[:postLimit];

# 게시글 마크다운 생성
postsMarkdown = f"""
## Recent Posts
"""

for post in posts:
    rawPublishedAt = post['published_parsed'];
    formatedPublishedAt = time.strftime('%Y.%M.%D', rawPublishedAt);
    title = post['title'];

    postsMarkdown += f'- {title} {formatedPublishedAt} <br/>\n';

# 최종 마크다운 생성
readStream = open('TEMPLATE.md', mode='r',encoding='utf-8');
templateMarkdown = readStream.read();
readStream.close();

resultMarkdown = templateMarkdown + postsMarkdown;

# README.md에 작성

fileStream = open('README.md', mode='w', encoding='utf-8');
fileStream.write(resultMarkdown)
fileStream.close();
