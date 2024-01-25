from django.contrib import admin
from .models import Question, Choice # added choice
# Register your models here.

# admin.site.register(Question)

# update number 1 to QuestionAdmin class
# replace with
# class QuestionAdmin(admin.ModelAdmin):
#     # this change makes the “Publication date” come before the “Question” field
#     fields = ["pub_date", "question_text"]

# add ChoiceInline class
class ChoiceInline(admin.TabularInline): # changed from admin.StackedInline to admin.TabularInline; Django offers a tabular way of displaying inline related objects
    model = Choice # from models.py
    extra = 3 # provide enough fields for 3 choices

# update number 2 to QuestionAdmin class
# split forms into fieldsets
class QuestionAdmin(admin.ModelAdmin):
    # first element of each tuple in fieldsets is the title of the fieldset
    fieldsets = [
        (None, {"fields": ["question_text"]}),
        ("Date information", {"fields": ["pub_date"]}),
    ]
    inlines = [ChoiceInline] # Choice objects are edited on the Question admin page instead of on a separate Choices admin page(when admin.site.register(Choice) is used)

    # update number 3 - customize admin change list
    # add list_display to QuestionAdmin class
    list_display = ["question_text", "pub_date", "was_published_recently"]

    # add list_filter to QuestionAdmin class
    # to support filtering by the pub_date field
    # since admin.display was added in models.py
    list_filter = ["pub_date"]

    # adding search capability
    # add search_fields to QuestionAdmin class
    # adds a search box at the top of the change list
    search_fields = ["question_text"]



# pattern: admin.site.register(<model>, <model>Admin)
# create a model admin class, then pass it as the second argument to admin.site.register()
# any time you need to change the admin options for a model
admin.site.register(Question, QuestionAdmin)

# removed then added ChoiceInline class
# admin.site.register(Choice) # added choice