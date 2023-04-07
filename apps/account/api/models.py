from conf.database import Base, metadata, engine
from sqlalchemy import Table

class User(Base):
    """
    Connection to User
    """

    __table__ = Table("account_user", metadata, autoload_with=engine)



