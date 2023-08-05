# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['graphene_resolver', 'graphene_resolver.types']

package_data = \
{'': ['*']}

install_requires = \
['graphene>=2.1,<3.0',
 'isodate>=0.6,<0.7',
 'lazy-object-proxy>=1.4,<2.0',
 'phrases-case>=0.1.1,<0.2.0']

setup_kwargs = {
    'name': 'graphene-resolver',
    'version': '0.1.5',
    'description': 'Using mongoose-like schema to write apollo-like resolver for graphene.',
    'long_description': '# Graphene resolvers\n\n[![build status](https://github.com/NateScarlet/graphene-resolver/workflows/Python%20package/badge.svg)](https://github.com/NateScarlet/graphene-resolver/actions)\n[![version](https://img.shields.io/pypi/v/graphene-resolver)](https://pypi.org/project/graphene-resolver/)\n![python version](https://img.shields.io/pypi/pyversions/graphene-resolver)\n![wheel](https://img.shields.io/pypi/wheel/graphene-resolver)\n![maintenance](https://img.shields.io/maintenance/yes/2019)\n[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-yellow.svg)](https://conventionalcommits.org)\n\nUsing mongoose-like schema to write apollo-like resolver.\n\n## Install\n\n`pip install graphene-resolver`\n\n## Usage\n\nsimple example:\n\n```python\nimport graphene\nimport graphene_resolver as resolver\n\nclass Foo(resolver.Resolver):\n    schema = {\n        "args": {\n            "key":  \'String!\',\n            "value": \'String!\',\n        },\n        "type": \'String!\',\n    }\n\n    def resolve(self, **kwargs):\n        self.parent # parent field\n        self.info # resolve info\n        self.context # resolve context\n        return kwargs[\'value\']\n\nclass Query(graphene.ObjectType):\n    foo = Foo.as_field()\n```\n\n```graphql\n{\n  foo(key: "k", value: "v")\n}\n```\n\n```json\n{ "foo": "v" }\n```\n\nrelay node:\n\n```python\npets = [dict(\n    id=1,\n    name=\'pet1\',\n    age=1,\n)]\nclass Pet(resolver.Resolver):\n    schema = {\n        \'type\': {\n            \'name\': \'String\',\n            \'age\': \'Int\',\n        },\n        \'interfaces\': (graphene.Node,)\n    }\n\n    def get_node(self, id_):\n        return next(i for i in pets if i[\'id\'] == int(id_))\n\n    def validate(self, value):\n        return (\n            isinstance(value, typing.Mapping)\n            and isinstance(value.get(\'name\'), str)\n            and isinstance(value.get(\'age\'), int)\n        )\nclass Query(graphene.ObjectType):\n    node = graphene.Node.Field()\n\nschema = graphene.Schema(query=Query, types=[Pet.as_type()])\n```\n\n```graphql\n{\n  node(id: "UGV0OjE=") {\n    id\n    __typename\n    ... on Pet {\n      name\n      age\n    }\n  }\n}\n```\n\n```json\n{ "node": { "id": "UGV0OjE=", "__typename": "Pet", "name": "pet1", "age": 1 } }\n```\n\nrelay connection:\n\n```python\nclass Item(resolver.Resolver):\n    schema = {\'name\': \'String!\'}\n\nclass Items(resolver.Resolver):\n    schema = resolver.connection.get_type(Item)\n\n    def resolve(self, **kwargs):\n        return resolver.connection.resolve([{\'name\': \'a\'}, {\'name\': \'b\'}], **kwargs)\n```\n\n```graphql\n{\n  items {\n    edges {\n      node {\n        name\n      }\n      cursor\n    }\n    pageInfo {\n      total\n      hasNextPage\n      hasPreviousPage\n      startCursor\n      endCursor\n    }\n  }\n}\n```\n\n```json\n{\n  "items": {\n    "edges": [\n      { "node": { "name": "a" }, "cursor": "YXJyYXljb25uZWN0aW9uOjA=" },\n      { "node": { "name": "b" }, "cursor": "YXJyYXljb25uZWN0aW9uOjE=" }\n    ],\n    "pageInfo": {\n      "total": 2,\n      "hasNextPage": false,\n      "hasPreviousPage": false,\n      "startCursor": "YXJyYXljb25uZWN0aW9uOjA=",\n      "endCursor": "YXJyYXljb25uZWN0aW9uOjE="\n    }\n  }\n}\n```\n\nenum:\n\n```python\n\n    class Foo(resolver.Resolver):\n        schema = (\'a\', \'b\')\n\n        def resolve(self, **kwargs):\n            return \'a\'\n\n    class Query(graphene.ObjectType):\n        foo = Foo.as_field()\n\n    schema = graphene.Schema(query=Query)\n    assert str(schema) == \'\'\'\\\nschema {\n  query: Query\n}\n\nenum Foo {\n  a\n  b\n}\n\ntype Query {\n  foo: Foo\n}\n\'\'\'\n```\n\nenum with description:\n\n```python\n\n    class Foo(resolver.Resolver):\n        schema = {\n            \'type\': [(\'a\', \'this is a\'), (\'b\', \'this is b\'), \'c\'],\n            \'description\': \'A enum\',\n        }\n\n        def resolve(self, **kwargs):\n            return \'a\'\n\n    class Query(graphene.ObjectType):\n        foo = Foo.as_field()\n\n    schema = graphene.Schema(query=Query)\n    enum_type = schema.get_type(\'Foo\')\n    assert enum_type.description == \'A enum\'\n    assert enum_type.get_value(\'a\').value == \'a\'\n    assert enum_type.get_value(\'a\').description == \'this is a\'\n    assert enum_type.get_value(\'b\').value == \'b\'\n    assert enum_type.get_value(\'b\').description == \'this is b\'\n    assert enum_type.get_value(\'c\').value == \'c\'\n    assert enum_type.get_value(\'c\').description is None\n```\n\nunion:\n\n```python\n    class Foo(resolver.Resolver):\n        schema = ({\'a\': \'String\'}, {\'b\': \'Int\'})\n\n        def resolve(self, **kwargs):\n            return {\'__typename\': \'Foo0\', \'a\': \'a\'}\n\n    class Query(graphene.ObjectType):\n        foo = Foo.as_field()\n\n    schema = graphene.Schema(query=Query)\n    assert str(schema) == \'\'\'\\\nschema {\n  query: Query\n}\n\nunion Foo = Foo0 | Foo1\n\ntype Foo0 {\n  a: String\n}\n\ntype Foo1 {\n  b: Int\n}\n\ntype Query {\n  foo: Foo\n}\n\'\'\'\n```\n\n```graphql\n{\n  foo {\n    __typename\n    ... on Foo0 {\n      a\n    }\n  }\n}\n```\n\n```json\n{ "foo": { "__typename": "Foo0", "a": "a" } }\n```\n\ncomplicated example:\n\n```python\nclass Foo(resolver.Resolver):\n    _input_schema = {\n        "type": {"type": \'String\'},\n        "data": [\n            {\n                "type":\n                {\n                    "key": {\n                        "type": \'String\',\n                        "required": True,\n                        "description": "<description>",\n                    },\n                    "value": \'Int\',\n                    "extra": {\n                        "type": [\'String!\'],\n                        "deprecation_reason": "<deprecated>"\n                    },\n                },\n                "required": True\n            },\n        ],\n    }\n    schema = {\n        "args": {\n            "input": _input_schema\n        },\n        "type": _input_schema,\n        "description": "description",\n        "deprecation_reason": None\n    }\n\n    def resolve(self, **kwargs):\n        return kwargs[\'input\']\n```\n\n```graphql\n{\n  foo(\n    input: { type: "type", data: [{ key: "key", value: 42, extra: ["extra"] }] }\n  ) {\n    type\n    data {\n      key\n      value\n      extra\n    }\n  }\n}\n```\n\n```json\n{\n  "foo": {\n    "type": "type",\n    "data": [{ "key": "key", "value": 42, "extra": ["extra"] }]\n  }\n}\n```\n',
    'author': 'NateScarlet',
    'author_email': 'NateScarlet@Gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/NateScarlet/graphene-resolver',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
