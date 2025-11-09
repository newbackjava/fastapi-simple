# python에서 db연결하여 crud처리하는 파일(모듈)
# crud기능 4개 넣을 예정

#1. 라이브러리 필요
import pymysql as mysql
from pymysql import IntegrityError
from pymysql.cursors import DictCursor

def read_count():
    print("read count")
    try:
        # 2. db연결(url(ip+port), id/pw, db명)
        con = mysql.connect(host='localhost',
                            port=3307,
                            user='root',
                            password='1234',
                            db='shop2',
                            cursorclass=DictCursor
                            )
        cursor = con.cursor()

        # 3. sql문 작성한 후 sql문을 db서버에 보내자.
        sql = """
                select count(distinct customers) as count
                from daily_sales_metrics;
                
              """;

        result = cursor.execute(sql);
        print(result);  # insert, update, delete의 결과는 정수값!
        # 실행된 결과의 행수(레코드 개수)
        if result >= 1:
            print("데이터 검색 성공!!! ")
        row = cursor.fetchone(); #전체 목록 다
        # 4. 보낸 sql문을 바로 실행해줘(반영해줘.)
        con.commit();

        # 5. 커넥션 close
        con.close();
    except IntegrityError as ie:
        print("무결성 에러 발생함.")
        print(ie)  # 에러 정보 출력
    return row;

def read_avg():
    try:
        # 2. db연결(url(ip+port), id/pw, db명)
        con = mysql.connect(host='localhost',
                            port=3307,
                            user='root',
                            password='1234',
                            db='shop2',
                            cursorclass=DictCursor
                            )
        cursor = con.cursor()

        # 3. sql문 작성한 후 sql문을 db서버에 보내자.
        sql = """
                SELECT customers, avg(orders) as avg
                FROM daily_sales_metrics group by customers
                ORDER BY avg(orders) DESC
              """;

        result = cursor.execute(sql);
        print(result);  # insert, update, delete의 결과는 정수값!
        # 실행된 결과의 행수(레코드 개수)
        if result >= 1:
            print("데이터 검색 성공!!! ")
        rows = cursor.fetchall(); #전체 목록 다
        # rows = cursor.fetchmany(2); #전체 목록 중 2개만
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

def read_all():
    try:
        # 2. db연결(url(ip+port), id/pw, db명)
        con = mysql.connect(host='localhost',
                            port=3307,
                            user='root',
                            password='1234',
                            db='shop2',
                            cursorclass=DictCursor
                            )
        cursor = con.cursor()

        # 3. sql문 작성한 후 sql문을 db서버에 보내자.
        sql = """
                SELECT revenue, customers
                FROM daily_sales_metrics
                order by revenue desc
                limit 3
              """;

        result = cursor.execute(sql)
        print(result);  # insert, update, delete의 결과는 정수값!
        # 실행된 결과의 행수(레코드 개수)
        if result >= 1:
            print("데이터 검색 성공!!! ")
        rows = cursor.fetchall(); #전체 목록 다
        # rows = cursor.fetchmany(2); #전체 목록 중 2개만
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

