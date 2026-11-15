from datetime import datetime
from typing import Optional
import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column
from app import db


class Post(db.Model):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    title: Mapped[str] = mapped_column(sa.String(150), nullable=False)
    content: Mapped[str] = mapped_column(sa.Text, nullable=False)
    posted: Mapped[Optional[datetime]] = mapped_column(sa.DateTime, default=datetime.utcnow)
    category: Mapped[Optional[str]] = mapped_column(
        sa.Enum("news", "publication", "tech", "other", name="post_category"),
        default="news",
        nullable=True
    )
    is_active: Mapped[Optional[bool]] = mapped_column(sa.Boolean, default=True)
    author: Mapped[Optional[str]] = mapped_column(sa.String(20), default="Anonymous")

    def __init__(self, **kwargs):
        if "text" in kwargs and "content" not in kwargs:
            kwargs["content"] = kwargs.pop("text")
        super().__init__(**kwargs)

    @property
    def text(self):
        return self.content

    @text.setter
    def text(self, value):
        self.content = value

    def __repr__(self) -> str:
        return f"<Post(title={self.title})>"