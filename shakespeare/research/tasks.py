from celery import shared_task, task, signature, chord
from research.utils import get_research_pieces
from research.models import Research
from research.aggregators.predictleads import do_predictleads_events
from research.aggregators.storyzy import do_storyzy


@shared_task(max_retries=3)
def collect_research(research_id):
    chord([
        storyzy.s(research_id),
        predictleads.s(research_id)
    ])(finish.s(research_id).set(link_error=['error_callback']))

@task(max_retries=3)
def storyzy(research_id):
    research = Research.objects.get(pk=research_id)
    do_storyzy(research)

@task(max_retries=3)
def predictleads(research_id):
    research = Research.objects.get(pk=research_id)
    do_predictleads_events(research)

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

@shared_task(max_retries=3)
def get_research_pieces_task(research_id):
    research = Research.objects.get(pk=research_id)
    get_research_pieces(research)
    research.complete = True #Mark the record complete once it's done gathering research
    research.save()