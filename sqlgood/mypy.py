import os
from configparser import ConfigParser
from functools import partial
from mypy.plugin import Plugin, MethodSigContext, CheckerPluginInterface
from mypy.types import CallableType, Type, TypedDictType, Instance, TupleType
from mypy.nodes import TypeInfo, SymbolTable, ClassDef, Block
from mypy.mro import calculate_mro
from mypy.options import Options
from typing import Any, List, Tuple, Optional, Dict, Set

from sqlgood.parse_sqlite import get_db_schema_text
from sqlgood.parse_sqlite import parse_query_types
from sqlgood.parse_sqlite import parse_schema
from sqlgood.parse_sqlite import ParsedSchema
from sqlgood.parse_sqlite import ParsedQueryTypes
from sqlgood.parse_sqlite import ParsedField

CONFIGFILE_KEY = 'sqlgood-mypy'


def _sql_outputs_to_return_typed_dict(outputs: List[ParsedField], api: CheckerPluginInterface) -> TypedDictType:
    int_type = api.named_generic_type('builtins.int', [])
    str_type = api.named_generic_type('builtins.str', [])
    bool_type = api.named_generic_type('builtins.bool', [])
    dict_type = api.named_generic_type('builtins.dict', [])
    items: Dict[str, Instance] = dict()
    required_keys: Set[str] = set()
    for field in outputs:
        name = field['name']
        typ = field['type']
        if typ == 'int':
            instance = Instance(int_type.type, [])
        elif typ == 'str':
            instance = Instance(str_type.type, [])
        elif typ == 'bool':
            instance = Instance(bool_type.type, [])
        else:
            raise ValueError(f'Invalid type {typ}')
        items[name] = instance
        required_keys.add(name)
    return TypedDictType(items, required_keys, dict_type)


def _sql_inputs_to_arg_tuple(inputs: List[ParsedField], api: CheckerPluginInterface) -> TupleType:
    pass


def sqlite_hook(schema_text: Optional[str], ctx: MethodSigContext) -> Type:
    if schema_text is None:
        ctx.api.fail(
            f'Invalid SQLGood configuration. ' + \
            f'Make sure to add a \'[{CONFIGFILE_KEY}]\' section to the \'mypy.ini\' config file, ' + \
            f'with a field \'sqlite_database_filename=...\'',
            ctx.context)
        return ctx.default_signature
    sql = ctx.args[0][0].value
    try:
        schema = parse_schema(schema_text)
    except ValueError as e:
        ctx.api.fail('Failed to parse database schema: ' + str(e), ctx.context)
        return ctx.default_signature

    try:
        inputs, outputs = parse_query_types(sql, schema_text)
    except ValueError as e:
        ctx.api.fail('Failed to parse SQL query: ' + str(e), ctx.context)
        return ctx.default_signature

    new_ret_type = ctx.api.named_generic_type(
        'builtins.list',
        [
            _sql_outputs_to_return_typed_dict(outputs, ctx.api)
        ]
    )
    return CallableType(
        arg_types=ctx.default_signature.arg_types,
        arg_kinds=ctx.default_signature.arg_kinds,
        arg_names=ctx.default_signature.arg_names,
        ret_type=new_ret_type,
        #ret_type=ctx.default_signature.ret_type,
        fallback=ctx.default_signature.fallback
    )


class SQLGoodPluginConfig:
    __slots__ = ('sqlite_database_filename',)
    sqlite_database_filename: Optional[str]

    def __init__(self, options: Options) -> None:
        self.sqlite_database_filename = None
        if options.config_file is None:
            return
        plugin_config = ConfigParser()
        plugin_config.read(options.config_file)
        if CONFIGFILE_KEY not in plugin_config:
            return
        for key in self.__slots__:
            if key in plugin_config[CONFIGFILE_KEY]:
                setting = plugin_config[CONFIGFILE_KEY][key]
                setattr(self, key, setting)


class SQLGoodPlugin(Plugin):
    def __init__(self, options: Options) -> None:
        self.plugin_config = SQLGoodPluginConfig(options)
        if self.plugin_config.sqlite_database_filename is None:
            self.schema_text = None
        else:
            self.schema_text = get_db_schema_text(self.plugin_config.sqlite_database_filename)
        super().__init__(options)

    def get_method_signature_hook(self, fullname: str):
        if fullname == 'sqlgood.sqlite.SQLiteDatabase.query':
            return partial(sqlite_hook, self.schema_text)
        return None


def plugin(version: str):
    return SQLGoodPlugin

