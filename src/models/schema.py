import sys
import traceback
import src.models.sound as sound
import src.models.playlist as playlist
import src.db.pg as pg

# NOTE: we could generate this list dynamically from files in this directory
# but we would have to take dependencies between models into account to put
# them in the right order (or use a numeric prefix in the filename etc.)
models = [
  sound,
  playlist
]

def get_migrate_sql(model, migration_type):
  var_name = f'SCHEMA_{migration_type.upper()}'
  return getattr(model, var_name)

def match_model_name(model, model_name):
  return model.__name__ == model_name or model.__name__ == f'src.models.{model_name}'

MIGRATION_TYPES = ('create', 'drop')

def migrate(migration_type = 'create', model_name = None):
  if not pg.conn:
    pg.connect()
  if not migration_type in MIGRATION_TYPES:
    raise Exception(f'Invalid migration_type={migration_type} - MIGRATION_TYPES={MIGRATION_TYPES}')
  all_models = [model for model in models if get_migrate_sql(model, migration_type)]
  if model_name:
    models_to_migrate = [model for model in all_models if match_model_name(model, model_name)]
  elif migration_type == 'drop_schema':
    # need to drop in reverse create order
    models_to_migrate = list(reversed(all_models))
  else:
    models_to_migrate = all_models
  if len(models_to_migrate) == 0:
    all_model_names = [model.__name__ for model in all_models]
    print(f'models.migrate - found no models to migrate - aborting - available models: {all_model_names}')
    return
  for model in models_to_migrate:    
    log_prefix = f'models.migrate {model.__name__} - {migration_type}'
    try:
        print(log_prefix)
        sql = get_migrate_sql(model, migration_type)
        print(sql)
        pg.execute(sql)
    except:
      error = sys.exc_info()[0]
      print(f'{log_prefix} - error thrown', error)
      traceback.print_exc()
