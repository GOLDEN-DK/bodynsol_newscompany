# 업무 결정 기록

사용자가 정한 업무 정책을 날짜·결정·근거·영향 문서 순으로 기록한다.

## 2026-11-03 매체명 변경

- 결정: 매체명을 `바디앤솔매거진`에서 `ALL바른매거진`으로 바꾼다.
  - 푸터(회사 정보 줄, 저작권 표기)에는 `ALL바른매거진(바디앤솔매거진)`으로 병기한다.
  - 브라우저 탭 제목, 상단 로고, 새 기사의 작성자 고정값은 `ALL바른매거진`으로 표기한다.
  - 운영 DB의 기존 기사 중 작성자가 `바디앤솔매거진`인 기사도 `ALL바른매거진`으로 바꾼다.
- 근거: 사용자 요청.
- 영향: `app/templates/base.html`, `app/admin/routes.py`, `migrations/versions/c41e7b2a9d05_rename_article_author.py`.

## 2026-11-03 메뉴 정리와 센터 연결

- 결정: 매거진에서 운영하는 카테고리는 사실상 건강뿐이므로 상단 메뉴를 정리한다.
  - 상단 메뉴에는 최근 365일 안에 글이 있는 카테고리만 표시한다(`app/main/routes.py`의 `NAV_CATEGORY_RECENT_DAYS`). 다른 카테고리와 기존 글은 DB에 유지하고 URL로 계속 접근할 수 있다.
  - 상단 메뉴에 "ALL바른 필라테스" 항목을 두고 홈페이지·공지사항·카드뉴스·체험 신청 페이지로 연결한다. 공지사항·카드뉴스 내용은 매거진에 복사하지 않고 홈페이지로 이동하는 링크만 둔다.
  - 홈 1페이지 상단에 센터 소개 문구를, 기사 하단에 체험 신청·홈페이지 방문 버튼을, 푸터에 홈페이지 링크를 둔다.
  - 홈은 최신 메인 기사 1건을 대표 기사로 크게 보여 주고, 나머지는 썸네일 목록으로 보여 준다.
- 근거: 사용자 요청(건강 카테고리만 운영, 센터 소개·홈페이지 연결 필요, 모바일 친화 레이아웃). 365일 기준은 Lead 기본값이다.
- 영향: `app/main/routes.py`, `app/templates/base.html`, `app/templates/main/index.html`, `app/templates/main/category.html`, `app/templates/main/article.html`, `app/static/css/style.css`, `config.py`(`ALLBARUN_URL`).
