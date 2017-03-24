from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from research.categories import GROUPS
from research.models import Company, Individual, Research, Piece, Nugget
from faker import Factory
import uuid, pytz, random


class Command(BaseCommand):

    def __init__(self):
        self.fake = Factory.create()
        self.user = User.objects.filter(is_superuser=True)[0] #get the superuser
        self.pieces = []
        self.nuggets = []

    def handle(self, *args, **options):
        self.create_company()
        self.create_individual()
        self.create_research()
        self.generate_research_pieces()
        print("Fake Research: ", self.research.id)

    def create_company(self):
        self.company = Company(**{
            "clearbit" : uuid.uuid4(),
            "domain": self.fake.domain_name(),
            "created": "2017-03-19T02:50:04.091604Z",
            "name": "Axonify",
            "location" : "Waterloo",
            #"cleanedname": "Axonify",
            "industry": "Internet Software & Services",
            "sector": "Information Technology",
            "crunchbase": "organization/axonify",
            "description": "Axonify is the world’s first Employee Knowledge Platform. Pushing beyond the boundaries of eLearning, it combines an award-winning approach to microlearning, with innovative knowledge-on-demand capabilities to ensure employees do the right things right. The entire experience is gamified, driving high levels of participation. The platform can also measure employee knowledge growth, and tie it directly to behavior that powers business performance. ",
            "logo": "https://logo.clearbit.com/axonify.com"
        })
        self.company.save()
    
    def create_individual(self):
        self.individual = Individual(**{
            "clearbit" : uuid.uuid4(),
            "company" : self.company,
            "email": self.fake.safe_email(),
            "created": "2017-03-19T03:02:26.100871Z",
            "firstname": "Jonathan",
            "lastname": "Jones",
            "jobtitle": "development manager",
            "role": "Operations",
            "avatar": "https://d1ts43dypk8bqh.cloudfront.net/v1/avatars/66087d5d-3918-42bc-9993-bf2f0a1d891c"
        })
        self.individual.save()

    def create_research(self):
        self.research = Research(**{
            "owner" : self.user,
            "complete" : True,
            "individual" : self.individual
        })
        self.research.save()

    def generate_research_pieces(self):
        for group, categories in GROUPS.items():
            url = self.get_publisher_domain()
            newPiece = Piece(**{
                "research" : self.research,
                "aggregator" : "storyzy",
                "publisheddate" : self.fake.date_time_this_month(before_now=True, after_now=False, tzinfo=pytz.utc),
                "title" : self.fake.bs(),
                "author" : self.fake.name(),
                "body" : self.fake.bs(),
                "source" : {
                    "uri": url,
                    "publisher": self.fake.company(),
                    "author": self.fake.name(),
                    "title": self.fake.bs(),
                    "domain" : self.get_publisher_domain
                },
                "url" : url,
                "group" : group,
            })
            newPiece.save()
            for category in categories:
                category = category[0] #it's a tuple so let's just grab the first part
                Nugget(**{
                    "piece" : newPiece,
                    "category" : category,
                    "body" : self.fake.bs(),
                    "additionaldata" : self.generate_additionaldata_for_category(category)
                }).save()


    def generate_additionaldata_for_category(self, category):
        if category == "quote_from_company":
            additionaldata = {
                "company": self.fake.company(),
                "name": self.fake.name(),
                "publisher": self.fake.url()
            }
        else:
            additionaldata = {
                "company": self.fake.company(),
                "name": self.fake.name(),
                "publisher": self.fake.url()
            }
        return additionaldata

    def get_publisher_domain(self):
        return random.choice([
            "thestar.com",
            "theguardian.com",
            "nytimes.com",
            "huffingtonpost.com",
            "financialpost.com"
        ])


