from collections import Counter

from django.shortcuts import render_to_response

# Для отладки механизма ab-тестирования используйте эти счетчики
# в качестве хранилища количества показов и количества переходов.
# но помните, что в реальных проектах так не стоит делать
# так как при перезапуске приложения они обнулятся
counter_show = Counter(test=0, orig=0)
counter_click = Counter(test=0, orig=0)


def index(request):
    # Реализуйте логику подсчета количества переходов с лендига по GET параметру from-landing
    if request.GET.get('from-landing') == 'original':
        counter_click['orig'] += 1
    if request.GET.get('from-landing') == 'test':
        counter_click['test'] += 1
    return render_to_response('index.html')


def landing(request):
    # Реализуйте дополнительное отображение по шаблону app/landing_alternate.html
    # в зависимости от GET параметра ab-test-arg
    # который может принимать значения original и test
    # Так же реализуйте логику подсчета количества показов
    page = request.GET.get('ab-test-arg')
    if page == 'test':
        template = 'landing_alternate.html'
        counter_show['test'] += 1
    else:
        template = 'landing.html'
        counter_show['orig'] += 1
    return render_to_response(template)


def stats(request):
    # Реализуйте логику подсчета отношения количества переходов к количеству показов страницы
    # Для вывода результат передайте в следующем формате:
    try:
        test_conv = counter_click['test'] / counter_show['test']
    except ZeroDivisionError:
        test_conv = 0
    try:
        orig_conv = counter_click['orig'] / counter_show['orig']
    except ZeroDivisionError:
        orig_conv = 0
    return render_to_response('stats.html', context={
        'test_conversion': test_conv,
        'original_conversion': orig_conv,
    })
