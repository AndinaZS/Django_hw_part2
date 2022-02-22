from django.http import JsonResponse
from django.views.generic import ListView, CreateView, DetailView
from ads.models import Advert, Categories
from users.models import User, Location


class AdvertListView(ListView):
    pass
    model = Advert

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        response = []
        for advert in self.object_list:
            response.append(
                {'name': advert.name,
                 'price': advert.price,
                 'description': advert.description,
                 'is_published': advert.is_published,
                 }
            )

        return JsonResponse(response, safe=False)


class AdvertCreateView(CreateView):
    pass


class AdvertDetailView(DetailView):
    pass



