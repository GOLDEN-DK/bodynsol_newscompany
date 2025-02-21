from flask import render_template, request
from app.main import bp
from app.models import Article, Category
from extensions import db
import re

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

@bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    articles = Article.query.order_by(Article.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False
    )
    
    # 각 기사의 내용과 요약에서 HTML 태그 제거
    for article in articles.items:
        if article.summary:
            article.summary = strip_html_tags(article.summary)
        article.content = strip_html_tags(article.content)
    
    categories = Category.query.all()
    return render_template('main/index.html', articles=articles, categories=categories)

@bp.route('/article/<int:id>')
def article(id):
    article = Article.query.get_or_404(id)
    categories = Category.query.all()
    return render_template('main/article.html', article=article, categories=categories)

@bp.route('/category/<slug>')
def category(slug):
    category = Category.query.filter_by(slug=slug).first_or_404()
    page = request.args.get('page', 1, type=int)
    articles = Article.query.filter_by(category_id=category.id)\
        .order_by(Article.created_at.desc())\
        .paginate(page=page, per_page=10)
    
    # 각 기사의 내용과 요약에서 HTML 태그 제거
    for article in articles.items:
        if article.summary:
            article.summary = strip_html_tags(article.summary)
        article.content = strip_html_tags(article.content)
    
    categories = Category.query.all()
    return render_template('main/category.html', category=category, articles=articles, categories=categories) 