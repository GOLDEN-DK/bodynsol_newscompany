from flask import render_template, request
from app.main import bp
from app.models import Article, Category
from extensions import db

@bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    articles = Article.query.order_by(Article.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False
    )
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
    categories = Category.query.all()
    return render_template('main/category.html', category=category, articles=articles, categories=categories) 