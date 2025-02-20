from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.admin import bp
from app.models import Article, Category
from extensions import db

@bp.route('/dashboard')
@login_required
def dashboard():
    page = request.args.get('page', 1, type=int)
    per_page = 10  # 한 페이지당 표시할 기사 수
    
    # 페이지네이션 적용 및 필요한 컬럼만 선택
    articles = Article.query.with_entities(
        Article.id,
        Article.title,
        Article.author,
        Article.created_at
    ).order_by(
        Article.created_at.desc()
    ).paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )
    
    return render_template('admin/dashboard.html', articles=articles)

@bp.route('/article/create', methods=['GET', 'POST'])
@login_required
def create_article():
    if request.method == 'POST':
        article = Article(
            title=request.form['title'],
            content=request.form['content'],
            summary=request.form['summary'],
            source_link=request.form.get('source_link'),
            author=current_user.username,
            category_id=request.form['category_id'],
            is_main=bool(request.form.get('is_main')),  # 메인 기사 여부
            main_image=request.form.get('main_image')   # 메인 이미지 URL
        )
        db.session.add(article)
        db.session.commit()
        flash('기사가 성공적으로 등록되었습니다.', 'success')
        return redirect(url_for('admin.dashboard'))
    
    categories = Category.query.all()
    return render_template('admin/create_article.html', categories=categories)

@bp.route('/article/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_article(id):
    article = Article.query.get_or_404(id)
    if request.method == 'POST':
        article.title = request.form['title']
        article.content = request.form['content']
        article.summary = request.form['summary']
        article.source_link = request.form.get('source_link')
        db.session.commit()
        flash('기사가 성공적으로 수정되었습니다.', 'success')
        return redirect(url_for('admin.dashboard'))
    return render_template('admin/edit_article.html', article=article)

@bp.route('/article/<int:id>/delete', methods=['POST'])
@login_required
def delete_article(id):
    article = Article.query.get_or_404(id)
    db.session.delete(article)
    db.session.commit()
    flash('기사가 삭제되었습니다.', 'success')
    return redirect(url_for('admin.dashboard')) 