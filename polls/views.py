from django.views.generic import DetailView
from .models import PollingUnit, AnnouncedPUResults



class PollingUniteResultView(DetailView):
    model = PollingUnit
    pk_url_kwarg = "uniqueid"
    template_name = 'polls/poll_results.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["polling_unit_results"] = AnnouncedPUResults.objects.filter(polling_unit=self.get_object().uniqueid)
        return context
