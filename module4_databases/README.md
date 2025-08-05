# Module 4: Database integration

## Getting Started
1. **Create a virtual environment:**
    ```bash
    python -m venv .venv
    ```
    
    **Activate the virtual environment:**
    - On macOS/Linux:
    ```bash
    source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
    ```

## PostgreSQL 

1. **Install PostgreSQL:**
   - On macOS, you can use Homebrew:
     ```bash
     brew install postgresql
     ```

   - On Ubuntu:
     ```bash
     sudo apt-get install postgresql postgresql-contrib
     ```

   - On Windows, download the installer from the [PostgreSQL official site](https://www.postgresql.org/download/windows/).  

2. **Start PostgreSQL service:**
   - On macOS:
     ```bash
     brew services start postgresql
     ```
   - On Ubuntu:
     ```bash
     sudo service postgresql start
     ```
   - On Windows, the service should start automatically after installation. 

3. **Create a database:**
   ```bash
   psql -U postgres -c "CREATE DATABASE mydatabase;"
   ```
## Configure Environment Variables
1. **Copy the example environment file:**
   ```bash
   cp .env.example .env
   ```
2. **Edit the `.env` file:**
   - Set your database user and password in the `.env` file:
   ```plaintext
   DB_USER=your_db_user
   DB_PASS=your_db_password 
    ```


## Install Dependencies
1. **Install SQLAlchemy:**
   ```bash
   pip install sqlalchemy
   ```      
1. **Install dotenv:**
   ```bash
   pip install dotenv
   ```
1. **Install psycopg2:**
   ```bash
   pip install psycopg2

## Practical Exercises: One-to-Many Relationships with SQLAlchemy

### ✅ Problem 1: Define One-to-Many Models
- Objective: Model a one-to-many relationship between `Article` and `Comment`.
- Instructions:
  - In `models/article_comment_onetomany.py`, define two SQLAlchemy models:
    - `Article`:
        - Fields: `id` (primary key), `title` (required)
    - Relationship: One Article has many Comments
    - `Comment`:
      - Fields: `id` (primary key), `content` (required), `article_id` (foreign key)
    - Constraints:
        - Use SQLAlchemy's relationship() and ForeignKey() to link the models.

  - Use `declarative_base()` to define the ORM base class.

### ✅ Problem 2: Setup and Configure the Database
- Objective: Create the PostgreSQL connection and initialize the database schema.
- Instructions:
    - In `main.py`, do the following:
      - Load environment variables using `dotenv`.
      - Read `DB_USER` and `DB_PASS` from .env, with fallback defaults.
      - Create a connection string:
        ```
        postgresql://<DB_USER>:<DB_PASS>@localhost/fastapi_week4
        ```
      - Use `create_engine()` to initialize a SQLAlchemy engine.
      - Use `Base.metadata.create_all()` to create tables.

### ✅ Problem 3: Add a Sample Article and Related Comments
- Objective: Populate the database with sample data.
- Instructions:
    - Create a session using sessionmaker.
    - Create one Article titled "Sample Article".
    - Create two Comment objects with different content.
    - Associate the comments with the article using:
      ```python
      article.comments = [comment1, comment2]
      ```
    - Add and commit the article (with comments) to the session.

### ✅ Problem 4: Query Article and Its Comments
- Objective: Retrieve an article and print its related comments.
- Instructions:
  - Use a new session to query the first article from the database.
  - Print: 
      - Article ID
      - Number of comments
      - Each comment's ID

## Hints

### Create models
1. `models/article_comment_onetomany.py`

    ```python
    from sqlalchemy import Column, Integer, String, ForeignKey
    from sqlalchemy.orm import relationship
    from sqlalchemy.ext.declarative import declarative_base


    Base = declarative_base()

    class Article(Base):
        __tablename__ = 'articles'
        id = Column(Integer, primary_key=True)
        title = Column(String, nullable=False)
        comments = relationship("Comment")


    class Comment(Base):
        __tablename__ = 'comments'
        id = Column(Integer, primary_key=True)
        content = Column(String, nullable=False)
        article_id = Column(Integer, ForeignKey('articles.id'))
    ```

### Create Database Connection and Initialize Tables

1. `main.py`

    ```python
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
    ```

## Run the Application

1. **Run the database app:**
    ```bash
    python main.py
    ```