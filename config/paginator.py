from rest_framework.pagination import PageNumberPagination, Response


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'per_page'

    def __init__(self, page_size=None):
        if page_size:
            self.page_size = page_size

    def get_paginated_response(self, data):
        return Response({
            'previous': self.get_previous_link(),
            'next': self.get_next_link(),
            'count': self.page.paginator.count,
            'results': data,
            'page_number': self.page.number,
            'per_page': self.page.paginator.per_page,
            'total_pages': self.page.paginator.num_pages,
        })
