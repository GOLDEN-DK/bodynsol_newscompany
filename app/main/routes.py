from datetime import datetime, timedelta
from flask import render_template, request
from app.main import bp
from app.models import Article, Category
from extensions import db
import re

# 상단 메뉴에는 이 기간 안에 글이 있는 카테고리만 표시한다.
NAV_CATEGORY_RECENT_DAYS = 365

def strip_html_tags(text):
    if not text:
        return ""
    # HTML 태그 제거
    clean = re.compile('<.*?>')
    # 여러 줄 바꿈을 하나로
    text = re.sub(r'\n+', '\n', text)
    # HTML 태그 제거
    text = re.sub(clean, '', text)
    # 앞뒤 공백 제거
    return text.strip()

def strip_article_html(articles):
    # 목록에 표시할 기사의 내용과 요약에서 HTML 태그 제거
    for article in articles:
        if article.summary:
            article.summary = strip_html_tags(article.summary)
        article.content = strip_html_tags(article.content)

@bp.app_context_processor
def inject_nav_categories():
    cutoff = datetime.utcnow() - timedelta(days=NAV_CATEGORY_RECENT_DAYS)
    nav_categories = Category.query.filter(
        Category.articles.any(Article.created_at >= cutoff)
    ).order_by(Category.id).all()
    return {'nav_categories': nav_categories}

@bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)

    # 가장 최근 메인 기사 1건을 대표 기사로 쓰고, 목록에서는 제외한다.
    hero = Article.query.filter_by(is_main=True)\
        .order_by(Article.created_at.desc()).first()
    list_query = Article.query
    if hero:
        list_query = list_query.filter(Article.id != hero.id)
    articles = list_query.order_by(Article.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False
    )

    strip_article_html(articles.items + ([hero] if hero else []))
    return render_template(
        'main/index.html',
        hero=hero if page == 1 else None,
        articles=articles
    )

@bp.route('/article/<int:id>')
def article(id):
    article = Article.query.get_or_404(id)

    # SQL expression으로 증가시켜 동시 요청에서도 조회수가 유실되지 않게 한다.
    Article.query.filter_by(id=id).update(
        {Article.view_count: db.func.coalesce(Article.view_count, 0) + 1},
        synchronize_session=False
    )
    db.session.commit()
    db.session.refresh(article)

    return render_template('main/article.html', article=article)

@bp.route('/category/<slug>')
def category(slug):
    category = Category.query.filter_by(slug=slug).first_or_404()
    page = request.args.get('page', 1, type=int)
    articles = Article.query.filter_by(category_id=category.id)\
        .order_by(Article.created_at.desc())\
        .paginate(page=page, per_page=10)

    strip_article_html(articles.items)
    return render_template('main/category.html', category=category, articles=articles)
