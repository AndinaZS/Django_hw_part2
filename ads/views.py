import json

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from HW import settings
from ads.models import Advert, Categories
from users.models import User


class AdvertListView(ListView):
    model = Advert

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        self.object_list.order_by('name')

        paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
        page_number = request.GET.get('page')
        page_list = paginator.get_page(page_number)

        adverts = []
        for advert in page_list:
            adverts.append(
                {'name': advert.name,
                 'author_id': advert.author_id.id,
                 'price': advert.price,
                 'description': advert.description,
                 'categories': list(advert.category_id.all().values_list('name', flat=True)),
                 }
            )

        response = {'items':adverts,
                    'num_pages': page_list.paginator.num_pages,
                    'total': page_list.paginator.count}

        return JsonResponse(response, safe=False)


class AdvertDetailView(DetailView):
    model = Advert

    def get(self, request, *args, **kwargs):
        advert = self.get_object()
        return JsonResponse(
            {'name': advert.name,
             'author': advert.author_id.username,
             'price': advert.price,
             'description': advert.description,
             'categories': list(advert.category_id.all().values_list('name', flat=True)),
             }
        )


@method_decorator(csrf_exempt, name='dispatch')
class AdvertCreateView(CreateView):
    model = Advert
    fields = ['name', 'author_id', 'price', 'description', 'category_id']

    def post(self, request, *args, **kwargs):
        advert_data = json.loads(request.body)
        categories = set()

        try:
            author_id = User.objects.get(id=advert_data['author_id'])
        except User.DoesNotExist:
            return JsonResponse({'error': 'author not found'}, status=404)

        for category in advert_data.get('category_id', []):
            try:
                categories.add(Categories.objects.get(name=category))
            except Categories.DoesNotExist:
                return JsonResponse({'error': f'category {category} not found'}, status=404)

        new_advert = Advert.objects.create(
            name=advert_data['name'],
            author_id=author_id,
            price=advert_data['price'],
            description=advert_data['description'],
        )
        new_advert.category_id.set(categories)

        return JsonResponse({
            'id': new_advert.id,
            'name': new_advert.name,
            'price': new_advert.price,
            'author': new_advert.author_id.username,
            'categories': list(new_advert.category_id.all().values_list('name', flat=True)),
        }, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class AdvertUpdateView(UpdateView):
    model = Advert
    fields = ['name', 'price', 'description', 'category_id']

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        advert_data = json.loads(request.body)

        self.object.name = advert_data['name']
        self.object.price = advert_data['price']
        self.object.description = advert_data['description']

        for category in advert_data.get('category_id', []):
            try:
                self.object.category_id.add(Categories.objects.get(name=category))
            except Categories.DoesNotExist:
                return JsonResponse({'error': f'category {category} not found'})

        self.object.save()

        return JsonResponse({
            'id': self.object.id,
            'name': self.object.name,
            'price': self.object.price,
            'description': self.object.description,
            'categories': list(self.object.category_id.all().values_list('name', flat=True))
        }, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class AdvertImageView(UpdateView):
    model = Advert
    fields = ['image']

    def patch(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.image = request.FILES['image']
        self.object.save()
        return JsonResponse({
                'id': self.object.id,
                'name': self.object.name,
                'image': self.object.image.url,}, status=201)



@method_decorator(csrf_exempt, name='dispatch')
class AdvertDeleteView(DeleteView):
    model = Advert
    success_url = '/ads'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({'status': 'ok'})


'------------Categories------------'


class CatListView(ListView):
    model = Categories

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        response = []
        for category in self.object_list:
            response.append({'name': category.name})

        return JsonResponse(response, safe=False)


class CatDetailView(DetailView):
    model = Categories

    def get(self, request, *args, **kwargs):
        category = self.get_object()
        return JsonResponse({'name': category.name})


@method_decorator(csrf_exempt, name='dispatch')
class CatCreateView(CreateView):
    model = Categories
    fields = ['name']

    def post(self, request, *args, **kwargs):
        category_data = json.loads(request.body)
        new_category = Categories.objects.create(
            name=category_data['name'])

        return JsonResponse({
            'id': new_category.id,
            'name': new_category.name}, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class CatUpdateView(UpdateView):
    model = Categories
    fields = ['name']

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        category_data = json.loads(request.body)
        self.object.name = category_data['name']

        self.object.save()

        return JsonResponse({
            'id': self.object.id,
            'name': self.object.name}, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class CatDeleteView(DeleteView):
    model = Categories
    success_url = '/cat'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({'status': 'ok'})
