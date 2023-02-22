import django.core.management.base
from partsmanagement import models
import csv


def sku(part):
    return f'VTQ-{part["Artikelnummer"]}'


class Command(django.core.management.base.BaseCommand):
    """Import VTQ Geschenke"""

    help = __doc__
    _file_ = __file__

    def handle(self, *args, **options):
        """Execute the command."""
        catsearch = models.Category.objects.filter(name='VTQ')
        if not len(catsearch):
            category = models.Category(name='VTQ')
            category.save()
        else:
            category = catsearch[0]
        with open('vtq.csv', newline='') as csvfile:
            parts = csv.DictReader(csvfile , delimiter=';')
            for part in parts:
                print(f"Adding {part['Matchcode']}")
                partsearch = models.Part.objects.filter(sku=sku(part))
                if not len(partsearch):
                    partadd = models.Part()
                    partadd.name = part['Matchcode']
                    partadd.description = part['Matchcode'] + part['Bemerkung']
                    partadd.sku = sku(part)
                    partadd.save()
                    partadd.categories.set((category, ))
                    partadd.save()
                else:
                    partadd = partsearch[0]
                kistensearch = models.StoragePlace.objects.filter(name=part['lagerort'])
                if not len(kistensearch):
                    kiste = models.StoragePlace(name=part['lagerort'])
                    kiste.save()
                else:
                    kiste = kistensearch[0]
                sisearch = models.StorageItem.objects.filter(part=partadd, storage=kiste)
                if not len(sisearch):
                    si = models.StorageItem(part=partadd, storage=kiste)
                    si.save()
                else:
                    si = sisearch[0]
                    print("using existing storageitem")
                old_amount = si.on_stock or 0
                si.on_stock = old_amount + int(part['Bestand'])

                si.save()
