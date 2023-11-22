from django.contrib import admin
from .models import Movie, Director, Actor
from django.db.models import QuerySet

# Register your models here.
admin.site.register(Director)
admin.site.register(Actor)


class RatingFilter(admin.SimpleListFilter):
    title = 'рейтингом'
    parameter_name = 'рейтинг'

    def lookups(self, request, model_admin):
        return [
            ('<40', 'low'),
            ('від 40 до 59', 'mid'),
            ('від 60 до 79', 'high'),
            ('від 80', 'higher'),
        ]

    def queryset(self, request, queryset: QuerySet):
        if self.value() == '<40':
            return queryset.filter(rating__lt=40)
        elif self.value() == 'від 40 до 59':
            return queryset.filter(rating__gte=40).filter(rating__lt=60)
        elif self.value() == 'від 60 до 79':
            return queryset.filter(rating__gte=60).filter(rating__lt=80)
        elif self.value() == 'від 80':
            return queryset.filter(rating__gte=80).filter(rating__lt=101)
        else:
            return queryset


class MovieAdmin(admin.ModelAdmin):
    fields = ('name', 'rating', 'year', 'budget', 'currency', 'slug', 'director', 'actors')
    # fieldsets = [
    #     ('Movie Information', {'fields': ['name', 'rating', 'year', 'budget', 'currency', 'slug']}),
    #     ('Director Information', {'fields': ['director']}),
    #     ('Actors', {'fields': ['actors']}),
    # ]
    # exclude = ['slug']
    # readonly_fields = ['slug'] # не комбінити з prepopulated_fields бо все полетить на*уй
    prepopulated_fields = {'slug': ('name',)}
    list_display = ['name', 'rating', 'year', 'budget', 'director', 'rating_status']
    list_editable = ['rating', 'year', 'director', 'budget']
    list_per_page = 10
    ordering = ['-rating', 'name']
    actions = ['set_usd', 'set_eur', 'set_uah']
    search_fields = ['name']
    list_filter = ['name', 'currency', RatingFilter]
    filter_horizontal = ['actors']

    def rating_status(self, mov: Movie):  # mov: Movie потрібно для піказки атрибутів
        if mov.rating < 50:
            return 'не дивись ці помиї'
        elif 50 < mov.rating < 70:
            return 'можна глянути'
        elif 70 < mov.rating < 85:
            return 'топчик'
        else:
            return '100% треба дивитись'

    def update_and_notify_currency(self, request, qs: QuerySet, currency):
        count_updated = qs.update(currency=currency)
        self.message_user(
            request,
            f'Було оновлено {count_updated} записів'
        )

    @admin.action(description='встановити валюту в: USD')
    def set_usd(self, request, qs: QuerySet):
        self.update_and_notify_currency(request, qs, Movie.USD)

    @admin.action(description='встановити валюту в: EUR')
    def set_eur(self, request, qs: QuerySet):
        self.update_and_notify_currency(request, qs, Movie.EUR)

    @admin.action(description='встановити валюту в: UAH')
    def set_uah(self, request, qs: QuerySet):
        self.update_and_notify_currency(request, qs, Movie.UAH)

    # @admin.action(description='встановити валюту в: USD')
    # def set_usd(self, request, qs: QuerySet):
    #     count_updated = qs.update(currency=Movie.USD)
    #     self.message_user(
    #         request,
    #         f'Було оновлено {count_updated} записів'
    #                       )


admin.site.register(Movie, MovieAdmin)
