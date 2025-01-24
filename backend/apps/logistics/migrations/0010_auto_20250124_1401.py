from django.db import migrations, models
class Migration(migrations.Migration):
    dependencies = [
        ('logistics', '0009_rename_position_contact_title'),
    ]
    operations = [
        migrations.DeleteModel('ContactAddress'),
        migrations.AddField(
            model_name='contact',
            name='addresses',
            field=models.ManyToManyField('Address', related_name='contacts', blank=True),
        ),
    ]