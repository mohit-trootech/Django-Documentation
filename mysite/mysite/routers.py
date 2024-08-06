from learning.models import TablespaceExample


class AppRouter:
    default_db = "default"
    sqlite_db = "sqlite"
    model = TablespaceExample
    route_app_label = "learning"

    def allow_migration(self, db, app_label, model_name=None, **hints):
        print(db, app_label, model_name, hints)
        if (
            model_name == self.model
            or db == self.sqlite_db
            or app_label == self.route_app_label
        ):
            return self.sqlite_db
        return None
