# python에서 db연결하여 crud처리하는 파일(모듈)
# crud기능 4개 넣을 예정

#1. 라이브러리 필요
import pymysql as mysql
from pymysql import IntegrityError


def create(data):
    try :
        # 2. db연결(url(ip+port), id/pw, db명)
        con = mysql.connect(host='localhost',
                            port= 3307,
                            user='root',
                            password='1234',
                            db='cloth'
                            )
        cursor = con.cursor()

        # 3. sql문 작성한 후 sql문을 db서버에 보내자.
        sql = "insert into member values (%s, %s, %s, %s)";
        # values ('ice', 1000)
        # %s --> 'winner'
        # %d --> 1000
        result = cursor.execute(sql, data);
        print(result); # insert, update, delete의 결과는 정수값!
        # 실행된 결과의 행수(레코드 개수)
        if result >= 1 :
            print("데이터 입력 성공!!! ")
        # 4. 보낸 sql문을 바로 실행해줘(반영해줘.)
        con.commit();

        # 5. 커넥션 close
        con.close();
    except IntegrityError as ie:
        print("무결성 에러 발생함.")
        print(ie)  # 에러 정보 출력



# read는 하나 검색과 여러개 검색
def read_one(data):
    try:
        # 2. db연결(url(ip+port), id/pw, db명)
        con = mysql.connect(host='localhost',
                            port=3307,
                            user='root',
                            password='1234',
                            db='cloth'
                            )
        cursor = con.cursor()

        # 3. sql문 작성한 후 sql문을 db서버에 보내자.
        sql = "select * from member where id = %s";
        result = cursor.execute(sql, data);
        print(result);  # insert, update, delete의 결과는 정수값!
        # 실행된 결과의 행수(레코드 개수)
        if result >= 1:
            print("데이터 검색 성공!!! ")
        # 4. 보낸 sql문을 바로 실행해줘(반영해줘.)
        row = cursor.fetchone();
        print("검색결과 row");
        print(row)
        con.commit();

        # 5. 커넥션 close
        con.close();
    except IntegrityError as ie:
        print("무결성 에러 발생함.")
        print(ie)  # 에러 정보 출력
    return row

def read_all():
    try:
        # 2. db연결(url(ip+port), id/pw, db명)
        con = mysql.connect(host='localhost',
                            port=3307,
                            user='root',
                            password='1234',
                            db='cloth'
                            )
        cursor = con.cursor()

        # 3. sql문 작성한 후 sql문을 db서버에 보내자.
        sql = "select * from member";
        # values ('ice', 1000)
        # %s --> 'winner'
        # %d --> 1000
        result = cursor.execute(sql);
        print(result);  # insert, update, delete의 결과는 정수값!
        # 실행된 결과의 행수(레코드 개수)
        if result >= 1:
            print("데이터 입력 성공!!! ")
        # rows = cursor.fetchall(); #전체 목록 다
        rows = cursor.fetchmany(2); #전체 목록 중 2개만
        for row in rows:
            print(row)
        # 4. 보낸 sql문을 바로 실행해줘(반영해줘.)
        con.commit();

        # 5. 커넥션 close
        con.close();
    except IntegrityError as ie:
        print("무결성 에러 발생함.")
        print(ie)  # 에러 정보 출력
    return rows;

def update(data):
    try:
        # 2. db연결(url(ip+port), id/pw, db명)
        con = mysql.connect(host='localhost',
                            port=3307,
                            user='root',
                            password='1234',
                            db='cloth'
                            )
        cursor = con.cursor()

        # 3. sql문 작성한 후 sql문을 db서버에 보내자.
        sql = "update member set tel = %s where id = %s";
        result = cursor.execute(sql, data);
        print(result);  # insert, update, delete의 결과는 정수값!
        # 실행된 결과의 행수(레코드 개수)
        if result >= 1:
            print("데이터 수정 성공!!! ")
        # 4. 보낸 sql문을 바로 실행해줘(반영해줘.)
        con.commit();

        # 5. 커넥션 close
        con.close();
    except IntegrityError as ie:
        print("무결성 에러 발생함.")
        print(ie)  # 에러 정보 출력

def delete(data):
    try:
        # 2. db연결(url(ip+port), id/pw, db명)
        con = mysql.connect(host='localhost',
                            port=3307,
                            user='root',
                            password='1234',
                            db='cloth'
                            )
        cursor = con.cursor()

        # 3. sql문 작성한 후 sql문을 db서버에 보내자.
        sql = "delete from member where id = %s";
        result = cursor.execute(sql, data);
        print(result);  # insert, update, delete의 결과는 정수값!
        # 실행된 결과의 행수(레코드 개수)
        if result >= 1:
            print("데이터 삭제 성공!!! ")
        # 4. 보낸 sql문을 바로 실행해줘(반영해줘.)
        con.commit();

        # 5. 커넥션 close
        con.close();
    except IntegrityError as ie:
        print("무결성 에러 발생함.")
        print(ie)  # 에러 정보 출력

# if __name__ == '__main__':
#     create()