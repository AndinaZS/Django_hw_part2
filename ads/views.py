from django.http import JsonResponse
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from ads.models import Advert, Categories
from users.models import User, Location


class AdvertListView(ListView):
    model = Advert

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        response = []
        for advert in self.object_list:
            response.append(
                {'name': advert.name,
                 'author_id': advert.author_id,
                 'price': advert.price,
                 'description': advert.description,
                 'category_id': advert.category_id,
                 }
            )

        return JsonResponse(response, safe=False)


class AdvertCreateView(CreateView):
    pass


class AdvertDetailView(DetailView):
    pass


class AdvertUpdateView(UpdateView):
    pass


class AdvertDeleteView(DeleteView):
    pass


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


class CatCreateView(CreateView):
    pass


class CatUpdateView(UpdateView):
    pass


class CatDeleteView(DeleteView):
    pass