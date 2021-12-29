from django.shortcuts import render, get_object_or_404
from django.http import Http404
from .models import Query
from .forms import QueryForm

# Create your views here.
def query_view(request, id):
    obj = Query.objects.get(id=id)
    context = {
        'object': obj
    }
    return render(request, 'queries/query_view.html', context)

def query_create_view(request):
    id = Query.objects.count()
    if id > 0:
        obj = Query.objects.get(id=id) # get_object_or_404(Query, id)
    else:
        obj = None

    form = QueryForm(request.POST or None)
    if form.is_valid():
        form.save()
        form = QueryForm()
        obj = Query.objects.get(id=id+1)

    context = {
        'form': form,
        'object': obj
    }
    return render(request, 'queries/query_create.html', context)
