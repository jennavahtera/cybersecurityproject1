from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Choice, Question
from django.db import transaction

class AllPollsView(LoginRequiredMixin, generic.ListView):
    template_name = 'polls/all_polls.html'
    context_object_name = 'question_list'

    def get_queryset(self):
        """
        Return all published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')

class MyPollsView(LoginRequiredMixin, generic.ListView):
    template_name = 'polls/my_polls.html'
    context_object_name = 'my_question_list'

    def get_queryset(self):
        """
        Return all published questions created by the logged-in user.
        """
        return Question.objects.filter(
            user=self.request.user,
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')

class DetailView(LoginRequiredMixin, generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(LoginRequiredMixin, generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

@login_required
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

@login_required
def create_question(request):
    if request.method == 'POST':
        question_text = request.POST.get('question_text')
        choices = request.POST.getlist('choices[]')

        if question_text and choices and any(choice.strip() for choice in choices):
            with transaction.atomic():
                question = Question.objects.create(
                    question_text=question_text,
                    pub_date=timezone.now(),
                    user=request.user
                )

                for choice_text in choices:
                    choice_text = choice_text.strip()
                    if choice_text:
                        Choice.objects.create(question=question, choice_text=choice_text)

                return redirect('polls:my_polls')

        else:
            return render(request, 'polls/create_question.html', {
                'error_message': 'Please enter a question and at least one choice.'
            })

    return render(request, 'polls/create_question.html')
