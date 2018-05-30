from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse
from django.views import generic
from hoods.models import Hood, HoodMember
from django.contrib import messages
from django.db import IntegrityError
from django.shortcuts import get_object_or_404

# Create your views here

class CreateHood(LoginRequiredMixin, generic.CreateView):
    fields = ('name', 'location')
    model = Hood


class SingleHood(generic.DetailView):
    model = Hood


class ListHoods(generic.ListView):
    model = Hood

class JoinHood(LoginRequiredMixin, generic.RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse('hoods:single', kwargs={'slug': self.kwargs.get('slug')})

    def get(self, request, *args, **kwargs):
        hood = get_object_or_404(Hood, slug=self.kwargs.get('slug'))

        try:
            HoodMember.objects.create(user=self.request.user, hood=hood)
        except IntegrityError:
            messages.warning(self.request, 'You are already a member!')
        else:
            messages.success(self.request, 'Congratulatoins!! You are now a member!')

        return super().get(request, *args, **kwargs)


class LeaveHood(LoginRequiredMixin, generic.RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse('hoods:single', kwargs={'slug': self.kwargs.get('slug')})

    def get(self, request, *args, **kwargs):

        try:
            membership = HoodMember.objects.filter(user=self.request.user, hood__slug=self.kwargs.get('slug')).get()
        except HoodMember.DoesNotExist:
            messages.warning(self.request, 'Sorry your are not a member here!')
        else:
            membership.delete()
            messages.success(self.request, 'You are no longer a member!')

        return super().get(request, *args, **kwargs)