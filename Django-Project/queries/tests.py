from django.test import TestCase

from django.utils import timezone
from .models import Query, Transaction
# Create your tests here.

class QueryModelTests(TestCase):
    def checkToStr(self):
        q = Query(queryDate=timezone.now(), dateStart='03/01/2022', dateEnd='04/01/2022')
        print(q)

class TransactionModelTests(TestCase):
    def checkToStr(self):
        t = Transaction(q, trans_name="nameeeee", trans_date=timezone.now(), trans_amount=11.11, trans_comment="hiii")
        print(t)
