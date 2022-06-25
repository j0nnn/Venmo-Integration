from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpResponse, HttpResponseRedirect
# from django.template import loader
from django.urls import reverse

from .venmo import *
from .models import Transaction, Query
# from django.views import generic
# import asyncio
# from time import sleep
# from asgiref.sync import sync_to_async

# Create your views here.
# class IndexView(generic.ListView):

def index(request):
    template_name = 'queries/index.html'
    # template = loader.get_template('polls/index.html')

    queries = Query.objects.all()
    context = {
        'queries': queries,
    }

    # return render(request, template_name, context)
    return HttpResponseRedirect(reverse('queries:create'))

def detail(request, query_id):
    template_name = 'queries/detail.html'

    q = get_object_or_404(Query, pk=query_id)
    queries = Query.objects.all()
    context = {
        'queries': queries,
        'query': q,
    }
    # print(request)
    return render(request, template_name, context)

def create(request):
    template_name = 'queries/create.html'

    queries = Query.objects.all()
    context = {
        'queries': queries,
    }
    return render(request, template_name, context)

def loading(request):
    template_name = 'queries/loading.html'

    queries = Query.objects.all()
    context = {
    'queries': queries,
    }
    return render(request, template_name, context)

def delete(request, query_id):
    Query.objects.get(pk=query_id).delete()

    return HttpResponseRedirect(reverse('queries:index'))

def inp(request):
    start_date = request.POST['start_date']
    end_date = request.POST['end_date']
    keyword = request.POST['keyword']
    # print(start_date, type(start_date))
    # print(end_date, type(end_date))
    # print(keyword, type(keyword))

    # response = HttpResponseRedirect(reverse('queries:loading'))

    # loop = asyncio.new_event_loop()
    # loop.create_task(makeQuery(start_date, end_date, keyword))
    # # asyncio.set_event_loop(loop)
    # # async_result = loop.run_until_complete()
    # # loop.close()

    # return HttpResponseRedirect(reverse('queries:loading'))
    return makeQuery(start_date, end_date, keyword)

def makeQuery(start, end, key):
    q = Query(dateStart=start, dateEnd=end, keyword=key)
    q.save()

    transaction_array = transaction_search(start, end, key)
    # print(transaction_array)
    for trans in transaction_array:
        # [t_date.strftime("%m/%d/%Y"), t.note, t.actor.display_name, t.amount, t.actor.username]
        t = Transaction(query=q, trans_name=trans[2], trans_date=trans[0], trans_comment=trans[1], trans_amount=trans[3])
        t.save()

    return HttpResponseRedirect(reverse('queries:detail', args=(q.id,)))
