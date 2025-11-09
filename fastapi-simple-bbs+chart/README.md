
# FastAPI + MySQL + Google Charts 대시보드 사용 설명서

> **목표**: FastAPI 서버에서 MySQL 데이터를 조회하여 **Google Charts**(PieChart, Gauge)를 웹에 시각화하고, 간단한 **게시판(BBS)** CRUD까지 동작하는 프로젝트의 **설치·구성·실행·확장** 가이드

---

## 데이터 흐름 다이어그램

<img width="1482" height="1036" alt="스크린샷 2025-11-09 09 32 09" src="https://github.com/user-attachments/assets/bdfbc957-2154-4ed4-9029-21beee713eae" />

---
<a href=https://developers.google.com/chart/interactive/docs/gallery">google chart</a>
<img width="1045" height="618" alt="스크린샷 2025-11-09 11 16 59" src="https://github.com/user-attachments/assets/1d89fb2f-bb23-423b-83d7-c89849569a5f" />

---
<img width="1400" height="900" alt="fastapi_chart_flow_10pt_color" src="https://github.com/user-attachments/assets/30e1132b-1114-4f12-b69a-01d4341abadf" />

---
<img width="1400" height="980" alt="2d_list_diagram_10pt_color_nokr_spaced" src="https://github.com/user-attachments/assets/6f03fd54-b5cc-413f-8665-0d3baf36268b" />

---

> 브라우저가 `/chart` 페이지를 요청하면 템플릿이 렌더링되고, 템플릿 내 JS가 `axios`로 `/chart/count`, `/chart/avg`, `/chart/all`을 호출합니다.  
> FastAPI는 `chart_db.py`를 통해 MySQL에서 데이터를 조회하여 JSON으로 반환하고, Google Charts가 JSON을 DataTable로 변환해 PieChart와 Gauge로 렌더링합니다.

---

## 1) 전체 아키텍처 개요

- **클라이언트(브라우저)**: Jinja2 템플릿으로 렌더링된 HTML + `axios`로 REST API 호출 → Google Charts로 시각화
- **FastAPI 서버**: 라우팅, 템플릿 렌더링, REST API 제공(`/chart/*`, `/bbs/*` 등)
- **DB 계층(MySQL 8)**: `daily_sales_metrics` 테이블에서 판매/고객 지표 읽기, 게시판(BBS) 테이블 CRUD
- **정적 리소스**: `/static` 경로로 CSS/JS/이미지 제공

데이터 흐름(요약):
1. 브라우저가 `/chart` 페이지 요청 → 템플릿 렌더링
2. 템플릿 내 JS가 `axios`로 `/chart/count`, `/chart/avg`, `/chart/all` 호출
3. FastAPI가 `chart_db.py`를 통해 MySQL 조회 결과를 JSON으로 반환
4. Google Charts가 JSON → DataTable로 변환하여 **파이차트**와 **게이지**를 렌더링

---

## 2) 디렉터리 구조 예시

```
project-root/
├─ main.py                 # FastAPI 라우터/템플릿 연결/엔드포인트
├─ bbs_db.py               # BBS CRUD 모듈
├─ chart_db.py             # Chart용 조회(read_count/read_avg/read_all)
├─ templates/
│  ├─ base.html
│  ├─ index.html
│  ├─ page.html
│  ├─ page2.html
│  ├─ bbs.html
│  ├─ bbs_list.html
│  ├─ bbs_read.html
│  ├─ bbs_update.html
│  ├─ bbs_insert.html
│  └─ chart.html           # 차트 페이지(구글 차트 + axios)
├─ static/
│  ├─ css/site.css
│  ├─ js/app.js
│  └─ img/
│     └─ ...               # 스크린샷/아이콘 등
└─ requirements.txt
```

> 실제 파일명은 코드에 맞추어 사용하세요. `app.mount("/static", StaticFiles(directory="static"), name="static")` 이므로 정적 경로는 `/static/*` 입니다.

