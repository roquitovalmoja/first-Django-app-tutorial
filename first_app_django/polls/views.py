from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.template import loader
from .models import Question

# Create your views here.
# each view is responsible for doing one of two things:
# 1. returning an HttpResponse object containing the content for the requested page
# 2. raising an exception such as Http404
def index(request):
    """
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    # loads the template called polls/index.html and passes it a context
    template = loader.get_template("polls/index.html")
    context = {
        "latest_question_list": latest_question_list,
    }
    # output = ", ".join([q.question_text for q in latest_question_list])
    return HttpResponse(template.render(context, request))
    """
    # shortcut: render()
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = {
        "latest_question_list": latest_question_list,
    }
    # render() takes the request object as its first argument, a template name as its second argument and a dictionary as its optional third argument
    # when rendering a template use render() and HttpResponse() for stub views requests
    return render(request, "polls/index.html", context)

def detail(request, question_id):
    """
    try:
        question = Question.objects.get(pk=question_id)
    except:
        raise Http404("Question does not exist")
    return render(request, "polls/detail.html", {"question": question})
    """

    # shortcut: get_object_or_404()
    # get_object_or_404() takes a Django model as its first argument and an arbitrary number of keyword arguments, which it passes to the get() function of the model's manager
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/detail.html", {"question": question})

def results(request, question_id):
    response = f"You're looking at the results of question {question_id}"
    return HttpResponse(response)

def vote(request, question_id):
    return HttpResponse(f"You're voting on question {question_id}")
