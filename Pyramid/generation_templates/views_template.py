from file_paths import PYRAMID_VIEWS_PATH

TOTAL_VIEWS_TEMPLATE = """from pyramid.response import Response
from pyramid.view import view_config

{{ views }}
"""

VIEW_TEMPLATE = """
@view_config(route_name='{{ route_name }}', renderer='json')
def {{ route_name }}(request):
    return {'name': 'Hello View'}

"""


def generate_complete_views_file(filled_views_template):
    total_views_str = TOTAL_VIEWS_TEMPLATE.replace('{{ views }}',
                                                   filled_views_template)

    with open(PYRAMID_VIEWS_PATH, 'w') as f:
        f.write(total_views_str)


def get_filled_view_template(view_name):
    base_tmpl = VIEW_TEMPLATE
    base_tmpl = base_tmpl.replace('{{ route_name }}', view_name)

    return base_tmpl
