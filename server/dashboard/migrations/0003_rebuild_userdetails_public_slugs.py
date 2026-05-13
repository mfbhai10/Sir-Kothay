# Generated manually — rebuild URL slugs from slugified username + pk

from django.db import migrations
from django.utils.text import slugify


def forwards(apps, schema_editor):
    UserDetails = apps.get_model('dashboard', 'UserDetails')
    User = apps.get_model('authApp', 'CustomUser')

    for row in UserDetails.objects.iterator():
        user = User.objects.get(pk=row.user_id)
        base = slugify(str(user.username), allow_unicode=False) or 'user'
        base = base[:80]
        new_slug = f'{base}-{row.pk}'[:100]
        if row._slug != new_slug:
            UserDetails.objects.filter(pk=row.pk).update(_slug=new_slug)


def backwards(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_alter_userdetails_user'),
        ('authApp', '0003_username_and_url_slugs'),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
