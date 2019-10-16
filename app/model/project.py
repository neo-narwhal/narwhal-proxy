from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import relationship
from sqlalchemy.schema import Sequence

from .. import db


class Project(db.Model):
    __tablename__ = 'project'

    id = Column(INTEGER(10), primary_key=True)
    user_id = Column(ForeignKey('user.id'), nullable=False, index=True)
    container_name = Column(String(191))
    name = Column(String(191), nullable=False)
    description = Column(String(191), nullable=False)
    image_tag = Column(String(191), nullable=False)
    cpu = Column(String(191), nullable=False)
    memory = Column(String(191), nullable=False)
    storage = Column(String(191), nullable=False)
    is_custom = Column(String(191), nullable=False)
    port = Column(String(191))

    user = relationship('User')

    def as_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}