---

## 3) 사전 준비

### 3.1 필수 소프트웨어
- **Python 3.10+**
- **MySQL 8.x**
- **pip** (가상환경 권장)
- (선택) **Uvicorn** 또는 **Hypercorn**

### 3.2 Python 패키지
`requirements.txt` 예시:
```
fastapi
uvicorn[standard]
jinja2
pymysql
python-multipart
starlette
```

설치:
```bash
pip install -r requirements.txt
```

### 3.3 MySQL 준비
- 접속 정보(예시)
  - host: `localhost`
  - port: `3307`  ← 코드에서 3307 사용
  - user: `root`
  - password: `1234`
  - database: `shop2`

> 포트/계정/DB명은 시스템에 맞게 수정하세요. `chart_db.py`/`bbs_db.py`와 일치해야 합니다.

---

## 4) DB 스키마 및 테스트 데이터

### 4.1 지표 테이블 생성/샘플 데이터
```sql
CREATE TABLE daily_sales_metrics (
  id         INT AUTO_INCREMENT PRIMARY KEY,
  sale_date  DATE            NOT NULL,
  orders     INT             NOT NULL,
  revenue    DECIMAL(12,2)   NOT NULL,
  customers  INT             NOT NULL
);

DELETE FROM daily_sales_metrics;

INSERT INTO daily_sales_metrics (sale_date, orders, revenue, customers) VALUES
('2025-10-20', 40, 520000.00, 35),
('2025-10-21', 44, 575000.00, 39),
('2025-10-22', 38, 500000.00, 33),
('2025-10-23', 47, 615000.00, 41),
('2025-10-24', 52, 680000.00, 39),
('2025-10-25', 60, 820000.00, 35),
('2025-10-26', 58, 790000.00, 48),
('2025-10-27', 43, 560000.00, 37),
('2025-10-28', 45, 590000.00, 35),
('2025-10-29', 49, 640000.00, 39),
('2025-10-30', 55, 720000.00, 47),
('2025-10-31', 62, 880000.00, 35),
('2025-11-01', 57, 760000.00, 49),
('2025-11-02', 63, 900000.00, 39),
('2025-11-03', 50, 680000.00, 35),
('2025-11-04', 48, 650000.00, 42),
('2025-11-05', 52, 700000.00, 46),
('2025-11-06', 54, 730000.00, 47),
('2025-11-07', 59, 820000.00, 39),
('2025-11-08', 61, 860000.00, 39);
```

### 4.2 확인용 쿼리
- 건수/목록:
```sql
SELECT sale_date, revenue, orders FROM daily_sales_metrics ORDER BY sale_date;
SELECT * FROM daily_sales_metrics;
SELECT COUNT(*) FROM daily_sales_metrics;
```
- 고객 수별 평균 주문수:
```sql
SELECT customers, AVG(orders) FROM daily_sales_metrics GROUP BY customers;
SELECT COUNT(DISTINCT customers) FROM daily_sales_metrics;
SELECT COUNT(*) FROM daily_sales_metrics WHERE customers = 35;
```
- 차트 API에서 사용하는 쿼리(요약):
```sql
-- /chart/count
SELECT COUNT(DISTINCT customers) AS count FROM daily_sales_metrics;

-- /chart/avg
SELECT customers, AVG(orders) AS avg
FROM daily_sales_metrics
GROUP BY customers
ORDER BY AVG(orders) DESC;

-- /chart/all
SELECT revenue, customers
FROM daily_sales_metrics
ORDER BY revenue DESC
LIMIT 3;
```

---

## 5) 핵심 파이썬 모듈 설명

