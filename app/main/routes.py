from flask import render_template, request
from app.main import bp
from app.models import Article

@bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    articles = Article.query.order_by(Article.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False)
    return render_template('main/index.html', articles=articles)

@bp.route('/article/<int:id>')
def article(id):
    article = Article.query.get_or_404(id)
    return render_template('main/article.html', article=article) 