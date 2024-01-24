from django.test import TestCase
"""
python manage.py test polls

django test client
from django.test.utils import setup_test_environment
setup_test_environment()
from django.test import Client
client = Client()
response = client.get("/")
from django.urls import reverse
response = client.get(reverse("polls:index"))
response.status_code
response.content
response.context["latest_question_list"]
"""


# Create your tests here.
import datetime

from django.test import TestCase
from django.utils import timezone

from .models import Question

from django.urls import reverse

class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for question whose pub_date is in the future
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date = time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for question whose pub_date is older than 1 day
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds = 1)
        old_question = Question(pub_date = time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns False for question whose pub_date is within the last day
        """
        time = timezone.now() - datetime.timedelta(hours = 23, minutes = 59, seconds = 59)
        recent_question = Question(pub_date = time)
        self.assertIs(recent_question.was_published_recently(), True)

# testing the views
# we are using the tests to tell a story of admin input and user experience on the site, and checking that at every state and for every new change in the state of the system, the expected results are published
def create_question(question_text, days):
    """
    Create a question with the given 'question_text' and published the given number of 'days' offset to now (negative for questions published in the past, positive for questions that have yet to be published)
    """
    # shortcut function for creating questions
    time = timezone.now() + datetime.timedelta(days = days)
    return Question.objects.create(question_text = question_text, pub_date = time)

class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed
        """
        # does not create any questions but checks for the message "No polls are available."
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context["latest_question_list"], []) # verify that the latest_question_list is empty

    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the index page
        """
        question = create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["latest_question_list"], [question]) # verify that the latest_question_list contains our question

    def test_future_question(self):
        """
        Questions with a pub_date in the future aren't displayed on the index page
        """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context["latest_question_list"], []) # verify that the latest_question_list is empty
        # future question should not be displayed

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions are displayed
        """
        question = create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["latest_question_list"], [question])

    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions
        """
        question1 = create_question(question_text="Past question 1.", days=-30)
        question2 = create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["latest_question_list"], [question2, question1])

class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        the detail view of a question with a pub_date in the future returns a 404 not found
        """
        future_question = create_question(question_text="Future question.", days=5)
        url =reverse("polls:detail", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404) # should return an error code 404

    def test_past_question(self):
        """
        the detail view of a question witha pub_date in the past displays the question's text
        """
        past_question = create_question(question_text="Past Question.", days=-5)
        url =reverse("polls:detail", args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text) # should return the past question's text since it is valid

# testing the results view
class QuestionResultsViewTests(TestCase):
    def test_future_question(self):
        """
        the results view of a question with a pub_date in the future returns a 404 not found
        """
        future_question = create_question(question_text="Future question.", days=5)
        url =reverse("polls:results", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404) # should return an error code 404

    def test_past_question(self):
        """
        the results view of a question witha pub_date in the past displays the question's text
        """
        past_question = create_question(question_text="Past Question.", days=-5)
        url =reverse("polls:results", args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text) # should return the past question's text since it is valid

# testing rules-of-thumb
# 1. A separate TestClass for each model or view
# 2. A separate test method for each set of conditions you want to test
# 3. Test method names that describe their function
        
# test using Selenium to test the way HTML, CSS, and JavaScript render in the browser
# Django includes LiveServerTestCase to facilitate integration with tools like Selenium
        