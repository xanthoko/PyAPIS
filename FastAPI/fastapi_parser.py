from FastAPI.generation_templates.main_template import (generate_complete_main_file,
                                                        get_view_template_with_data)


class FastAPICreator:
    def __init__(self, parsed_dict):
        self.parsed_dict = parsed_dict

        self.total_views_str = ''

    def parse_endpoints(self):
        base_path = self.parsed_dict.get('basePath', '')
        endpoints_dict = self.parsed_dict.get('paths', {})

        for ind, (path, endpoint_data) in enumerate(endpoints_dict.items()):
            full_path = base_path + path

            # NOTE: currently only one method per view supported
            for method, view_data in endpoint_data.items():
                # NOTE: keep the first response code
                response_code = list(view_data['responses'].keys())[0]
                parameters = view_data.get('parameters', [])
                path_parameters = [{
                    'name': x['name'],
                    'type': x['schema']['type'],
                    'required': x['required']
                } for x in parameters if x['in'] == 'path']
                query_parameters = [{
                    'name': x['name'],
                    'type': x['schema']['type'],
                    'required': x['required']
                } for x in parameters if x['in'] == 'query']
                # body parameters
                # NOTE: we assume the body params are form data
                request_body = view_data.get('requestBody')
                if request_body:
                    schema = request_body['content'][
                        'application/x-www-form-urlencoded']['schema']
                    properties = schema['properties']
                    required_parameters = schema.get('required', [])
                    body_parameters = [{
                        'name': k,
                        'type': v['type'],
                        'required': k in required_parameters
                    } for k, v in properties.items()]
                else:
                    body_parameters = {}

                filled_view_template = get_view_template_with_data(
                    method, full_path, response_code, ind, path_parameters,
                    query_parameters, body_parameters)
                self.total_views_str += filled_view_template

        self._finilize_views_template()

    def _finilize_views_template(self):
        self.total_views_str = self.total_views_str[:-2]
        generate_complete_main_file(self.total_views_str)
