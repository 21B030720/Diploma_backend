from drf_yasg import openapi

openai_library_param = openapi.Parameter('library', openapi.IN_QUERY, description="Library to use",
                                         type=openapi.TYPE_STRING, enum=['openai', 'deep_seek'], required=True)

shop_id_param = openapi.Parameter('shop_id',
                                  openapi.IN_QUERY,
                                  description="Filter by shop id",
                                  type=openapi.TYPE_INTEGER)

category_name_param = openapi.Parameter('category_name',
                                        openapi.IN_QUERY,
                                        description="Filter by category name",
                                        type=openapi.TYPE_STRING)

sort_param = openapi.Parameter('sort',
                               openapi.IN_QUERY,
                               description="Sort order",
                               type=openapi.TYPE_STRING)

from_age_param = openapi.Parameter('from_age',
                                   openapi.IN_QUERY,
                                   description="Filter by from_age",
                                   type=openapi.TYPE_INTEGER)

to_age_param = openapi.Parameter('to_age',
                                 openapi.IN_QUERY,
                                 description="Filter by to_age",
                                 type=openapi.TYPE_INTEGER)
