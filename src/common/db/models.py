from sqlalchemy import (
    create_engine, Column, BigInteger, String, Date, JSON, DATETIME, ForeignKey, TEXT
)
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func

Base = declarative_base()

class Law(Base):
    __tablename__ = 'law'

    id = Column(BigInteger, primary_key=True)
    law_id = Column(String(20), unique=True, nullable=False)
    law_name = Column(String(255), nullable=False)
    promulgation_number = Column(String(20))
    promulgation_date = Column(Date)
    effective_date = Column(Date)
    ministry_name = Column(String(100))
    details = Column(JSON)
    created_at = Column(DATETIME, default=func.now())
    updated_at = Column(DATETIME, default=func.now(), onupdate=func.now())

    articles = relationship("Article", back_populates="law")

class Article(Base):
    __tablename__ = 'article'

    id = Column(BigInteger, primary_key=True)
    law_id = Column(BigInteger, ForeignKey('law.id'), nullable=False)
    article_number = Column(String(20), nullable=False)
    article_title = Column(String(255))
    content = Column(TEXT)
    effective_date = Column(Date)
    created_at = Column(DATETIME, default=func.now())
    updated_at = Column(DATETIME, default=func.now(), onupdate=func.now())

    law = relationship("Law", back_populates="articles")
