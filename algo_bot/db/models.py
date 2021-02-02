import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, scoped_session, sessionmaker
from sqlalchemy_mixins import AllFeaturesMixin, TimestampsMixin

from algo_bot.clients import finviz_client
from algo_bot.settings import AlgoBotSettings, get_settings

settings: AlgoBotSettings = get_settings()
Base = declarative_base()


class BaseModel(Base, AllFeaturesMixin, TimestampsMixin):
    __table_args__ = {"schema": settings.db_name}
    __abstract__ = True
    id = sa.Column(sa.BIGINT, primary_key=True)


class User(BaseModel):
    __tablename__ = "users"
    email = sa.Column(sa.NVARCHAR(200), nullable=False, unique=True)
    slack = sa.Column(sa.NVARCHAR(200), nullable=False, unique=True)
    first_name = sa.Column(sa.NVARCHAR(100), nullable=False)
    last_name = sa.Column(sa.NVARCHAR(100), nullable=False)
    timezone = sa.Column(sa.NVARCHAR(200), nullable=True)
    screeners = relationship("Screener")


class Screener(BaseModel):
    __tablename__ = "screeners"
    user_id = sa.Column(
        sa.BIGINT, sa.ForeignKey(f"{settings.db_name}.users.id"), nullable=False
    )
    user = relationship("User", back_populates="screeners")
    filters = sa.Column(sa.NVARCHAR(1000), nullable=False)
    name = sa.Column(sa.NVARCHAR(200), nullable=False, unique=True)
    cron = sa.Column(sa.NVARCHAR(100), nullable=True, default="*/5 9-16 * * 1-5")

    def run(self):
        return finviz_client.screener(filters=self.filters.split(","))

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "filters": self.filters,
            "cron": self.cron,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


# DB Connection setup
engine = sa.create_engine(
    f"mysql://{settings.db_username}:{settings.db_password}@{settings.db_host}/{settings.db_name}?charset=utf8mb4"
)
session = scoped_session(sessionmaker(bind=engine, autocommit=True))
# Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
BaseModel.set_session(session)
