from django.views.generic import DetailView, FormView, CreateView
from django.db.models import Sum, Q
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import get_object_or_404
from .models import PollingUnit, AnnouncedPUResults, LGA
from .forms import PollForm




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


class RecordPollResult(FormView):
    model = AnnouncedPUResults
    form_class = PollForm
    template_name = "polls/new_poll.html"


    def form_valid(self, form):
        # check if poll result has been recorded for party under this unit
        polling_unit = get_object_or_404(PollingUnit, uniqueid=self.kwargs['uniqueid'])
        results_exist = AnnouncedPUResults.objects.filter(Q(polling_unit=polling_unit.uniqueid) & Q(party_abbreviation=form.cleaned_data['party_abbreviation']))
        if results_exist:
            messages.warning(
                self.request, 
                f"""
                Polling result for {form.cleaned_data['party_abbreviation']} 
                have already been recorded under this polling unit {polling_unit.uniqueid}, 
                please record for another party or move to an entire new new polling unit
                """
            )
            return self.form_invalid(form)
        # record polling result if party is new
        announced_pu_results =  AnnouncedPUResults.objects.create(
            **form.cleaned_data,
            polling_unit=int(self.kwargs['uniqueid']),
            user_ip_address="127.0.0.1"
        )
        self.success_url = reverse("polls:unit-results", kwargs={"uniqueid": self.kwargs['uniqueid']})
        return super().form_valid(form)