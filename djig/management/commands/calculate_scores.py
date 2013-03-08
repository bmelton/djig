from django.core.management.base import BaseCommand, CommandError

from djig.models import Article

class Command(BaseCommand):
    help = "Loops through articles and calculates score."

    def handle(self, *args, **options):
        articles = Article.objects.all()
        for article in articles:
            article.calculate_score()
        self.stdout.write("Finished calculating scores.")
