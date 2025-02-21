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
        # 폼 데이터 검증
        if not request.form.get('title') or not request.form.get('content'):
            flash('제목과 내용은 필수입니다.', 'error')
            return redirect(url_for('admin.create_article'))

        try:
            # 기사 객체 생성
            article = Article(
                title=request.form['title'],
                content=request.form['content'],
                summary=request.form.get('summary', ''),
                source_link=request.form.get('source_link', ''),
                author=current_user.username,
                category_id=request.form.get('category_id'),
                is_main=bool(request.form.get('is_main')),
                main_image=request.form.get('main_image', '')
            )
            
            # 데이터베이스에 저장
            db.session.add(article)
            db.session.commit()
            
            print(f"Article created successfully: ID={article.id}, Title={article.title}")
            flash('기사가 성공적으로 등록되었습니다.', 'success')
            return redirect(url_for('admin.dashboard'))
            
        except Exception as e:
            db.session.rollback()
            print(f"Error creating article: {str(e)}")
            flash('기사 등록 중 오류가 발생했습니다.', 'error')
            return redirect(url_for('admin.create_article'))
    
    # GET 요청 처리
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
        article.category_id = request.form['category_id']
        article.is_main = bool(request.form.get('is_main'))
        article.main_image = request.form.get('main_image')
        
        db.session.commit()
        flash('기사가 성공적으로 수정되었습니다.', 'success')
        return redirect(url_for('admin.dashboard'))
    
    categories = Category.query.all()
    return render_template('admin/edit_article.html', article=article, categories=categories)

@bp.route('/article/<int:id>/delete', methods=['POST'])
@login_required
def delete_article(id):
    article = Article.query.get_or_404(id)
    db.session.delete(article)
    db.session.commit()
    flash('기사가 삭제되었습니다.', 'success')
    return redirect(url_for('admin.dashboard')) 