### 5.1 `chart_db.py` (DB 조회 전용)
- **공통 연결**: `pymysql.connect(..., cursorclass=DictCursor)` 로 dict 결과
- **함수**
  - `read_count()` → `{ "count": <고객 수 중복 제거한 개수> }`
  - `read_avg()` → `[{"customers": <int>, "avg": <Decimal>}, ...]` 리스트
  - `read_all()` → 상위 3개 매출 `[{"revenue": <Decimal>, "customers": <int>}, ...]`

> 반환 값을 그대로 FastAPI에서 JSON으로 응답하므로, **Decimal 직렬화**가 가능하도록 DictCursor 사용 및 FastAPI의 기본 JSON 인코더(Starlette) 활용.

### 5.2 `bbs_db.py` (게시판 CRUD)
- `create([title, content, writer])`
- `read_all()` / `read_one(no)` / `read_search(q)`
- `update([title, content, no])`
- `delete(no)`

> 실제 BBS 테이블 정의는 프로젝트에 맞게 구현하세요. (예: `BBS(no INT AUTO_INCREMENT PK, title TEXT, content TEXT, writer VARCHAR(50))`)

### 5.3 `main.py` (라우팅/템플릿)
- 정적 경로: `app.mount("/static", StaticFiles(directory="static"), name="static")`
- 템플릿: `templates = Jinja2Templates(directory="templates")`
- 예제 라우트: `/items/{item_id}`, `/users/{...}`, `/raw`
- **템플릿 렌더링**: `TemplateResponse` 사용 시 `{"request": request}` **반드시 포함**
  - 이유: Jinja2 템플릿 내에서 `url_for` 등 Starlette 컨텍스트가 필요하기 때문
- **BBS 라우트**
  - GET `/bbs/bbs_insert` : 작성 폼
  - POST `/bbs/bbs_insert` : `Form(...)`로 값 수신 후 DB `create` → `RedirectResponse("/bbs/bbs_list", 303)`
  - GET `/bbs/bbs_list` : 목록
  - GET `/bbs/bbs_read/{no}` : 상세
  - GET `/bbs/bbs_update/{no}` : 수정 폼
  - POST `/bbs/bbs_update` : 수정 반영
  - POST `/bbs/bbs_delete/{no}` : 삭제
- **차트 라우트**
  - GET `/chart` : 차트 페이지 템플릿
  - GET `/chart/count` : `{ "count": 10 }` 형태
  - GET `/chart/avg` : `{ "avg": [ {customers, avg}, ...] }`
  - GET `/chart/all` : `{ "all": [ {revenue, customers}, ...] }`

---

## 6) 템플릿(`chart.html`) 자바스크립트 동작

### 6.1 회원수(고객수 종류) 표시
```javascript
axios.get('/chart/count').then(res => {
  document.getElementById('count').innerHTML =
    "전체 회원수 : " + res.data.count + "명";
});
```

### 6.2 파이 차트 (고객 수별 평균 주문수)
```javascript
google.charts.load('current', {'packages':['corechart']});
google.charts.setOnLoadCallback(drawChart);

async function drawChart() {
  await axios.get('/chart/avg').then(res => {
    const data = res.data.avg;
    const total = [['avg', 'Customers']];
    for (const x of data) {
      total.push([String(x.customers), x.avg]);
    }
    const dataTable = google.visualization.arrayToDataTable(total);
    const options = { title: 'Customers Avg' };
    const chart = new google.visualization.PieChart(
      document.getElementById('piechart'));
    chart.draw(dataTable, options);
  });
}
```

- **포인트**
  - Google DataTable 첫 행은 **헤더**
  - 숫자/문자 타입 일치 필요 (여기서는 customers를 `String`으로 변환하여 범례에 라벨로 사용)

