from Django.file_paths import VIEWS_PATH

VIEWS_FILE_TEMPLATE = """from django.http import JsonResponse

{{ views }}
"""

VIEW_TEMPLATE = """
def basic_view_{{ view_index }}(request{{ path_params }}):
{{ body_params }}
    return JsonResponse({})\n
"""


def generate_complete_views_file(filled_views_template):
    filled_views_file_template = VIEWS_FILE_TEMPLATE.replace(
        '{{ views }}', filled_views_template)

    with open(VIEWS_PATH, 'w') as f:
        f.write(filled_views_file_template)


def get_view_template_with_data(view_index, view_details):
    v_temp = VIEW_TEMPLATE
    v_temp = v_temp.replace('{{ view_index }}', str(view_index))

    path_parameters = [''] + view_details['path_parameters']
    v_temp = _replace_path_parameters(v_temp, path_parameters)

    body_parameters = view_details['body_parameters']
    v_temp = _replace_body_parameters(v_temp, body_parameters)

    return v_temp


def get_view_name(index):
    return f'basic_view_{index}'


def _replace_path_parameters(template_string, parameters):
    str_path_parameters = ', '.join(parameters)
    return template_string.replace('{{ path_params }}', str_path_parameters)


def _replace_body_parameters(template_string, parameters):
    total_body_params_str = ''
    for parameter in parameters:
        body_params_str = f"    {parameter} = request.POST['{parameter}']\n"
        total_body_params_str += body_params_str
    total_body_params_str = total_body_params_str[:-1]

    return template_string.replace('{{ body_params }}', total_body_params_str)
