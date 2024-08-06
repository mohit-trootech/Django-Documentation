from django.db.models import Lookup, Field, Transform


@Field.register_lookup
class NotEqual(Lookup):
    lookup_name = "ne"

    def as_sql(self, compiler, connection):
        lhs, lhs_params = self.process_lhs(compiler=compiler, connection=connection)
        rhs, rhs_params = self.process_rhs(compiler=compiler, connection=connection)
        params = lhs_params + rhs_params

        return "%s <> %s" % (lhs, rhs), params


@Field.register_lookup
class AbsoluteValueLessThan(Lookup):
    lookup_name = "lt"

    def as_sql(self, compiler, connection):
        lhs, lhs_params = compiler.compile(self.lhs.lhs)
        rhs, rhs_params = self.process_rhs(compiler, connection)
        params = lhs_params + rhs_params + lhs_params + rhs_params
        return "%s < %s AND %s > -%s" % (lhs, rhs, lhs, rhs), params

@Field.register_lookup
class MySQLNotEqual(NotEqual):
    def as_mysql(self, compiler, connection, **extra_context):
        lhs, lhs_params = self.process_lhs(compiler, connection)
        rhs, rhs_params = self.process_rhs(compiler, connection)
        params = lhs_params + rhs_params
        return "%s != %s" % (lhs, rhs), params
