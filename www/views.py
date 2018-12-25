import json

from django.core.paginator import Paginator
from django.db.models import Max
from django.http import JsonResponse
from django.contrib.auth import authenticate, logout, login
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from osu_cipher.utils import to_int
from www.models import Score, User


@method_decorator(csrf_exempt, name='dispatch')
class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return JsonResponse(data={
                'status': 'ok',
                'user': {
                    'nickname': request.user.username
                }
            })
        return JsonResponse(data={
            'status': 'error',
            'user': None,
        }, status=401)

    def post(self, request):
        if request.user.is_authenticated:
            return JsonResponse(data={
                'status': 'ok',
                'user': {
                    'nickname': request.user.username,
                }
            })

        try:
            data = json.loads(request.body)
        except ValueError:
            return JsonResponse(data={
                'status': 'error',
                'errors': [
                    'Not json. POST body must contain nickname and password.'
                ]
            }, status=400)
        username = data.get('nickname', None)
        password = data.get('password', None)
        user = authenticate(username=username, password=password) \
            if (username is not None and password is not None)\
            else None
        if user is not None:
            login(request, user)
            return JsonResponse(data={
                'status': 'ok',
                'user': {
                    'nickname': user.username,
                },
            })
        else:
            return JsonResponse(data={
                'status': 'error',
                'errors': [
                    'Bad credentials.'
                ]
            }, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class LogoutView(View):
    def post(self, request):
        logout(request)
        return JsonResponse(data={
            'status': 'ok'
        })


@method_decorator(csrf_exempt, name='dispatch')
class RegisterView(View):
    def post(self, request):
        if request.user.is_authenticated:
            return JsonResponse(data={
                'status': 'error',
                'errors': [
                    'Authenticated user cannot register another one.'
                ]
            }, status=403)

        try:
            data = json.loads(request.body)
        except ValueError:
            return JsonResponse(data={
                'status': 'error',
                'errors': [
                    'Not json. POST body must contain nickname and password.'
                ]
            }, status=400)
        username = data.get('nickname', None)
        password = data.get('password', None)
        if username is None or password is None:
            return
        if User.objects.filter(username=username).exists():
            return JsonResponse(data={
                'status': 'error',
                'errors': [
                    'The nickname is already registered.'
                ]
            }, status=400)
        User.objects.create_user(username=username, password=password)
        user = authenticate(username=username, password=password)
        login(request, user)
        return JsonResponse(data={
            'status': 'ok',
            'user': {
                'nickname': user.username,
            }
        })


@method_decorator(csrf_exempt, name='dispatch')
class ScoreView(View):
    DEFAULT_PAGE = 1
    DEFAULT_ON_PAGE = 10

    def get(self, request):
        page_num = request.GET.get('page', self.DEFAULT_PAGE)
        page_num = to_int(page_num, self.DEFAULT_PAGE)
        on_page = request.GET.get('on_page', self.DEFAULT_ON_PAGE)
        on_page = to_int(on_page, self.DEFAULT_ON_PAGE)
        scores = Score.objects.values('user__username')\
            .annotate(userscore=Max('score'))\
            .order_by('-userscore', 'user__username').all()
        p = Paginator(scores, on_page)
        if p.num_pages > page_num:
            page_num = p.num_pages - 1
        page = p.page(page_num)
        start_index = page.start_index()
        return JsonResponse(data={
            'status': 'ok',
            'users': [
                {
                    'place': start_index + i - 1,
                    'score': score['userscore'],
                    'nickname': score['user__username'],
                } for i, score in enumerate(page.object_list)
            ],
            'pages': p.num_pages
        })

    def post(self, request):
        if not request.user.is_authenticated:
            return JsonResponse(data={
                'status': 'error',
                'errors': [
                    'You are not authenticated.'
                ]
            }, status=403)

        try:
            data = json.loads(request.body)
        except ValueError:
            return JsonResponse(data={
                'status': 'error',
                'errors': [
                    'Not json. POST body must contain score.'
                ]
            }, status=400)
        score = data.get('score', None)

        if score:
            newScore = Score(user=request.user, score=score)
            newScore.save()

        return JsonResponse(data={
            'status': 'ok',
        })
