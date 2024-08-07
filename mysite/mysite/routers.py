from learning.models import TablespaceExample, Pizza, Topping


class AppRouter:
    default_db = "default"
    sqlite_db = "sqlite"
    related_models = [TablespaceExample, Pizza, Topping]

    def db_for_read(self, model, **hints):
        if model in self.related_models:
            return self.sqlite_db
        return None

    def db_for_write(self, model, **hints):
        if model in self.related_models:
            return self.sqlite_db
        return None
