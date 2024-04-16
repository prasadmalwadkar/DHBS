class ModelRouter:
    def db_for_read(self, model, **hints):
        return None

    def db_for_write(self, model, **hints):
        guest_id = hints.get('guest_id', None)
        if guest_id is not None:
            return 'odd' if int(guest_id) % 2 != 0 else 'even'
        return None


    def allow_migrate(self, db, app_label, model_name=None, **hints):
        return True
