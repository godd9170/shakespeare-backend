from celery import shared_task
from research.utils import get_research_pieces
from .models import Research


@shared_task
def get_research_pieces_task(research_id):
    research = Research.objects.get(pk=research_id)
    get_research_pieces(research)