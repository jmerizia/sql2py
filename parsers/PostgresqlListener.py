# Generated from Postgresql.g4 by ANTLR 4.9.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .PostgresqlParser import PostgresqlParser
else:
    from PostgresqlParser import PostgresqlParser

# This class defines a complete listener for a parse tree produced by PostgresqlParser.
class PostgresqlListener(ParseTreeListener):

    # Enter a parse tree produced by PostgresqlParser#queries.
    def enterQueries(self, ctx:PostgresqlParser.QueriesContext):
        pass

    # Exit a parse tree produced by PostgresqlParser#queries.
    def exitQueries(self, ctx:PostgresqlParser.QueriesContext):
        pass


    # Enter a parse tree produced by PostgresqlParser#query.
    def enterQuery(self, ctx:PostgresqlParser.QueryContext):
        pass

    # Exit a parse tree produced by PostgresqlParser#query.
    def exitQuery(self, ctx:PostgresqlParser.QueryContext):
        pass


    # Enter a parse tree produced by PostgresqlParser#create_query.
    def enterCreate_query(self, ctx:PostgresqlParser.Create_queryContext):
        pass

    # Exit a parse tree produced by PostgresqlParser#create_query.
    def exitCreate_query(self, ctx:PostgresqlParser.Create_queryContext):
        pass


    # Enter a parse tree produced by PostgresqlParser#drop_query.
    def enterDrop_query(self, ctx:PostgresqlParser.Drop_queryContext):
        pass

    # Exit a parse tree produced by PostgresqlParser#drop_query.
    def exitDrop_query(self, ctx:PostgresqlParser.Drop_queryContext):
        pass


    # Enter a parse tree produced by PostgresqlParser#select_query.
    def enterSelect_query(self, ctx:PostgresqlParser.Select_queryContext):
        pass

    # Exit a parse tree produced by PostgresqlParser#select_query.
    def exitSelect_query(self, ctx:PostgresqlParser.Select_queryContext):
        pass


    # Enter a parse tree produced by PostgresqlParser#insert_query.
    def enterInsert_query(self, ctx:PostgresqlParser.Insert_queryContext):
        pass

    # Exit a parse tree produced by PostgresqlParser#insert_query.
    def exitInsert_query(self, ctx:PostgresqlParser.Insert_queryContext):
        pass


    # Enter a parse tree produced by PostgresqlParser#delete_query.
    def enterDelete_query(self, ctx:PostgresqlParser.Delete_queryContext):
        pass

    # Exit a parse tree produced by PostgresqlParser#delete_query.
    def exitDelete_query(self, ctx:PostgresqlParser.Delete_queryContext):
        pass


    # Enter a parse tree produced by PostgresqlParser#update_query.
    def enterUpdate_query(self, ctx:PostgresqlParser.Update_queryContext):
        pass

    # Exit a parse tree produced by PostgresqlParser#update_query.
    def exitUpdate_query(self, ctx:PostgresqlParser.Update_queryContext):
        pass


    # Enter a parse tree produced by PostgresqlParser#empty_query.
    def enterEmpty_query(self, ctx:PostgresqlParser.Empty_queryContext):
        pass

    # Exit a parse tree produced by PostgresqlParser#empty_query.
    def exitEmpty_query(self, ctx:PostgresqlParser.Empty_queryContext):
        pass


    # Enter a parse tree produced by PostgresqlParser#column_refs.
    def enterColumn_refs(self, ctx:PostgresqlParser.Column_refsContext):
        pass

    # Exit a parse tree produced by PostgresqlParser#column_refs.
    def exitColumn_refs(self, ctx:PostgresqlParser.Column_refsContext):
        pass


    # Enter a parse tree produced by PostgresqlParser#column_ref.
    def enterColumn_ref(self, ctx:PostgresqlParser.Column_refContext):
        pass

    # Exit a parse tree produced by PostgresqlParser#column_ref.
    def exitColumn_ref(self, ctx:PostgresqlParser.Column_refContext):
        pass


    # Enter a parse tree produced by PostgresqlParser#table_ref.
    def enterTable_ref(self, ctx:PostgresqlParser.Table_refContext):
        pass

    # Exit a parse tree produced by PostgresqlParser#table_ref.
    def exitTable_ref(self, ctx:PostgresqlParser.Table_refContext):
        pass


    # Enter a parse tree produced by PostgresqlParser#column_defs.
    def enterColumn_defs(self, ctx:PostgresqlParser.Column_defsContext):
        pass

    # Exit a parse tree produced by PostgresqlParser#column_defs.
    def exitColumn_defs(self, ctx:PostgresqlParser.Column_defsContext):
        pass


    # Enter a parse tree produced by PostgresqlParser#column_def.
    def enterColumn_def(self, ctx:PostgresqlParser.Column_defContext):
        pass

    # Exit a parse tree produced by PostgresqlParser#column_def.
    def exitColumn_def(self, ctx:PostgresqlParser.Column_defContext):
        pass


    # Enter a parse tree produced by PostgresqlParser#column_values.
    def enterColumn_values(self, ctx:PostgresqlParser.Column_valuesContext):
        pass

    # Exit a parse tree produced by PostgresqlParser#column_values.
    def exitColumn_values(self, ctx:PostgresqlParser.Column_valuesContext):
        pass


    # Enter a parse tree produced by PostgresqlParser#column_type.
    def enterColumn_type(self, ctx:PostgresqlParser.Column_typeContext):
        pass

    # Exit a parse tree produced by PostgresqlParser#column_type.
    def exitColumn_type(self, ctx:PostgresqlParser.Column_typeContext):
        pass


    # Enter a parse tree produced by PostgresqlParser#simple_expr.
    def enterSimple_expr(self, ctx:PostgresqlParser.Simple_exprContext):
        pass

    # Exit a parse tree produced by PostgresqlParser#simple_expr.
    def exitSimple_expr(self, ctx:PostgresqlParser.Simple_exprContext):
        pass


    # Enter a parse tree produced by PostgresqlParser#atom.
    def enterAtom(self, ctx:PostgresqlParser.AtomContext):
        pass

    # Exit a parse tree produced by PostgresqlParser#atom.
    def exitAtom(self, ctx:PostgresqlParser.AtomContext):
        pass


    # Enter a parse tree produced by PostgresqlParser#is_eq.
    def enterIs_eq(self, ctx:PostgresqlParser.Is_eqContext):
        pass

    # Exit a parse tree produced by PostgresqlParser#is_eq.
    def exitIs_eq(self, ctx:PostgresqlParser.Is_eqContext):
        pass


    # Enter a parse tree produced by PostgresqlParser#neq.
    def enterNeq(self, ctx:PostgresqlParser.NeqContext):
        pass

    # Exit a parse tree produced by PostgresqlParser#neq.
    def exitNeq(self, ctx:PostgresqlParser.NeqContext):
        pass


    # Enter a parse tree produced by PostgresqlParser#gt.
    def enterGt(self, ctx:PostgresqlParser.GtContext):
        pass

    # Exit a parse tree produced by PostgresqlParser#gt.
    def exitGt(self, ctx:PostgresqlParser.GtContext):
        pass


    # Enter a parse tree produced by PostgresqlParser#lt.
    def enterLt(self, ctx:PostgresqlParser.LtContext):
        pass

    # Exit a parse tree produced by PostgresqlParser#lt.
    def exitLt(self, ctx:PostgresqlParser.LtContext):
        pass



del PostgresqlParser