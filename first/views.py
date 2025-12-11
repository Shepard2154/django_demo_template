import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from first.forms import CalcForm
from first.models import CalcHistory


def get_base_context(pagename):
    menu = [
        {'link': '/calc', 'text': 'Калькулятор'},
    ]

    return {
        'sitename': 'Demosite',
        'pagename': pagename,
        'menu': menu,
    }


def main_page(request):
    context = get_base_context('Кто ты воин? Добро пожаловать и пожалуйтесь, пожалуйста!')
    creation_date = datetime.datetime.now()
    context['pages'] = 3
    context['auth'] = 'Andrew'
    context['cr_date'] = creation_date
    context['user'] = request.user
    return render(request, 'index.html', context)


@login_required
def calc(request):
    context = get_base_context("Калькулятор")

    user = request.user

    all_data = CalcHistory.objects.filter(author=user)
    context['history'] = all_data

    if request.method == 'POST':  # Обрабатываем введённые данные
        f = CalcForm(request.POST)
        context['data_sent'] = True
        if f.is_valid():  # данные правильные, работаем с ними
            a = f.data['first']
            b = f.data['second']
            c = int(a) + int(b)
            record = CalcHistory(date=datetime.datetime.now(), first=a, second=b, result=c, author=user)
            record.save()
            context.update({
                'first_value': a,
                'second_value': b,
                'result': c,
                'form': f,
                'history': all_data
            })
        else:
            context['form'] = f
    else:
        f = CalcForm()
        context.update({
            'history': all_data,
            'form': f
        })

    return render(request, 'calc.html', context)
