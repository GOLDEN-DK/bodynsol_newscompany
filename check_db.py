import psycopg2
import os

# 데이터베이스 연결 정보
db_params = {
    'host': 'ep-flat-lake-a5zf4bdd-pooler.us-east-2.aws.neon.tech',
    'database': 'neondb',
    'user': 'neondb_owner',
    'password': 'npg_AKaJ7IyBrX5R',
    'sslmode': 'require'
}

try:
    # 데이터베이스 연결
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()
    
    # 테이블 목록 조회
    cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
    """)
    
    tables = cursor.fetchall()
    
    print("데이터베이스 연결 성공!")
    print("테이블 목록:")
    for table in tables:
        print(f"- {table[0]}")
    
    # 테이블이 있으면 스키마 확인
    if tables:
        for table in tables:
            table_name = table[0]
            print(f"\n테이블 '{table_name}'의 스키마:")
            cursor.execute(f"""
                SELECT column_name, data_type 
                FROM information_schema.columns 
                WHERE table_name = '{table_name}'
            """)
            columns = cursor.fetchall()
            for column in columns:
                print(f"  - {column[0]}: {column[1]}")
    else:
        print("\n데이터베이스에 테이블이 없습니다.")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"데이터베이스 연결 오류: {e}") 