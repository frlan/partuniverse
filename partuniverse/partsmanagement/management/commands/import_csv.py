import django.core.management.base
from partsmanagement import models
import csv


#sku;title;amount;description;categories;storage_place
#123513214;Arduino nano;5;The famous Arduino nano;microcontroller,atmel;X-5-3

class Command(django.core.management.base.BaseCommand):
    """Import parts from csv"""
    help = 'Import parts from csv. See example.csv for format details.'

    def add_arguments(self, parser):
        parser.add_argument('csv_filename', type=str)

    def handle(self, *args, **options):
        """Execute the command."""
        with open(options['csv_filename'], newline='') as csvfile:
            parts = csv.DictReader(csvfile , delimiter=';')
            for part in parts:
                part_categories = []
                for cat in part['categories'].split(','):
                    catsearch = models.Category.objects.filter(name=cat)
                    if not len(catsearch):
                        category = models.Category.objects.create(name=cat)
                        category.save()
                    else:
                        category = catsearch[0]
                    part_categories.append(category)

                print(f"Adding {part['title']}")
                partsearch = models.Part.objects.filter(sku=part['sku'])
                if not len(partsearch):
                    partadd = models.Part.objects.create(
                                name=part['title'],
                                description=part['description'],
                                sku=part['sku'])
                    partadd.save()
                    partadd.categories.set(tuple(part_categories))
                    partadd.save()
                else:
                    partadd = partsearch[0]
                kistensearch = models.StoragePlace.objects.filter(name=part['storage_place'])
                if not len(kistensearch):
                    kiste = models.StoragePlace.objects.create(name=part['storage_place'])
                    kiste.save()
                else:
                    kiste = kistensearch[0]
                sisearch = models.StorageItem.objects.filter(part=partadd, storage=kiste)
                if not len(sisearch):
                    si = models.StorageItem.objects.create(part=partadd, storage=kiste)
                    si.save()
                else:
                    si = sisearch[0]
                    print("using existing storageitem")
                old_amount = si.on_stock or 0
                si.on_stock = old_amount + int(part['amount'])

                si.save()
