import MySQLdb

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

class Command(BaseCommand):
    help = "Fixes 'Incorrect String Value' errors when trying to save unicode characters."

    def handle(self, *args, **options):
        hostname    = settings.DATABASES["default"]["HOST"]
        port        = settings.DATABASES["default"]["PORT"]
        user        = settings.DATABASES["default"]["USER"]
        password    = settings.DATABASES["default"]["PASSWORD"]
        dbname      = settings.DATABASES["default"]["NAME"]

        if hostname == "":
            hostname = "localhost"

        db = MySQLdb.connect(host=hostname, user=user, passwd=password, db=dbname)
        cursor = db.cursor()

        cursor.execute("ALTER DATABASE `%s` CHARACTER SET 'utf8' COLLATE 'utf8_unicode_ci'" % dbname)

        sql = "SELECT DISTINCT(table_name) FROM information_schema.columns WHERE table_schema = '%s'" % dbname
        cursor.execute(sql)

        results = cursor.fetchall()
        for row in results:
            sql = "ALTER TABLE `%s` convert to character set DEFAULT COLLATE DEFAULT" % (row[0])
            cursor.execute(sql)

        db.close()
        self.stdout.write("Finised converting database.")
