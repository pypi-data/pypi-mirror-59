from json import dumps, loads


class GraphQLError(Exception):
    def __init__(self, mutation, error):
        super().__init__(f'Mutation "{mutation}" failed with error: "{error}"')


def format_result(name, result):
    if 'errors' in result:
        raise GraphQLError(name, result['errors'])
    return result['data'][name]


def json_escape(dict):
    str = dumps(dict)
    return dumps(str)[1:-1]


def content_escape(content):
    return content.replace('\\', '\\\\').replace('\n', '\\n').replace('"', '\\"')
