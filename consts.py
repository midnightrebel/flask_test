import os

from flask import Flask
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
Base = declarative_base()
BASE_URL = os.environ['BASE_URL']
DATABASE_URL = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
db = SQLAlchemy(app)
engine = create_async_engine(DATABASE_URL, echo=True)
async_session = AsyncSession(bind=engine)