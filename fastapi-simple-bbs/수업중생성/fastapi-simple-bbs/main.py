from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.requests import Request
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse, RedirectResponse

app = FastAPI()
# 정적 파일 제공 (CSS/JS/이미지)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
# @app.get("/")
# def root():
#     #요청들어왔으니 처리한 다음 http응답
#     return "start page ok..!!";

@app.get("/")
def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/bbs")
def bbs(request: Request):
    return templates.TemplateResponse("bbs.html", {"request": request})

@app.get("/addr")
def bbs(request: Request):
    return templates.TemplateResponse("addr.html", {"request": request})

# 데이터가 rest방식으로 ==> 요청주소/값/값/값
# /items/100
@app.get("/items/{item_id}")
def items(request: Request,
          item_id : int):
    print("라우터로 전달된 값>> ", item_id)
    return "ok"

# /items/100/hong
@app.get("/items/{item_id}/{item_name}")
def items2(request: Request,
          item_id : int,
          item_name : str):
    print("라우터로 전달된 값>> ", item_id, item_name)
    return "ok"

# /items?item_id=100&item_name=hong
@app.get("/items")
def items2(request: Request):
    params = request.query_params
    print("라우터로 전달된 값2>> ",
          params['item_id'],
          params['item_name'])
    print(request.headers)
    print(request.method)
    return "ok"


@app.get("/page")
def page2(request: Request):
    data = {
        "request" : request,
        "name" : "hong",
        "age" : 100,
        "food" : ['아이스크림','라떼','레몬']
    }
    return templates.TemplateResponse("page.html", data)