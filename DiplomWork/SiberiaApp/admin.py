from django.contrib import admin

from .models import Person
from .models import History

admin.site.register(Person)
admin.site.register(History)
