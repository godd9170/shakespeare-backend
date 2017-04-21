from celery import shared_task, task, signature, chord, chain
from research.models import Research, Piece
from django.conf import settings
from research.aggregators import * #get all of our aggregator classes
from research.aggregators import aggregator, storyzy, predictleads, featuredcustomers
import rollbar


def collect_research(research):
    if settings.PERFORM_ASYNCHRONOUS:
        chord([
            chain(predictleadsevents_task.s(research.id), extract_article_bodies_task.s(research.id)),
            predictleadsjobs_task.s(research.id),
            featuredcustomers_task.s(research.id),
            chain(storyzy_task.s(research.id), extract_article_bodies_task.s(research.id))
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
def extract_article_bodies_task(results, research_id):
    research = Research.objects.get(pk=research_id)
    aggregator.AbstractAggregator(research).get_article_bodies()

@task(max_retries=3)
def finish(results, research_id):
    research = Research.objects.get(pk=research_id)
    research.complete = True
    research.save()
    #Notify Rollbar if no results showed up
    if Piece.objects.filter(research=research_id).count() < 1:
        rollbar.report_message('[No Research] No research results found.', 'warning', payload_data={'person' : { 'id' : str(research.owner.id) }}, extra_data={ 'individual_id' : research.individual.id }) #See https://github.com/rollbar/pyrollbar/blob/97623876abeb200182bcc98b4f598dd93f9efcfe/rollbar/logger.py#L102 

@task(max_retries=3, name='error_callback')
def finish_with_errors(results):
    print('>>>>>>>>>>>ARGS>>>>>>>>>>>>>{}'.format(results))
    research = Research.objects.get(pk=research_id)
    research.complete = True
    research.save()
    #Notify Rollbar of failure
    rollbar.report_exc_info()

