# fastapi-simple — 사용설명서 (README)
<img width="1680" height="1528" alt="스크린샷 2025-11-07 06 51 32" src="https://github.com/user-attachments/assets/d00218c3-11ca-40a1-bf07-2932f280b86d" />
<img width="899" height="822" alt="스크린샷 2025-11-07 07 41 55" src="https://github.com/user-attachments/assets/522899e5-a74d-4416-bdd9-11a655dffa2b" />


## 개요
이 레포는 FastAPI + Jinja2 + StaticFiles(이미지/CSS/JS)로 구성된 **초간단 서버 렌더링 예제**입니다.  
게시판(BBS) 목록/등록 화면, 기본 라우팅, 템플릿 상속, 정적 리소스 제공까지 최소 기능을 담았습니다.

- 프레임워크: FastAPI / Starlette
- 템플릿: Jinja2
- DB 드라이버: PyMySQL (동기)
- 실행: Uvicorn 개발 서버

---

## 폴더 구조
```
fastapi-simple/
├─ main.py                    # FastAPI 엔트리포인트(라우트/템플릿 렌더)
├─ bbs_db.py                  # MySQL 연동 CRUD 유틸
├─ requirements.txt           # 의존성 목록
├─ templates/                 # Jinja2 템플릿
│  ├─ base.html               # 공통 레이아웃
│  ├─ index.html              # 메인 페이지
│  ├─ page.html               # 샘플: 리스트 렌더
│  ├─ page2.html              # 샘플: Path Param 렌더
│  ├─ bbs.html                # BBS 입구(링크 모음)
│  ├─ bbs_list.html           # BBS 목록 화면
│  └─ bbs_insert.html         # BBS 등록 화면 (카드/표 스타일)
└─ static/
   ├─ css/site.css            # 스타일
   └─ js/app.js               # 스크립트
```
> `app.mount("/static", ...)` 로 `/static/...` 경로에 정적 리소스를 서빙합니다.

---

## 요구 사항
- Python 3.10+ 권장
- MySQL 8.x (또는 호환 MariaDB) — 이 예제는 **로컬 MySQL:3307, DB=shop2** 기준
- OS 제약 없음 (Windows / macOS / Linux)

---

## 설치 및 실행

### 1) 가상환경(선택)
```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
```

### 2) 의존성 설치
```bash
pip install -r fastapi-simple/requirements.txt
```
> `requirements.txt` 예시: fastapi, uvicorn, pymysql 등

### 3) 개발 서버 실행
작업 디렉터리를 `fastapi-simple/` 로 맞춘 뒤 실행합니다.
```bash
cd fastapi-simple
uvicorn main:app --reload --port 8000
```
- 접속: http://127.0.0.1:8000
- 문서: http://127.0.0.1:8000/docs (Swagger) / http://127.0.0.1:8000/redoc

---

## 데이터베이스 설정

### 연결 정보 (기본값)
`bbs_db.py`에 하드코딩되어 있습니다.
- host=`localhost`
- port=`3307`
- user=`root`
- password=`1234`
- database=`shop2`

> 운영/팀 협업 시 **환경변수**로 바꿔 주입하는 방식을 권장합니다.

### 테이블 스키마 예시 (MySQL)
```sql
CREATE DATABASE IF NOT EXISTS shop2 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
USE shop2;

CREATE TABLE IF NOT EXISTS bbs (
  no        INT AUTO_INCREMENT PRIMARY KEY,
  title     VARCHAR(200)   NOT NULL,
  content   TEXT           NOT NULL,
  writer    VARCHAR(50)    NOT NULL,
  created_at DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 샘플 데이터
INSERT INTO bbs (title, content, writer) VALUES
('fun',  'friday', 'apple'),
('test', 'test',   'apple'),
('test', 'test',   'apple'),
('test2','test2',  'apple');
```

### 쿼리 사용 방식
`bbs_db.py` 내부에서 **PyMySQL + DictCursor**로 아래 패턴을 사용합니다.
```python
# 예시
SELECT * FROM bbs;                    # 목록
SELECT * FROM bbs WHERE no = %s;      # 단건 조회
INSERT INTO bbs(title, content, writer) VALUES (%s, %s, %s);
```
> `cursor.fetchall()`은 DictCursor 사용 시 `[{...}, {...}]` 형태로 반환됩니다.

---

## 라우팅(엔드포인트)

`main.py` 기준 등록된 경로

| 메서드 | 경로 | 설명 |
|---|---|---|
| GET | `/` | 메인 페이지(템플릿) |
| GET | `/items/{item_id}` | 샘플: Path Param 처리 |
| POST | `/users/` | 샘플: Form/Body 처리 예제 |
| GET | `/users/{user_id}/{user_name}/{user_age}` | 샘플: 다중 Path Param |
| GET | `/raw` | 샘플: HTMLResponse로 원시 HTML 반환 |
| GET | `/page` | 샘플: 리스트 렌더 템플릿 |
| GET | `/page2` | 샘플: 쿼리/기본값 렌더 |
| GET | `/page2/{item_id}` | 샘플: Path Param 렌더 |
| GET | `/bbs` | BBS 입구(링크) |
| GET | `/bbs/bbs_list` | **BBS 목록 화면** 렌더(검색 지원, 페이지네이션 없음) |
| GET | `/bbs/bbs_insert` | **BBS 등록 폼 화면** (카드+표 UI) |
| POST | `/bbs/bbs_insert` | **BBS 등록 처리** → 303 리다이렉트(`/bbs/bbs_list`) |

