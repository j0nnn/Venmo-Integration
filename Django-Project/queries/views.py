from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpResponse, HttpResponseRedirect
# from django.template import loader
from django.urls import reverse

from .venmo import *
from .models import Transaction, Query
# from django.views import generic

# Create your views here.
# class IndexView(generic.ListView):

def index(request):
    template_name = 'queries/index.html'
    # template = loader.get_template('polls/index.html')

    queries = Query.objects.all()
    context = {
        'queries': queries,
    }

    return render(request, template_name, context)

def detail(request, query_id):
    template_name = 'queries/detail.html'

    q = get_object_or_404(Query, pk=query_id)
    queries = Query.objects.all()
    context = {
        'queries': queries,
        'query': q,
    }
    print(request)
    return render(request, template_name, context)

def create(request):
    template_name = 'queries/create.html'

    queries = Query.objects.all()
    context = {
        'queries': queries,
    }
    return render(request, template_name, context)


def inp(request):
    start_date = request.POST['start_date']
    end_date = request.POST['end_date']
    keyword = request.POST['keyword']

    # print(start_date, type(start_date))
    # print(end_date, type(end_date))
    # print(keyword, type(keyword))

    q = Query(dateStart=start_date, dateEnd=end_date, keyword=keyword)
    q.save()

    transaction_array = transaction_search(start_date, end_date, keyword)
    # print(transaction_array)
    for trans in transaction_array:
        # [t_date.strftime("%m/%d/%Y"), t.note, t.actor.display_name, t.amount, t.actor.username]
        t = Transaction(query=q, trans_name=trans[2], trans_date=trans[0], trans_comment=trans[1], trans_amount=trans[3])
        t.save()

    return HttpResponseRedirect(reverse('queries:detail', args=(q.id,)))
