import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

import config

engine = create_engine(config.Config.SQLALCHEMY_DATABASE_URI)

Session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()