from django.contrib import admin
from .models import BookSubjectModel, BookModels, BookCategoryModels


class BookModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'offer_price', 'active']
    list_editable = ['price', 'offer_price', 'active']
    list_filter = ['price', 'subject', 'active']


class BookSubjectModelAdmin(admin.ModelAdmin):
    list_display = ['subject_name']
    list_filter = ['subject_name']


admin.site.register(BookModels, BookModelAdmin)
admin.site.register(BookSubjectModel, BookSubjectModelAdmin)
admin.site.register(BookCategoryModels)
