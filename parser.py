from prance import ResolvingParser
from Django.django_parser import DjangoCreator

parser = ResolvingParser('test_simple.yml')

dc = DjangoCreator(parser.specification)
dc.parse_endpoints()
