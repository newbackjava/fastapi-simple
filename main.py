from fastapi import FastAPI

# FastAPI 앱 인스턴스 생성
app = FastAPI()

# 기본 루트 엔드포인트
@app.get("/")
def read_root():
    return {"message": "Hello FastAPI!"}

# 경로 파라미터 예시
@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "query": q}

# POST 요청 예시
@app.post("/users/")
def create_user(user: dict):
    return {"user_created": user}