> `bbs_list.html`은 카드 상단 이미지 + 검색툴바 + 테이블로 구성되어 있습니다. 날짜는 `strftime('%Y-%m-%d %H:%M')`로 간단 표기합니다.

---

## 템플릿 가이드

- **레이아웃**: `base.html`을 상속하여 공통 `<head>`, 정적리소스 링크, `{% block content %}` 제공
- **BBS 등록 화면**: `bbs_insert.html`  
  - 카드 레이아웃, 상단 이미지, 표 기반 폼
  - `<form action="/bbs/bbs_insert" method="post">`
  - 필드: `title`, `content`, `writer`
  - (선택) CSRF 토큰 hidden 필드
- **BBS 목록 화면**: `bbs_list.html`  
  - 카드 레이아웃, 상단 이미지
  - 검색 입력 `q`(제목/내용/작성자 대상 부분 일치)
  - 액션 버튼: View/Edit/Delete(경로만 제공; 백엔드 구현은 선택)

---

## 커스터마이징 팁

1. **DB 접속 정보 외부화**  
   - `os.environ.get()`로 읽고, 기본값(fallback) 제공
   - 예) `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASS`, `DB_NAME`
2. **CSRF 보호(선택)**  
   - Starlette/FastAPI 전용 미들웨어 또는 자체 토큰 발급/검증
   - 템플릿에 hidden input 삽입
3. **에러 처리**  
   - DB 커넥션 예외(네트워크/권한) 핸들링
   - 입력 검증(빈 제목/작성자 등) 보강
4. **페이지네이션 추가(선택)**  
   - `LIMIT/OFFSET` 사용, 쿼리파라미터 `page`, `page_size`
5. **로깅**  
   - `logging`으로 요청/쿼리/에러 로깅
6. **배포**  
   - `gunicorn -k uvicorn.workers.UvicornWorker -w 2 main:app`
   - Nginx 리버스프록시, 정적 리소스 캐싱

---

## 자주 묻는 질문(FAQ)

**Q. 템플릿에서 `request`를 꼭 넘겨야 하나요?**  
A. `TemplateResponse`로 렌더링 시 `{"request": request}`를 컨텍스트에 포함하는 것이 FastAPI/Jinja2 통합의 표준 패턴입니다.

**Q. Dict 형태로 결과를 받고 싶습니다.**  
A. PyMySQL의 `DictCursor`를 사용하세요. 커서 또는 연결에 `cursorclass=DictCursor`를 지정하면 됩니다.

**Q. 등록 후 303 리다이렉트 이유는?**  
A. 새로고침 시 중복 POST를 예방하기 위한 **PRG(Post-Redirect-Get)** 패턴입니다. 303은 브라우저가 GET으로 다시 요청하도록 보장합니다.

**Q. CSRF는 필수인가요?**  
A. 내부망/학습 목적이라면 생략 가능하지만, 운영 서비스라면 필수에 가깝습니다(세션/토큰 방식 권장).


---

## 요약 표

| 항목 | 값/설명 |
|---|---|
| 런타임 | Python 3.10+ |
| 핵심 라이브러리 | fastapi, uvicorn, pymysql, jinja2 |
| 실행 명령 | `cd fastapi-simple && uvicorn main:app --reload --port 8000` |
| 정적 경로 | `/static/...` (StaticFiles) |
| 템플릿 | `templates/` (`base.html` 상속) |
| DB | MySQL(로컬 3307), DB명 `shop2`, 테이블 `bbs` |
| BBS 경로 | 목록 `/bbs/bbs_list`, 등록화면 `/bbs/bbs_insert`(GET), 등록처리 `/bbs/bbs_insert`(POST) |
| 포맷 | 날짜: `YYYY-MM-DD HH:MM` |
| 보안(선택) | CSRF 토큰, 입력 검증, 예외 처리 |


---

## db query성능 비교
<img width="3162" height="1356" alt="스크린샷 2025-11-07 07 48 14" src="https://github.com/user-attachments/assets/6395b36c-d346-4c52-ac2c-8f44111a0e60" />
<img width="3164" height="1394" alt="스크린샷 2025-11-07 07 47 49" src="https://github.com/user-attachments/assets/8a7375ec-a819-4e9f-b379-e9a75658146f" />
<img width="3170" height="1586" alt="스크린샷 2025-11-07 07 47 32" src="https://github.com/user-attachments/assets/396b058b-837c-43f9-831f-b8b21f1f9245" />
<img width="3166" height="1616" alt="스크린샷 2025-11-07 07 46 53" src="https://github.com/user-attachments/assets/ae5019e1-a661-47e6-9182-116c594b369e" />

-- 


-- 

## csv import/export
<img width="1618" height="1224" alt="스크린샷 2025-11-07 07 43 34 (1)" src="https://github.com/user-attachments/assets/3cf8dc8a-7c18-4bc2-aecd-ae720c3e6259" />

<img width="809" height="612" alt="스크린샷 2025-11-07 07 43 34" src="https://github.com/user-attachments/assets/f3f76e1f-b42b-4987-b69e-a3eff831ccbf" />



