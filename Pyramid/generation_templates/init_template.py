from file_paths import PYRAMID_INIT_PATH

INIT_TEMPLATE = """from pyramid.config import Configurator


def main(global_config, **settings):
    config = Configurator(settings=settings)
{{ routes }}
    config.scan('.views')
    return config.make_wsgi_app()
"""

ROUTE_TEMPLATE = """    config.add_route('{{ view_name }}', '{{ route_path }}')\n"""


def generate_complete_init_file(filled_routes_template):
    total_init_file = INIT_TEMPLATE.replace('{{ routes }}', filled_routes_template)

    with open(PYRAMID_INIT_PATH, 'w') as f:
        f.write(total_init_file)


def get_filled_route_template(view_name, route_path):
    base_tmpl = ROUTE_TEMPLATE
    base_tmpl = base_tmpl.replace('{{ view_name }}', view_name)
    base_tmpl = base_tmpl.replace('{{ route_path }}', route_path)

    return base_tmpl