### 6.3 게이지 (매출 상위 3건)
```javascript
google.charts.load('current', {'packages':['gauge']});
google.charts.setOnLoadCallback(drawChart2);

async function drawChart2() {
  await axios.get('/chart/all').then(res => {
    const data2 = res.data.all;
    const total2 = [['customers', 'revenue']];
    for (const x of data2) {
      total2.push([String(x.customers), x.revenue]);
    }
    const dt = google.visualization.arrayToDataTable(total2);

    const options2 = {
      width: 900, height: 600,
      redFrom: 90, redTo: 100,
      yellowFrom: 75, yellowTo: 90,
      minorTicks: 5
    };

    const chart2 = new google.visualization.Gauge(
      document.getElementById('chart_div'));

    chart2.draw(dt, options2);

    // 데모용 랜덤 업데이트 (실서비스에서는 제거 권장)
    setInterval(function() {
      dt.setValue(0, 1, 40 + Math.round(60 * Math.random()));
      chart2.draw(dt, options2);
    }, 13000);
    // ...
  });
}
```

- **주의**: Gauge는 보통 `0~100` 스케일 가정. 현재 `revenue` 값이 **십만~백만 단위**이므로 게이지 범위와 단위가 맞지 않을 수 있습니다.  
  - 해결: `revenue`를 **정규화(예: 만원 단위, 또는 백분율)** 하거나 `max` 옵션을 크게 지정하세요.

---

## 7) 실행 방법

1. **DB에 테이블/데이터 생성**
2. **환경 변수 또는 코드에서 DB 접속 값 확인(포트 3307 등)**
3. 서버 실행:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
4. 브라우저에서:
   - `http://127.0.0.1:8000/` (메인)
   - `http://127.0.0.1:8000/chart` (차트)
   - `http://127.0.0.1:8000/bbs/bbs_list` (게시판)

---

## 8) 공통 이슈 및 해결 팁

### 8.1 MySQL 접속 오류
- **포트/계정/비밀번호** 재확인 (현재 코드 3307)
- 방화벽/바인딩 주소(`bind-address`) 확인
- `pymysql.err.OperationalError` 발생 시 에러코드로 원인 확인

### 8.2 Decimal 직렬화/타입 문제
- DictCursor 사용으로 대부분 해결되지만, 차트 데이터로 넘길 때 **문자/숫자형 변환** 유의
- 게이지에 큰 수치를 직접 사용하면 시계가 0~100 범위 밖이므로 **스케일링** 권장

### 8.3 템플릿에서 `request` 필수인 이유
- Starlette `TemplateResponse`는 템플릿 컨텍스트에 `request` 객체가 있어야 `url_for`, `request` 접근 가능

### 8.4 CORS
- 다른 도메인에서 API를 호출할 경우:
```python
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)
```
> 내부/개발용에서만 `*` 사용. 운영은 신중하게 설정.

### 8.5 보안·안정성
- **SQL 인젝션 방지**: 파라미터 바인딩(`cursor.execute(sql, params)`) 사용
- **예외 처리**: `try/except`로 DB 예외 로깅, 사용자 메시지는 일반화
- **리다이렉트 코드**: POST 후 `303 See Other`로 GET 목록 이동은 **좋은 패턴**

### 8.6 성능 팁
- 빈번한 DB 호출 시 **커넥션 풀**(e.g., `aiomysql` 또는 풀 구현) 고려
- 차트 데이터는 **캐싱**(예: 30초)하면 부하 감소
- 정적 리소스는 CDN/압축 적용

---

## 9) 확장 아이디어

- **기간 필터** 추가: `/chart/avg?start=2025-10-01&end=2025-10-31`
- **차트 종류 확대**: ColumnChart/LineChart로 매출 추이 표시
- **리포트 API**: `CSV/XLSX` 다운로드
- **권한/인증**: BBS 작성/수정/삭제에 인증 토큰 적용
- **비동기 DB**: `databases` or `SQLAlchemy + async`로 전환

---

## 10) 테스트 시나리오(핵심)

