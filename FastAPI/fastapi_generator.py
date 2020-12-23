from pathlib import Path

from FastAPI.generation_templates.main_template import (generate_complete_main_file,
                                                        get_view_template_with_data)
from file_paths import FASTAPI_PROJECT_PATH


def create_fastapi_project():
    Path(FASTAPI_PROJECT_PATH).mkdir(exist_ok=True)


class FastAPIGenerator:
    def __init__(self, parsed_dict):
        self.parsed_dict = parsed_dict

        self.total_views_str = ''

    def parse_endpoints(self):
        """Parses the endpoints and creates a main.py file in the demo directory.

        For every endpoint, extract its accepted http method, the reponse code
        and the path, query and body parameters and put them in a view_template. The
        total_views_str contains all of the filled view_templates as a string.
        """
        base_path = self.parsed_dict.get('basePath', '')
        endpoints_dict = self.parsed_dict.get('paths', {})

        for ind, (path, endpoint_data) in enumerate(endpoints_dict.items()):
            full_path = base_path + path

            for method, view_data in endpoint_data.items():
                # NOTE: keep the first response code
                response_code = list(view_data['responses'].keys())[0]
                parameters = view_data.get('parameters', [])
                path_parameters = self._get_path_parameters_list(parameters)
                query_parameters = self._get_query_parameters_list(parameters)
                body_parameters = self._get_body_parameters_list(view_data)

                filled_view_template = get_view_template_with_data(
                    method, full_path, response_code, ind, path_parameters,
                    query_parameters, body_parameters)

            # NOTE: currently only one method per view supported
            self.total_views_str += filled_view_template

        self._finilize_views_template()

    def _get_path_parameters_list(self, parameters):
        return [{
            'name': x['name'],
            'type': x['schema']['type'],
            'required': x['required']
        } for x in parameters if x['in'] == 'path']

    def _get_query_parameters_list(self, parameters):
        return [{
            'name': x['name'],
            'type': x['schema']['type'],
            'required': x['required']
        } for x in parameters if x['in'] == 'query']

    def _get_body_parameters_list(self, view_data):
        request_body = view_data.get('requestBody')
        if request_body:
            # NOTE: we assume the body params are form data
            schema = request_body['content']['application/x-www-form-urlencoded'][
                'schema']
            properties = schema['properties']
            required_parameters = schema.get('required', [])
            body_parameters = [{
                'name': name,
                'type': v['type'],
                'required': name in required_parameters
            } for name, v in properties.items()]
        else:
            body_parameters = {}
        return body_parameters

    def _finilize_views_template(self):
        # remove the last 2 \n
        self.total_views_str = self.total_views_str[:-2]
        generate_complete_main_file(self.total_views_str)
