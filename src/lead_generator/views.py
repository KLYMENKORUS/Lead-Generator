from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic import ListView
from users.forms import UserUpdateForm
from .models import Lead
from django.contrib.auth import get_user_model

__all__ = (
    'MainView',
    'ListLeadsView'
)

User = get_user_model()


class MainView(LoginRequiredMixin, TemplateView):
    template_name = 'lead_generator/lead_generator.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'You are not authenticated')
            return HttpResponseRedirect(reverse_lazy('users:login'))

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['update_form'] = UserUpdateForm(instance=self.request.user)

        return context


class ListLeadsView(LoginRequiredMixin, ListView):
    model = Lead
    template_name = 'lead_generator/list_leads.html'
    paginate_by = 10

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'You are not authenticated')
            return HttpResponseRedirect(reverse_lazy('users:login'))

        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        user_parameters = User.objects.filter(username=self.request.user.username,
                                              is_active=True).values().first()
        keyword = user_parameters.get('keyword')
        location = user_parameters.get('location')
        queryset = Lead.objects.filter(keyword=keyword, location=location)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        count = self.request.GET.get('value')
        context['all_leads'] = self.get_queryset()[:count]
        return context








