import feedparser, time, ssl;

# 게시글 읽어오기
ssl._create_default_https_context = ssl._create_unverified_context;
url = "https://ko.puleugo.dev/rss";
raw = feedparser.parse(url)['entries'];
# print(raw)

# 게시글 필터링
posts = [];

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
    tagsList = list(map(lambda data: data['term'], post['tags']))[1:]; # 첫 term은 카테고리, 이후부터는 게시글 태그
    tagsList = list(map(lambda words: ' '.join(word.capitalize() for word in words.split()), tagsList)); # 모든 문자의 첫 알파벳을 대문자로 변환
    tags = ', '.join(tagsList);
    formatedPublishedAt = time.strftime('%Y.%m.%d', rawPublishedAt);
    title = post['title'];
    url = post['links'][0]['href'];

    postsMarkdown += f'- [{title}]({url}) - {formatedPublishedAt} ';
    if len(tags) > 0:
        postsMarkdown += f'<br>\t{tags}';
    postsMarkdown += '<br/>\n';

# 최종 마크다운 생성
readStream = open('TEMPLATE.md', mode='r',encoding='utf-8');
templateMarkdown = readStream.read();
readStream.close();

resultMarkdown = templateMarkdown + postsMarkdown;

# README.md에 작성
fileStream = open('README.md', mode='w', encoding='utf-8');
fileStream.write(resultMarkdown)
fileStream.close();
