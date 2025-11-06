# import fastapi
# f= fastapi.FastAPI()
#
# import fastapi as f
# f= f.FastAPI()

from fastapi import *
app = FastAPI();

import member_db as db

# http요청하나당 함수하나!!!

@app.get("/")
def root():
    return {"message": "Hello World"}

# /items/100
@app.get("/items/{item_id}")
def item_id(item_id : int):
    return {"item_id_result" : item_id};

# /items/100/sold_out
@app.get("/items/{item_id}/{status}")
def item_id2(item_id : int, status : str):
    data = {
        "item_id_result" : item_id,
        "status" : status
    };
    return data;

@app.post("/users/")
def users(user : dict):
    # {
    #     "user_id": "apple2",
    #     "user_pw": "1234",
    #     "name": "apple",
    #     "tel": "011"
    # }

    list = []
    list.append(user['user_id']);
    list.append(user['user_pw']);
    list.append(user['name']);
    list.append(user['tel']);

    db.create(list)
    return {"user_created" : user}

@app.get("/users/{id}")
def users2(id: str):
    result = db.read_one(id);
    print("db 검색 결과 >> " , result);
    return { "result" : result}

# 회원정보 모두 검색
@app.get("/users/all/")
def users_all():
    result = db.read_all();
    return {"result" : result};

# 회원정보 삭제
@app.delete("/users/{id}")
def delete(id : str):
    db.delete(id);
    return "delete ok!!!";

# 회원정보 수정
@app.put("/users/{id}/{tel}")
def put(id : str, tel : str):
    list = []
    list.append(tel);
    list.append(id);
    db.update(list)
    return "update ok!!!";