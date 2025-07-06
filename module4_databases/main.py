import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from models.article_comment_onetomany import Article, Comment
from sqlalchemy.orm import sessionmaker

from models.article_comment_onetomany import Base

load_dotenv()

# Read DB_USER and DB_PASS from environment variables
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "postgres")
print(f"DB_USER: {DB_USER}, DB_PASS: {DB_PASS}")


SQLALCHEMY_DATABASE_URL = f'postgresql://{DB_USER}:{DB_PASS}@localhost/fastapi_week4'

# Create the SQLAlchemy engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create session
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
Base.metadata.create_all(bind=engine)

with Session() as session:
    article = Article(title="Sample Article")
    comment1 = Comment(content="This is the first comment.")
    comment2 = Comment(content="This is the second comment.")
    article.comments = [comment1, comment2]
    session.add(article)
    session.commit()


# Query the article and its comments
with Session() as session:
    article = session.query(Article).first()
    print(f"Article ID: {article.id}, Number of Comments: {len(article.comments)}")
    for comment in article.comments:
        print(f"Comment ID: {comment.id}")
