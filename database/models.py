from sqlalchemy import Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column, DeclarativeBase
from sqlalchemy.sql import func

class Base(DeclarativeBase):
    """
    A classe Base herda de declarativeBase e
    permite a bases que herdarem dela, servirem como abstração
    para tabelas no banco de dados.
    """
    pass

class User_db(Base):
    """
    PARAMETERS:
    fist_name:,
    last_name:,
    user_age:,
    user_mail:,
    password
    """
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    first_name: Mapped[str] = mapped_column(String)
    last_name: Mapped[str] = mapped_column(String)
    user_age: Mapped[int] = mapped_column(Integer)
    user_mail: Mapped[str] = mapped_column(String, unique=True)
    password_hash: Mapped[str] = mapped_column(String)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime, 
        server_default=func.now()
        )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime, 
        server_default=func.now(), 
        onupdate=func.now()
        )

    devices = relationship(
        "DeviceTable", 
        back_populates="user"
        )


class DeviceTable(Base):
    """
    -> PARAMETERS <-
    model,
    name,
    username,
    primaryOwnerName,
    machine_id,
    """
    __tablename__ = "devices"
    
    model: Mapped[str] = mapped_column(String)
    name: Mapped[str] = mapped_column(String)
    username: Mapped[str] = mapped_column(String)
    primaryOwnerName: Mapped[str] = mapped_column(String)
    machine_id = mapped_column(String ,primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )
    user: Mapped["User_db"] = relationship(
        back_populates="devices"
    )
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())