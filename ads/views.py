import json

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from HW import settings
from ads.models import Advert, Category
from users.models import User


class AdvertListView(ListView):
    model = Advert

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        self.object_list = self.object_list.select_related('author').prefetch_related('category').order_by('price')

        paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
        page_number = request.GET.get('page')
        page_list = paginator.get_page(page_number)

        adverts = []
        for advert in page_list:
            adverts.append(
                {'name': advert.name,
                 'author': advert.author.username,
                 'price': advert.price,
                 'description': advert.description,
                 'image': advert.image.url,
                 'category': advert.category.name,
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
             'author': advert.author.username,
             'price': advert.price,
             'description': advert.description,
             'image': advert.image.url,
             'category': advert.category.name,
             }
        )


@method_decorator(csrf_exempt, name='dispatch')
class AdvertCreateView(CreateView):
    model = Advert
    fields = ['name', 'author', 'price', 'description', 'category']

    def post(self, request, *args, **kwargs):
        advert_data = json.loads(request.body)

        author = get_object_or_404(User, pk=advert_data['author'])
        category = get_object_or_404(Category, pk=advert_data['category'])

        new_advert = Advert.objects.create(
            name=advert_data['name'],
            author=author,
            price=advert_data['price'],
            description=advert_data['description'],
            category=category,
        )

        return JsonResponse({
            'id': new_advert.id,
            'name': new_advert.name,
            'price': new_advert.price,
            'author': new_advert.author.username,
            'categories': new_advert.category.name,
        }, status=201)


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
        self.object.category = get_object_or_404(Category, pk=advert_data['category'])

        self.object.save()

        return JsonResponse({
            'id': self.object.id,
            'name': self.object.name,
            'price': self.object.price,
            'description': self.object.description,
            'categories': self.object.category
        }, status=201)


@method_decorator(csrf_exempt, name='dispatch')
class AdvertImageView(UpdateView):
    model = Advert
    fields = ['image']

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.image = request.FILES['image']
        self.object.save()

        return JsonResponse({
                'id': self.object.id,
                'name': self.object.name,
                'image': self.object.image.url}, status=201)



@method_decorator(csrf_exempt, name='dispatch')
class AdvertDeleteView(DeleteView):
    model = Advert
    success_url = '/ads'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({'status': 'ok'})


'------------Categories------------'


class CatListView(ListView):
    model = Category

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        self.object_list.order_by('name')

        response = []
        for category in self.object_list:
            response.append({'name': category.name})

        return JsonResponse(response, safe=False)


class CatDetailView(DetailView):
    model = Category

    def get(self, request, *args, **kwargs):
        category = self.get_object()
        return JsonResponse({'name': category.name})


@method_decorator(csrf_exempt, name='dispatch')
class CatCreateView(CreateView):
    model = Category
    fields = ['name']

    def post(self, request, *args, **kwargs):
        category_data = json.loads(request.body)
        new_category = Category.objects.create(
            name=category_data['name'])

        return JsonResponse({
            'id': new_category.id,
            'name': new_category.name}, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class CatUpdateView(UpdateView):
    model = Category
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
    model = Category
    success_url = '/cat'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({'status': 'ok'})
