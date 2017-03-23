from research.models import Research, Piece, Nugget

class AbstractAggregator(object):
    
    def __init__(self, research):
        self.research = research
        self.companyName = self.research.individual.companyname

    def create_piece(self, piece):
        self.currentPiece = Piece(research=self.research, **piece)
        self.currentPiece.save()

    def create_nugget(self, nugget):
        Nugget(piece=self.currentPiece, **nugget).save()
