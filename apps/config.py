import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Render.com 환경이면 'RENDER=true' 환경변수 존재
if os.environ.get("RENDER") == "true":
    # Render는 /tmp 디렉토리만 쓰기 가능하므로 거기에 DB 파일 생성
    DB_PATH = os.path.join('/tmp', 'app.db')
else:
    # 로컬은 현재 소스 위치에 db 생성 (원하면 다른 경로로 바꿔도 됨)
    from dotenv import load_dotenv
    dotenv_path = os.path.join(BASE_DIR, '..', '.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)
    DB_PATH = os.path.join(BASE_DIR, 'app.db')

# DB 경로의 상위 디렉토리가 없으면 생성
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

#print("SQLITE DB 위치:", DB_PATH)  # 디버깅 용도, 운영 반영 시 삭제 가능

class Config:
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{DB_PATH}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your-default-secret-key')
    WTF_CSRF_SECRET_KEY="mykey"
    API_KEY = os.environ.get('API_KEY')
    LABELS = ['setosa', 'versicolor', 'virginica']
