from rest_framework.pagination import PageNumberPagination

class DefaultPaginations(PageNumberPagination):
    page_size = 10