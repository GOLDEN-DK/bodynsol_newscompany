# 검색엔진·AI 수집용 경로(robots, sitemap, RSS, llms.txt)와 대표 주소 처리.
import html
import re
from datetime import timezone
from email.utils import format_datetime
from urllib.parse import quote, urlsplit

from flask import current_app, make_response, redirect, render_template, request, send_from_directory

from app.main import bp
from app.models import Article, Category

BLOCK_TAG_RE = re.compile(
    r'</?(?:p|br|div|li|ul|ol|h[1-6]|blockquote|figure|figcaption|table|tr|td|th|section|article)\b[^>]*>',
    re.IGNORECASE
)
TAG_RE = re.compile(r'<[^>]+>')
LOCAL_HOSTS = ('localhost', '127.0.0.1')
PATH_SAFE = "/!$&'()*+,;=:@-._~"
RSS_ITEM_LIMIT = 30
LLMS_ITEM_LIMIT = 20


def site_url():
    return current_app.config['SITE_URL'].rstrip('/')


def newest_first():
    # PostgreSQL은 DESC에서 NULL을 맨 앞에 두므로 발행일 없는 기사를 맨 뒤로 보낸다.
    return Article.created_at.desc().nulls_last()


@bp.before_app_request
def redirect_to_canonical_host():
    # www·Railway 기본 주소로 들어온 요청을 대표 주소로 영구 이동시킨다.
    # 프록시가 Host를 내부 주소로 바꿔도 반복 이동하지 않도록 X-Forwarded-Host를 먼저 본다.
    canonical = urlsplit(site_url())
    forwarded = request.headers.get('X-Forwarded-Host', '').split(',')[0].strip()
    host = (forwarded or request.host).split(':')[0].lower()
    if host == canonical.hostname or host in LOCAL_HOSTS:
        return None
    # 디코딩된 path를 다시 인코딩해 %3F 같은 예약문자가 쿼리로 바뀌지 않게 한다.
    target = f"{canonical.scheme}://{canonical.netloc}{quote(request.path, safe=PATH_SAFE)}"
    if request.query_string:
        target += '?' + request.query_string.decode('latin-1')
    return redirect(target, code=301 if request.method in ('GET', 'HEAD') else 308)


@bp.app_context_processor
def inject_seo():
    url = site_url() + request.path
    page = request.args.get('page', type=int)
    if page and page > 1:
        url += f'?page={page}'
    return {'canonical_url': url, 'site_url': site_url(), 'article_excerpt': article_excerpt}


def article_excerpt(article, length):
    # 문단이 붙지 않도록 블록 태그는 공백으로, 인라인 태그는 제거하고 HTML 엔티티를 푼다.
    text = BLOCK_TAG_RE.sub(' ', article.summary or article.content or '')
    text = html.unescape(TAG_RE.sub('', text))
    text = ' '.join(text.split())
    return text if len(text) <= length else text[:length].rstrip() + '…'


def text_response(body, mimetype):
    response = make_response(body)
    response.mimetype = mimetype
    return response


@bp.route('/robots.txt')
def robots_txt():
    return text_response(render_template('seo/robots.txt'), 'text/plain')


@bp.route('/sitemap.xml')
def sitemap_xml():
    articles = Article.query.with_entities(Article.id, Article.created_at)\
        .order_by(newest_first()).all()
    categories = Category.query.filter(Category.articles.any()).order_by(Category.id).all()
    latest = next((a.created_at for a in articles if a.created_at), None)
    return text_response(
        render_template('seo/sitemap.xml', articles=articles, categories=categories, latest=latest),
        'application/xml'
    )


@bp.route('/rss.xml')
def rss_xml():
    articles = Article.query.order_by(newest_first()).limit(RSS_ITEM_LIMIT).all()
    # 발행일이 없는 기사는 pubDate를 생략한다.
    items = [{
        'article': article,
        'description': article_excerpt(article, 300),
        'pub_date': format_datetime(article.created_at.replace(tzinfo=timezone.utc))
        if article.created_at else None,
    } for article in articles]
    last_build = next((item['pub_date'] for item in items if item['pub_date']), None)
    return text_response(
        render_template('seo/rss.xml', items=items, last_build=last_build),
        'application/rss+xml'
    )


@bp.route('/llms.txt')
def llms_txt():
    articles = Article.query.order_by(newest_first()).limit(LLMS_ITEM_LIMIT).all()
    items = [{'article': article, 'excerpt': article_excerpt(article, 160)} for article in articles]
    return text_response(render_template('seo/llms.txt', items=items), 'text/plain')


@bp.route('/favicon.ico')
def favicon():
    return send_from_directory(current_app.static_folder, 'favicon.ico',
                               mimetype='image/vnd.microsoft.icon')
