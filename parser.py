from prance import ResolvingParser
from Django.django_parser import DjangoCreator

parser = ResolvingParser('test.yml')

dc = DjangoCreator(parser.specification)
dc.parse_endpoints()
