from django.contrib import admin

from .models import *

admin.site.register(Contact)
admin.site.register(ContactFile)
admin.site.register(ContactNote)

admin.site.register(Deal)
admin.site.register(DealStage)
admin.site.register(DealType)
admin.site.register(DealNote)
admin.site.register(DealFile)

admin.site.register(Ticket)
