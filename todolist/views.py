import json

from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
from .models import List


def todolist(request):
    current_user = request.user
    do_list = List.objects.filter(author_id__exact=current_user.id)
    data = ''
    if len(do_list) == 0:
        pass
    else:
        data = do_list.get(author_id__exact=current_user.id).text
    return render(request, 'todolist/index.html', {'content': data})


def save(request):
    raw = request.read()
    current_user = request.user
    if current_user.is_authenticated:
        data = json.loads(raw)
        list_content = data.get('content', '')
        one_list = List.objects.filter(author_id__exact=current_user.id)
        if len(one_list) == 0:
            list = List(text=list_content, author=current_user)
            list.save()
        else:
            one_list.update(text=list_content)
        responsedata = {
            'code': 200
        }
        return HttpResponse(json.dumps(responsedata), content_type="application/json")
    else:
        return render(request, 'todolist/index.html')
