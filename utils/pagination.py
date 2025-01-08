from rest_framework.pagination import LimitOffsetPagination

class PageNumberAsLimitOffset(LimitOffsetPagination):
    limit_query_param = "pageSize"
    offset_query_param = "pageNumber"