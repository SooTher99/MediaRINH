from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Column, INT, ForeignKey

from conf.database import Base, metadata, engine
from typing import List
from sqlalchemy import Table
import sqlalchemy

class User(Base):
    """
    Connection to User
    """

    # __table__ = Table("account_user", metadata)
    __tablename__ = "account_user"
    id = Column(INT, primary_key=True)
    children: Mapped[List["UsersChannelModel"]] = relationship()


class ChannelsModel(Base):
    __tablename__ = "channel_channelsmodel"
    id = Column(INT, primary_key=True)
    children: Mapped[List["UsersChannelModel"]] = relationship()

class UsersChannelModel(Base):
    __tablename__ = 'channel_userschannelmodel'
    id = Column(INT, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("account_user.id"))
    channel_id: Mapped[int] = mapped_column(ForeignKey("channel_channelsmodel.id"))
    # user_id = sqlalchemy.ForeignKey(column="account_user.id")




