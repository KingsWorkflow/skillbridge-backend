from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='title',
            field=models.CharField(blank=True, help_text='Professional title or role, e.g. Full-Stack Developer', max_length=200),
        ),
    ]
