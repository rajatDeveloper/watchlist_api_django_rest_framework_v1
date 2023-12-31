from rest_framework.pagination import PageNumberPagination  , LimitOffsetPagination , CursorPagination

class WatchListPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'size'
    max_page_size = 10
    page_query_param = 'p'
    
    
class WatchListLOPagination(LimitOffsetPagination):
    default_limit = 5
    
    max_limit = 10    
    
class WatchListCPagination(CursorPagination):
    page_size = 2
    ordering = 'created'    