from drf_yasg import openapi

openai_library_param = openapi.Parameter('library', openapi.IN_QUERY, description="Library to use",
                                               type=openapi.TYPE_STRING, enum=['openai', 'deep_seek'], required=True)