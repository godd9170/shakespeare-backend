from celery import shared_task, task, signature, chord
from research.models import Research
from research.aggregators.predictleads import do_predictleads_events
from research.aggregators.storyzy import do_storyzy
from research.aggregators.featuredcustomers import FeaturedCustomers
from django.conf import settings
                  

def collect_research(research):
    if settings.PERFORM_ASYNCHRONOUS:
        chord([
            storyzy.s(research.id),
            predictleads.s(research.id),
            featuredcustomers.s(research.id)
        ])(finish.s(research.id).set(link_error=['error_callback']))
    else:
        #do_storyzy(research)
        #do_predictleads_events(research)
        FeaturedCustomers(research).execute()
        research.complete = True # Mark as complete
        research.save()

@task(max_retries=3)
def storyzy(research_id):
    research = Research.objects.get(pk=research_id)
    do_storyzy(research)

@task(max_retries=3)
def predictleads(research_id):
    research = Research.objects.get(pk=research_id)
    do_predictleads_events(research)

@task(max_retries=3)
def featuredcustomers(research_id):
    research = Research.objects.get(pk=research_id)
    do_featuredcustomers(research)

@task(max_retries=3)
def finish(results, research_id):
    research = Research.objects.get(pk=research_id)
    research.complete = True
    research.save()

@task(max_retries=3, name='error_callback')
def finish_with_errors(results, research_id):
    print('>>>>>>>>>>>ARGS>>>>>>>>>>>>>{}'.format(results))
    research = Research.objects.get(pk=research_id)
    research.complete = True
    research.save()