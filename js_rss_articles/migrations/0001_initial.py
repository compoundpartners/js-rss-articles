# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-12-04 04:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cms', '0020_old_tree_cleanup'),
    ]

    operations = [
        migrations.CreateModel(
            name='RSSArticles',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='js_rss_articles_rssarticles', serialize=False, to='cms.CMSPlugin')),
                ('title', models.CharField(blank=True, max_length=255, null=True, verbose_name='title')),
                ('url', models.CharField(blank=True, max_length=255, null=True, verbose_name='rss url')),
                ('count', models.IntegerField(verbose_name='number of articles')),
                ('layout', models.CharField(choices=[('columns', 'Columns'), ('rows', 'Rows'), ('hero', 'Hero'), ('articles', 'Articles')], max_length=30, verbose_name='layout')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
    ]
