from django.views.generic import DetailView
from django.db.models import Sum
from .models import PollingUnit, AnnouncedPUResults, LGA



class PollingUniteResultView(DetailView):
    model = PollingUnit
    pk_url_kwarg = "uniqueid"
    template_name = 'polls/poll_results.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["polling_unit_results"] = AnnouncedPUResults.objects.filter(polling_unit=self.get_object().uniqueid)
        return context


class LGAResultView(DetailView):
    model = LGA
    slug_field = "lga_id"
    slug_url_kwarg = "lga_id"
    template_name = 'polls/lga_results.html'

    def get_queryset(self):
        queryset = self.model.objects.defer('date_entered')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        polling_units = PollingUnit.objects.filter(lga=self.get_object().lga_id).defer('date_entered')
        result = AnnouncedPUResults.objects.filter(polling_unit__in=polling_units)
        distinct_polling_results = result.distinct('party_abbreviation')
        scores = dict()
        for polling_result in distinct_polling_results:
            scores[polling_result.party_abbreviation] = result.filter(party_abbreviation=polling_result.party_abbreviation).aggregate(Sum('party_score'))['party_score__sum']
        context['results'] = scores
        return context
