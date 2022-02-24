import json

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from HW import settings
from ads.models import Advert
from users.models import User, Location


class UserListView(ListView):
    model = User

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        self.object_list.order_by('username')

        paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
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
                 'location': user.location_id.name,
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
             'location': user.location_id.name,
             }
        )


@method_decorator(csrf_exempt, name='dispatch')
class UserCreateView(CreateView):
    model = User
    fields = ['username', 'password', 'first_name', 'last_name', 'role', 'age', 'location_name', 'lat', 'lng']

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

        if user_data['location_name'] and user_data['lat'] and user_data['lng']:
            new_user.location_id = Location.objects.create(name=user_data['location_name'],
                                                           lat=user_data['lat'],
                                                           lng=user_data['lng']).id

        return JsonResponse({
            'id': new_user.id,
            'username': new_user.username,
            'first_name': new_user.first_name,
            'last_name': new_user.last_name,
            'role': new_user.role,
            'age': new_user.age,
            'location': new_user.location_id.name,
        }, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    fields = ['username', 'password', 'first_name', 'last_name', 'age', 'location_name', 'lat', 'lng']

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        user_data = json.loads(request.body)

        self.object.username = user_data['username']
        self.object.password = user_data['password']
        self.object.first_name = user_data['first_name']
        self.object.last_name = user_data['last_name']
        self.object.age = user_data['age']

        if user_data['location_name'] or user_data['lat'] or user_data['lng']:
            try:
                locaton = Location.objects.get(id=self.object.location_id)
                locaton.name = user_data.get('location_name', locaton.name)
                locaton.lat = user_data.get('lat', locaton.lat)
                locaton.lng = user_data.get('lng', locaton.lng)
            except Location.DoesNotExist:
                self.object.location_id = Location.objects.create(name=user_data['location_name'],
                                                                  lat=user_data['lat'],
                                                                  lng=user_data['lng']).id

        self.object.save()

        return JsonResponse({
            'id': self.object.id,
            'username': self.object.username,
            'first_name': self.object.first_name,
            'last_name': self.object.last_name,
            'role': self.object.role,
            'age': self.object.age,
            'location': self.object.location_id.name,
        }, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class UserDeleteView(DeleteView):
    model = User
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({'status': 'ok'})
