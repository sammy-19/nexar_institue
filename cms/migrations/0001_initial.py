# Generated by Django 5.1.6 on 2025-04-27 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PageContent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.CharField(help_text="Unique identifier for this content (e.g., 'programs_banner', 'about_us_intro').", max_length=100, unique=True)),
                ('content_type', models.CharField(choices=[('text', 'Text'), ('image', 'Image'), ('rich_text', 'Rich Text')], default='text', max_length=10)),
                ('text_content', models.TextField(blank=True, help_text='Use for plain text or rich text content.', null=True)),
                ('image_content', models.ImageField(blank=True, help_text='Use for image content.', null=True, upload_to='page_content_images/')),
                ('description', models.CharField(blank=True, help_text='Brief description of what this content is for.', max_length=255)),
                ('last_updated', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
