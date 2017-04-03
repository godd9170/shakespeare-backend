from celery import shared_task, task, signature, chord, chain
from research.models import Research
from django.conf import settings
from .aggregators import * #get all of our aggregator classes
# from .aggregators import aggregator


def collect_research(research):
    if settings.PERFORM_ASYNCHRONOUS:
        chord([
            chain(storyzy_task.s(research.id), extract_article_bodies.s(research.id)),
            chain(predictleadsevents_task.s(research.id), extract_article_bodies.s(research.id)),
            predictleadsjobs_task.s(research.id),
            featuredcustomers_task.s(research.id)
        ])(finish.s(research.id).set(link_error=['error_callback']))
    else:
        # do_storyzy(research)
        # PredictLeads(research).execute('job_openings')
        # PredictLeads(research).execute('events')
        # FeaturedCustomers(research).execute()
        # Storyzy(research).execute()
        research.complete = True # Mark as complete
        research.save()

@task(max_retries=3)
def storyzy_task(research_id):
    research = Research.objects.get(pk=research_id)
    storyzy.Storyzy(research).execute()

@task(max_retries=3)
def predictleadsevents_task(research_id):
    research = Research.objects.get(pk=research_id)
    predictleads.PredictLeads(research).execute('events')

@task(max_retries=3)
def predictleadsjobs_task(research_id):
    research = Research.objects.get(pk=research_id)
    predictleads.PredictLeads(research).execute('job_openings')

@task(max_retries=3)
def featuredcustomers_task(research_id):
    research = Research.objects.get(pk=research_id)
    featuredcustomers.FeaturedCustomers(research).execute()

@task(max_retries=3)
def extract_article_bodies(results, research_id):
    research = Research.objects.get(pk=research_id)
    aggregator.AbstractAggregator(research).get_article_bodies()

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