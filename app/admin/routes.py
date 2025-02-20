from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.admin import bp
from app.models import Article
from api.extensions import db

@bp.route('/dashboard')
@login_required
def dashboard():
    articles = Article.query.order_by(Article.created_at.desc()).all()
    return render_template('admin/dashboard.html', articles=articles)

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_article():
    if request.method == 'POST':
        article = Article(
            title=request.form['title'],
            content=request.form['content'],  # HTML 컨텐츠가 그대로 저장됨
            summary=request.form['summary'],
            source_link=request.form.get('source_link'),
            author=current_user.username
        )
        db.session.add(article)
        db.session.commit()
        flash('기사가 성공적으로 등록되었습니다.', 'success')
        return redirect(url_for('admin.dashboard'))
    return render_template('admin/create_article.html')

@bp.route('/article/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_article(id):
    article = Article.query.get_or_404(id)
    if request.method == 'POST':
        article.title = request.form['title']
        article.content = request.form['content']
        article.summary = request.form['summary']
        db.session.commit()
        flash('Article updated successfully!')
        return redirect(url_for('admin.dashboard'))
    return render_template('admin/edit_article.html', article=article) 