from django.shortcuts import render
from django.views import generic
# Create your views here.
class IndexView(generic.ListView):

    model = None
    template_name = 'frontpage/index.html'

    id = 0
    context_object_name = 'query_set'

    def get_queryset(self):

        return []
