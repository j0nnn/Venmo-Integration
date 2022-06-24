from django.contrib import admin
from .models import Query, Transaction

# Register your models here.
# admin.site.register(Query)
# admin.site.register(Transaction)

class TransactionInline(admin.TabularInline):
    model = Transaction
    # extra = 3

class QueryAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Query Info', {'fields': ['keyword', 'dateStart', 'dateEnd']}),
    ]
    inlines = [TransactionInline]

    list_display = ('__str__', 'keyword', 'queryDate')
    list_filter = ['queryDate']
    search_fields = ['keyword']

admin.site.register(Query, QueryAdmin)
