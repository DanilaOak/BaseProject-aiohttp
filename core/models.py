import sqlalchemy as sa

meta = sa.MetaData()

SystemSettings = sa.Table(
    'system_settings', meta,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('name', sa.String, nullable=False, unique=True),
    sa.Column('value', sa.String, nullable=False)
)

_models = {'system_settings': SystemSettings}


def get_model_by_name(name: str) -> sa.Table:
    return _models.get(name, None)