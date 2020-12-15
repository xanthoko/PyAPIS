from Django.generation_templates.url_template import (generate_complete_urls_file,
                                                      get_path_template_with_data)
from Django.generation_templates.view_template import (get_view_template_with_data,
                                                       get_view_name,
                                                       generate_complete_views_file)


class DjangoCreator:
    def __init__(self, parsed_dict):
        self.parsed_dict = parsed_dict

        self.all_views_template = ''
        self.all_paths_template = ''

    def parse_endpoints(self):
        base_path = self.parsed_dict.get('basePath', '')
        endpoints_dict = self.parsed_dict.get('paths', {})

        for ind, (path, endpoint_data) in enumerate(endpoints_dict.items()):
            full_path = base_path + path
            full_path = full_path[1:]  # remove the first /

            view_name = get_view_name(ind)
            view_details = self._get_view_details(endpoint_data)

            self._append_view_to_template(ind, view_details)
            self._append_path_to_template(full_path, view_name)

        self._finilize_views_template()
        self._finilize_urls_template()

    def _append_path_to_template(self, path, view_name):
        path_str = get_path_template_with_data(path, view_name)
        self.all_paths_template += path_str

    def _finilize_urls_template(self):
        self.all_paths_template = self.all_paths_template[:-1]  # remove the last \n
        generate_complete_urls_file(self.all_paths_template)

    def _get_view_details(self, endpoint_data):
        for method, view_data in endpoint_data.items():
            parameters = view_data.get('parameters', [])
            path_parameters = [x['name'] for x in parameters if x['in'] == 'path']
            body_parameters = [x['name'] for x in parameters if x['in'] == 'body']

        return {
            'path_parameters': path_parameters,
            'body_parameters': body_parameters
        }

    def _append_view_to_template(self, view_index, view_details):
        view_str = get_view_template_with_data(view_index, view_details)
        self.all_views_template += view_str

    def _finilize_views_template(self):
        # remove the last 2 \n
        self.all_views_template = self.all_views_template[:-2]
        generate_complete_views_file(self.all_views_template)
