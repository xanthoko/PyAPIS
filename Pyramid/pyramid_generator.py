from pathlib import Path

from Pyramid.generation_templates.views_template import (
    get_filled_view_template, generate_complete_views_file)
from Pyramid.generation_templates.init_template import (get_filled_route_template,
                                                        generate_complete_init_file)
from Pyramid.generation_templates.project_templates import (get_dev_ini_str,
                                                            get_setup_str)
from file_paths import (PYRAMID_PROJECT_PATH, PYRAMID_INI_PATH, PYRAMID_SETUP_PATH,
                        PYRAMID_PACKAGE_NAME, PYRAMID_PACKAGE_PATH)


def create_pyramid_project():
    Path(PYRAMID_PROJECT_PATH).mkdir(exist_ok=True)

    with open(PYRAMID_INI_PATH, 'w') as f:
        f.write(get_dev_ini_str(PYRAMID_PACKAGE_NAME))

    with open(PYRAMID_SETUP_PATH, 'w') as f:
        f.write(get_setup_str(PYRAMID_PACKAGE_NAME))

    Path(PYRAMID_PACKAGE_PATH).mkdir(exist_ok=True)


class PyramidGenerator:
    def __init__(self, parsed_dict):
        self.parsed_dict = parsed_dict

        self.total_routes_str = ''
        self.total_views_str = ''

    def parse_endpoints(self):
        base_path = self.parsed_dict.get('basePath', '')
        endpoints_dict = self.parsed_dict.get('paths', {})

        for ind, (path, endpoint_data) in enumerate(endpoints_dict.items()):
            full_path = base_path + path

            view_name = f'base_view_{ind}'
            for method, view_data in endpoint_data.items():
                filled_route_str = get_filled_route_template(view_name, full_path)

            filled_view_str = get_filled_view_template(view_name)

            # NOTE: currently only one method per view supported
            self.total_routes_str += filled_route_str
            self.total_views_str += filled_view_str

        self._finilize_routes_template()
        self._finilize_views_template()

    def _finilize_routes_template(self):
        # remove the last \n
        self.total_routes_str = self.total_routes_str[:-1]
        generate_complete_init_file(self.total_routes_str)

    def _finilize_views_template(self):
        # remove the last 2 \n
        self.total_views_str = self.total_views_str[:-2]
        generate_complete_views_file(self.total_views_str)
