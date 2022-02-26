import json

from django.core.paginator import Paginator
from django.db.models import Count, Q, F
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView

from HW import settings
from users.models import User, Location


class UserListView(View):

    def get(self, request):

        user_qs = User.objects.annotate(adverts=Count('advert', filter=Q(advert__is_published=True))).order_by('username')

        paginator = Paginator(user_qs, settings.TOTAL_ON_PAGE)
        page_number = request.GET.get('page')
        page_list = paginator.get_page(page_number)

        users = []
        for user in page_list:
            users.append(
                {'id': user.id,
                 'username': user.username,
                 'first_name': user.first_name,
                 'last_name': user.last_name,
                 'role': user.role,
                 'age': user.age,
                 'locations': list(map(str, user.locations.all())),
                 'adverts': user.adverts
                 }
            )

        response = {'items': users,
                    'num_pages': page_list.paginator.num_pages,
                    'total': page_list.paginator.count}

        return JsonResponse(response, safe=False)


class UserDetailView(DetailView):
    model = User

    def get(self, request, *args, **kwargs):
        user = self.get_object()
        return JsonResponse(
            {'id': user.id,
             'username': user.username,
             'first_name': user.first_name,
             'last_name': user.last_name,
             'role': user.role,
             'age': user.age,
             'locations': list(map(str, user.locations.all())),
             }
        )


@method_decorator(csrf_exempt, name='dispatch')
class UserCreateView(CreateView):
    model = User
    fields = ['username', 'password', 'first_name', 'last_name', 'role', 'age', 'locations', 'lat', 'lng']

    def post(self, request, *args, **kwargs):
        user_data = json.loads(request.body)

        new_user = User.objects.create(
            username=user_data['username'],
            password=user_data['password'],
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            role=user_data['role'],
            age=user_data['age'],
        )

        for location in user_data['locations']:
            location_obj, _ = Location.objects.get_or_create(name=location['name'],
                                                           lat=location['lat'],
                                                           lng=location['lng'])
            new_user.locations.add(location_obj)

        return JsonResponse({
            'id': new_user.id,
            'username': new_user.username,
            'first_name': new_user.first_name,
            'last_name': new_user.last_name,
            'role': new_user.role,
            'age': new_user.age,
            'locations': list(map(str, new_user.locations.all())),
        }, status=201)


@method_decorator(csrf_exempt, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    fields = ['username', 'password', 'first_name', 'last_name', 'age', 'locations']

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        user_data = json.loads(request.body)

        self.object.username = user_data['username']
        self.object.password = user_data['password']
        self.object.first_name = user_data['first_name']
        self.object.last_name = user_data['last_name']
        self.object.age = user_data['age']

        for location in user_data['locations']:
            location_obj, _ = Location.objects.get_or_create(name=location['name'],
                                                           lat=location['lat'],
                                                           lng=location['lng'])
            self.object.locations.add(location_obj)

        self.object.save()

        return JsonResponse({
            'id': self.object.id,
            'username': self.object.username,
            'first_name': self.object.first_name,
            'last_name': self.object.last_name,
            'role': self.object.role,
            'age': self.object.age,
            'locations': list(map(str, self.object.locations.all())),
        }, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class UserDeleteView(DeleteView):
    model = User
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({'status': 'ok'}, status=204)
