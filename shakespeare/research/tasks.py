from celery import shared_task, task, signature, chord
from research.models import Research
from django.conf import settings
from research.aggregators import * #get all of our aggregator classes


def collect_research(research):
    if settings.PERFORM_ASYNCHRONOUS:
        chord([
            storyzy.s(research.id),
            predictleadsevents.s(research.id),
            predictleadsjobs.s(research.id),
            featuredcustomers.s(research.id)
        ])(finish.s(research.id).set(link_error=['error_callback']))
    else:
        #do_storyzy(research)
        #PredictLeads(research).execute('job_openings')
        #PredictLeads(research).execute('events')
        #FeaturedCustomers(research).execute()
        #Storyzy(research).execute()
        research.complete = True # Mark as complete
        research.save()

@task(max_retries=3)
def storyzy(research_id):
    research = Research.objects.get(pk=research_id)
    Storyzy(research).execute()

@task(max_retries=3)
def predictleadsevents(research_id):
    research = Research.objects.get(pk=research_id)
    PredictLeads(research).execute('events')

@task(max_retries=3)
def predictleadsjobs(research_id):
    research = Research.objects.get(pk=research_id)
    PredictLeads(research).execute('job_openings')

@task(max_retries=3)
def featuredcustomers(research_id):
    research = Research.objects.get(pk=research_id)
    FeaturedCustomers(research).execute()

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