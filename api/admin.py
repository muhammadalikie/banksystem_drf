from django.contrib import admin
from . import models
# Register your models here.

@admin.register(models.Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ['owner', 'balance', 'currency']
    ordering = ['owner', 'balance']

@admin.register(models.Transfer)
class TransferAdmin(admin.ModelAdmin):
    list_display = ['from_account_id']

@admin.register(models.Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ["account_id"]