import sqlalchemy as sa

meta = sa.MetaData()

SystemSettings = sa.Table(
    'system_settings', meta,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('name', sa.String, nullable=False, unique=True),
    sa.Column('value', sa.String, nullable=False)
)
User = sa.Table(
    'user', meta,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('login', sa.String, nullable=False, unique=True),
    sa.Column('password', sa.String, nullable=False),
    sa.Column('first_name', sa.String, nullable=True),
    sa.Column('last_name', sa.String, nullable=True),
    sa.Column('email', sa.String, nullable=True)
)

_models = {
    'system_settings': SystemSettings,
    'user': User,
}


def get_model_by_name(name: str) -> sa.Table:
    return _models.get(name, None)