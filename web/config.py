class Config:
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:123qwe@192.168.100.3/blog"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = '12345678'
    SESSION_COOKIE_HTTPONLY = False