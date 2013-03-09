from django.core.management.base import BaseCommand, CommandError
import logging
logging.basicConfig(filename='calculate_scores.log', level=logging.DEBUG, format='%(asctime)s %(message)s')

from djig.models import Article
from datetime import datetime

class Command(BaseCommand):
    help = "Loops through articles and calculates score."

    def handle(self, *args, **options):
        logging.debug("Calculating scores at %s" % datetime.now())
        articles = Article.objects.all()
        for article in articles:
            article.calculate_score()
            logging.debug("Calculated score for %s" % (article.title))
        logging.debug("Finished calculating scores")
        self.stdout.write("Finished calculating scores at %s." % datetime.now())
