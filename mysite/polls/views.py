from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import Question



def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))



def login(request):
    if request.method == 'GET':
        form = UserForm(request.GET)
        if form.is_valid():
            _email = form.cleaned_data['Input_Email']
            _password = form.cleaned_data['Input_Password']

            user = authentificate(username = _email, password = _password)


            if user is not None:
                connection = "L'utilisateur existe"
                user.last_login = timezone.now()
                user.save(update_fields=['last_login'])
                request.session['member_id'] = _email
                print(connection)
            else:
                connection = "l'utilisateur n'existe pas"
                print(connection)

    else:
        form = UserForm()

    return render(request, 'polls/login.html', {})
