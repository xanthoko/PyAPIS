from Django.file_paths import VIEWS_PATH

VIEWS_FILE_TEMPLATE = """from django.http import JsonResponse

{{ views }}
"""

VIEW_TEMPLATE = """
def basic_view_{{ view_index }}(request{{ path_params }}):
    if request.method == '{{ method }}':
{{ body_params }}
        return JsonResponse({}, status={{ response_code }})
    else:
        return JsonResponse({'error': 'Invalid method'}, status=405)\n
"""

REQUIRED_PARAMS_TEMPLATE = """
        try:
{{ params }}
        except KeyError as e:
            return JsonResponse({'error': f'Parameter {e} missing'}, status=400)
"""


def generate_complete_views_file(filled_views_template):
    filled_views_file_template = VIEWS_FILE_TEMPLATE.replace(
        '{{ views }}', filled_views_template)

    with open(VIEWS_PATH, 'w') as f:
        f.write(filled_views_file_template)


def get_view_template_with_data(view_index, method_and_params):
    method = method_and_params['method'].upper()
    response_codes = method_and_params['response_codes']

    v_temp = VIEW_TEMPLATE
    v_temp = v_temp.replace('{{ view_index }}', str(view_index))
    v_temp = v_temp.replace('{{ method }}', method)
    # for now use the first response code
    v_temp = v_temp.replace('{{ response_code }}', response_codes[0])

    path_parameters = [''] + method_and_params['path_parameters']
    v_temp = _replace_path_parameters(v_temp, path_parameters)

    body_parameters = method_and_params['body_parameters']
    v_temp = _replace_body_parameters(v_temp, body_parameters)

    return v_temp


def get_view_name(index):
    return f'basic_view_{index}'


def _replace_path_parameters(template_string, parameters):
    """
    Args:
        template_string (string): The template to fill
        parameters (list of strings): The path parameters
    """
    str_path_parameters = ', '.join(parameters)
    return template_string.replace('{{ path_params }}', str_path_parameters)


def _replace_body_parameters(template_string, parameters):
    """
    Args:
        tempalte_string (string): The template to fill
        parameters (dictionary): Body parameters in the following format.
            {'param': {is_required}(boolean), ...}
    """
    at_least_one_required_param = any(parameters.values())
    if at_least_one_required_param:
        intent = 3
    else:
        intent = 2

    prefix_spaces = _get_prefixed_spaces(intent)

    total_body_params_str = ''
    for param, required in parameters.items():
        if required:
            body_params_str = f"{prefix_spaces}{param} = request.POST['{param}']\n"
        else:
            body_params_str = f"{prefix_spaces}{param} = request.POST.get('{param}')\n"
        total_body_params_str += body_params_str

    total_body_params_str = total_body_params_str[:-1]

    if at_least_one_required_param:
        total_body_params_str = REQUIRED_PARAMS_TEMPLATE.replace(
            '{{ params }}', total_body_params_str)

    return template_string.replace('{{ body_params }}', total_body_params_str)


def _get_prefixed_spaces(number_of_intent):
    return '    ' * number_of_intent