1. `/chart/count` 응답에 `count` 키 존재, 정수값 검증
2. `/chart/avg` 응답 배열 길이 = `DISTINCT customers` 개수
3. `/chart/all` 길이 3, revenue 내림차순 정렬 확인
4. `chart.html` 파이차트/게이지가 렌더링되는지 시각 확인
5. BBS: 작성→목록→상세→수정→삭제 전체 플로우 동작

---

## 11) 배포 참고

- **Uvicorn + Nginx** 리버스 프록시
- **환경변수**로 DB 접속 정보 주입 (`os.getenv` 사용)
- **로깅/모니터링**: Uvicorn/Access Log, 에러 추적 도구(Sentry 등)

---

## 12) 자주 묻는 질문(FAQ)

- **Q. 모든 엔드포인트를 비동기로 바꿔야 하나요?**  
  A. 필수는 아닙니다. 현재 코드는 동기 `pymysql` 사용. 고부하 환경이면 `async` 전환을 고려하세요.

- **Q. CSRF를 폼에서 꼭 써야 하나요?**  
  A. API + SPA 조합에서는 토큰 기반 인증을 주로 사용합니다. 전통적 서버 렌더링 폼 제출엔 CSRF가 유용합니다.

- **Q. 템플릿에서 `request`를 왜 전달하나요?**  
  A. `url_for` 등 템플릿 기능에서 `request` 컨텍스트가 필요하기 때문입니다.

---

## 13) API 계약 요약

| 경로 | 메서드 | 요청 파라미터 | 응답 예시 | 설명 |
|---|---|---|---|---|
| `/chart/count` | GET | - | `{ "count": 10 }` | 중복 없는 `customers` 수 |
| `/chart/avg` | GET | - | `{ "avg": [{"customers":39,"avg":54.6667}, ...] }` | 고객별 평균 주문수, 내림차순 |
| `/chart/all` | GET | - | `{ "all": [{"revenue":900000.00,"customers":39}, ...] }` | 매출 상위 3건 |
| `/bbs/bbs_list` | GET | - | HTML | 게시글 목록 |
| `/bbs/bbs_insert` | GET | - | HTML | 작성 폼 |
| `/bbs/bbs_insert` | POST | `title, content, writer` | 303 Redirect | 글 등록 |
| `/bbs/bbs_read/{no}` | GET | `no` | HTML | 글 상세 |
| `/bbs/bbs_update/{no}` | GET | `no` | HTML | 수정 폼 |
| `/bbs/bbs_update` | POST | `no, title, content` | 303 Redirect | 수정 반영 |
| `/bbs/bbs_delete/{no}` | POST | `no` | 303 Redirect | 삭제 |

---

## 14) 마무리 정리 표

| 구분 | 핵심 내용 | 체크포인트 |
|---|---|---|
| 환경 | Python 3.10+, MySQL 8, FastAPI, Jinja2, PyMySQL | 포트 3307/DB명/계정 확인 |
| DB | `daily_sales_metrics` 스키마 + 샘플 데이터 | 쿼리 3종(`/chart/*`) 정상 동작 |
| 서버 | `main.py` 라우팅, 템플릿 렌더링 | `{"request": request}` 포함 필수 |
| 차트 | PieChart(평균 주문수), Gauge(상위 매출) | DataTable 헤더/타입 일치, 게이지 스케일 |
| BBS | 작성/목록/상세/수정/삭제 | POST 후 303 리다이렉트 |
| 보안 | 파라미터 바인딩, CORS, 예외처리 | 운영 시 인증/권한 도입 |
| 성능 | 커넥션 풀/캐싱 고려 | 고빈도 API 최적화 |
| 확장 | 기간 필터/추가 차트/리포트 | CSV/XLSX, 권한체계 |

---

**부록**: 게이지 스케일 조정 팁  
- 예: `revenue`(원)를 `만 단위`로 나눈 값 사용 → 게이지 `0~100` 내에서 시각적으로 안정적  
- 또는 `options: {max: 1000000}`과 같이 최대값을 늘려 실제 금액을 직접 표현



---


