from fastapi import FastAPI, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse
import bbs_db as db

# FastAPI 앱 인스턴스 생성
app = FastAPI()

# 정적 파일 제공 (CSS/JS/이미지)
app.mount("/static", StaticFiles(directory="static"), name="static")

# 템플릿 로더 (templates 디렉터리 지정)
templates = Jinja2Templates(directory="templates")

# 기본 루트 엔드포인트
# @app.get("/")
# def read_root():
#     return {"message": "Hello FastAPI!"}

# 경로 파라미터 예시
@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}

# POST 요청 예시
# @app.post("/users/")
@app.get("/users/{user_id}/{user_name}/{user_age}")
def create_user(user_id: str, user_name: str, user_age: int):
    user = {
        "user_id": user_id,
        "user_name": user_name,
        "user_age": user_age
    }
    return {"user_created": user}

@app.get("/raw")
def raw_html():
    html = """
    <html>
    <head>
     <link rel="stylesheet" href="/static/css/site.css">
    </head>
      <body>
        <h1>Hello</h1>
        <p>템플릿 없이 직접 HTML</p>
      </body>
    </html>
    """
    return HTMLResponse(content=html)

@app.get("/")
def page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/page")
def page2(request: Request):
    return templates.TemplateResponse(
        "page.html",
        {"request" : request, "title": "템플릿 페이지", "items": ["사과","배","포도"]}
    )

@app.get("/page2/{item_id}")
def page3(request: Request, item_id: str):
    print("----", request.query_params)
    print(request.headers)
    data = {"request" : request,
            "title" : "템플릿에 값 넣기",
            "item_id": item_id}
    return templates.TemplateResponse( "page2.html",data)


# http://127.0.0.1:8000/page2?item_id=root
@app.get("/page2")
def page4(request: Request):
    print("----", request.query_params) #---- item_id=root
    print(request.headers)
    data = {"request" : request,
            "title" : "템플릿에 값 넣기",
            "item_id": request.query_params["item_id"]}
    return templates.TemplateResponse( "page2.html",data)

@app.get("/bbs")
def bbs(request: Request):
    return templates.TemplateResponse("bbs.html", {"request": request})

@app.get("/bbs/bbs_insert")
def bbs(request: Request):
    return templates.TemplateResponse("bbs_insert.html", {"request": request})

@app.get("/bbs/bbs_list")
def bbs(request: Request):
    rows = db.read_all();
    print("router --------")
    print(rows)
    print("router --------")
    data = {
            "request" : request,
            "rows": rows
            }
    return templates.TemplateResponse("bbs_list.html", data)

@app.post("/bbs/bbs_insert")
def bbs(request: Request,
        title: str = Form(...),
        content: str = Form(...),
        writer: str = Form(...)):
    db.create([title, content, writer]);
    return RedirectResponse(url="/bbs/bbs_list", status_code=303)
    # 303 get요청, 302는 post/set, 307/308은 메서드 유지