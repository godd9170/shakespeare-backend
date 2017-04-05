from research.models import Research, Piece, Nugget
from research.categories import category_to_group
from urllib.parse import urlparse
from newspaper import Article
import re

class AbstractAggregator(object):
    
    def __init__(self, research):
        self.research = research
        self.companyName = self.research.individual.companyname

    def create_piece(self, piece):
        self.currentPiece = Piece(research=self.research, **piece)
        self.currentPiece.save()

    def create_nugget(self, nugget):
        Nugget(piece=self.currentPiece, **nugget).save()


    def category_to_group(self, category):
        return category_to_group(category)

    def parse_domain(self, url):
        return re.sub(r"(www\.)", "", urlparse(url).netloc)


    def get_article_bodies(self):
        pieces = Piece.objects.all().filter(research=self.research.id)
        for piece in pieces:
            try:
                print(piece)
                article = Article(piece.url)
                article.download()
                article.parse()
                piece.body = article.text
            except:
                piece.body = ''
            piece.save()
            
            

    # TO DO: this lives both here and in storyzy, it will move into an aggregator utils at some stage
    # This function strips of the period at the end of an article title if there is one
    def reformat_article_title(self, title):
        try:
            if title.endswith('.') or title.endswith(',') or title.endswith(';'):
                title = title[:-1]
        except:
            pass
        return title