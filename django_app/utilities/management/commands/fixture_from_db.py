from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.core import serializers
from battle.models import Battle, Player

class Command(BaseCommand):
    def handle(self, **kwargs):
        singleObject = not True;
        obj = None
        queryset = None
        if singleObject:
            # obj = Entity.objects.get(id=4)
            pass
        else:
#             queryset = User.objects.all()
#             queryset = Battle.objects.all()
            queryset = Player.objects.all()
            pass

        # Save to file
        out = open("model_fixture.json", "w")
        json_serializer = serializers.get_serializer("json")()
        if singleObject:
            json_serializer.serialize([obj], stream = out, sort_keys = True, indent = 4)
        else:
            items = []
            print "Total rows: %d " % len(queryset)
            for item in queryset:
                items.append(item)
            json_serializer.serialize(items, stream = out, sort_keys = True, indent = 4)
        out.close()

if __name__ == '__main__':
    import sys
    tests = []
    sys.argv = ['', 'fixture_from_db']
    import os
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_app.settings")
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)