from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.views import generic

from .models import Question, Choice

from django.utils import timezone

# Create your views here.
# each view is responsible for doing one of two things:
# 1. returning an HttpResponse object containing the content for the requested page
# 2. raising an exception such as Http404
"""
def index(request):
    
    # latest_question_list = Question.objects.order_by("-pub_date")[:5]
    # # loads the template called polls/index.html and passes it a context
    # template = loader.get_template("polls/index.html")
    # context = {
    #     "latest_question_list": latest_question_list,
    # }
    # # output = ", ".join([q.question_text for q in latest_question_list])
    # return HttpResponse(template.render(context, request))
    
    # shortcut: render()
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = {
        "latest_question_list": latest_question_list,
    }
    # render() takes the request object as its first argument, a template name as its second argument and a dictionary as its optional third argument
    # when rendering a template use render() and HttpResponse() for stub views requests
    return render(request, "polls/index.html", context)

def detail(request, question_id):
    # try:
    #     question = Question.objects.get(pk=question_id)
    # except:
    #     raise Http404("Question does not exist")
    # return render(request, "polls/detail.html", {"question": question})

    # shortcut: get_object_or_404()
    # get_object_or_404() takes a Django model as its first argument and an arbitrary number of keyword arguments, which it passes to the get() function of the model's manager
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/detail.html", {"question": question})

def results(request, question_id):
    # response = f"You're looking at the results of question {question_id}"
    # return HttpResponse(response)
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html", {"question": question})
"""

# Update to use generic views
# each generic views need to know what model it will be action upon
class IndexViews(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        # Return the last five published questions.
        # return Question.objects.order_by("-pub_date")[:5]
        """
        Return the last five published questions (not including those set to be published on the future)
        """
        return Question.objects.filter(pub_date__lte = timezone.now()).order_by("-pub_date")[:5]
    

class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

    # even though future questions have been excluded, users can still reach them if they know or guess the right url
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet
        """
        return Question.objects.filter(pub_date__lte = timezone.now())

class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"

    # def get_queryset(self):
    #     """
    #     Excludes any questions that aren't published yet
    #     """
    #     return Question.objects.filter(pub_date__lte = timezone.now())

def vote(request, question_id):
    # return HttpResponse(f"You're voting on question {question_id}")
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except(KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing with POST data.
        # This prevents data from being posted twice if a user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))