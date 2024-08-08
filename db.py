from sqlalchemy import create_engine

import config

engine = create_engine(
    url=config.DB_CONN_URL,
    echo=config.DB_ECHO,
)