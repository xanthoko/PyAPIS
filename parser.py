import argparse

from prance import ResolvingParser

from Django.django_generator import DjangoGenerator, create_django_project
from FastAPI.fastapi_parser import FastAPIGenerator, create_fastapi_project


def get_command_line_arguments():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('input_path', help='The path of the OpenAPI yml')
    arg_parser.add_argument('framework', help='The framework to create the API')

    args = arg_parser.parse_args()
    return args.framework, args.input_path


def validate_arguments(framework, yml_path):
    supported_frameworks = ['django', 'fastapi']
    if framework not in supported_frameworks:
        print(f'[ERROR] "{framework}" is not a supported framework')
        exit()

    if not yml_path.endswith('.yml'):
        print('[ERROR] OpenAPI input file must be yml')
        exit()


def generate_django_API(yml_parser):
    create_django_project()
    print('[INFO] Django project created')

    dg = DjangoGenerator(yml_parser.specification)
    dg.parse_endpoints()
    print('[INFO] Djang API generated')


def generate_fastapi_API(yml_parser):
    create_fastapi_project()
    print('[INFO] FastAPI project created')

    fg = FastAPIGenerator(yml_parser.specification)
    fg.parse_endpoints()
    print('[INFO] FastAPI API generated')


if __name__ == '__main__':
    framework, yml_path = get_command_line_arguments()
    validate_arguments(framework, yml_path)

    yml_parser = ResolvingParser(yml_path)

    if framework == 'django':
        generate_django_API(yml_parser)
    elif framework == 'fastapi':
        generate_fastapi_API(yml_parser)
