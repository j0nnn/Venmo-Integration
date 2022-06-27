from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpResponse, HttpResponseRedirect
# from django.template import loader
# template = loader.get_template('polls/index.html')
from django.urls import reverse
from django.db.models import Sum

from .venmo import *
from .models import Transaction, Query

# from .__init__ import login_flag
login_flag = False
print("init", login_flag)

# Create your views here.

def login(request):
    global login_flag

    print("Login page", login_flag)
    if login_flag:
        return HttpResponseRedirect(reverse('queries:index'))

    template_name = 'queries/login.html'
    return render(request, template_name)

def cred(request):
    global login_flag

    login_pass = os.getenv("login_pass")
    try:
        if request.POST['pwd'] == login_pass:
            login_flag = True
            return HttpResponseRedirect(reverse('queries:index'))
        else:
            return HttpResponseRedirect(reverse('queries:login'))
    except KeyError:
        return HttpResponseRedirect(reverse('queries:login'))

def logout(request):
    global login_flag
    login_flag = False

    print("Logging out", login_flag)

    return HttpResponseRedirect(reverse('queries:login'))

def index(request):
    global login_flag
    if not login_flag:
        return HttpResponseRedirect(reverse('queries:login'))

    template_name = 'queries/index.html'
    context = {
        'queries': Query.objects.all(),
    }
    return HttpResponseRedirect(reverse('queries:create'))

def detail(request, query_id):
    global login_flag
    if not login_flag:
        return HttpResponseRedirect(reverse('queries:login'))
    print("Detail", login_flag)

    template_name = 'queries/detail.html'
    q = get_object_or_404(Query, pk=query_id)
    context = {
        'queries': Query.objects.all(),
        'query': q,
        'query_sum': round(q.transaction_set.aggregate(Sum('trans_amount'))['trans_amount__sum'], 2),
    }
    return render(request, template_name, context)

def create(request):
    global login_flag
    if not login_flag:
        return HttpResponseRedirect(reverse('queries:login'))
    print("Create", login_flag)

    template_name = 'queries/create.html'
    context = {
        'queries': Query.objects.all(),
    }
    return render(request, template_name, context)

# def loading(request):
#     template_name = 'queries/loading.html'
#
#     queries = Query.objects.all()
#     context = {
#     'queries': queries,
#     }
#     return render(request, template_name, context)

def delete(request, query_id):
    global login_flag
    if not login_flag:
        return HttpResponseRedirect(reverse('queries:login'))

    Query.objects.get(pk=query_id).delete()
    return HttpResponseRedirect(reverse('queries:index'))

def inp(request):
    global login_flag
    if not login_flag:
        return HttpResponseRedirect(reverse('queries:login'))

    start_date = request.POST['start_date']
    end_date = request.POST['end_date']
    keyword = request.POST['keyword']

    ### ASYNC TESTING ###
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
    for trans in transaction_array:
        t = Transaction(query=q, trans_name=trans[2], trans_date=trans[0], trans_comment=trans[1], trans_amount=trans[3])
        t.save()

    return HttpResponseRedirect(reverse('queries:detail', args=(q.id,)))
