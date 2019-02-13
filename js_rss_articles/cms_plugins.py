# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from cms.plugin_pool import plugin_pool
from cms.plugin_base import CMSPluginBase
from .models import RSSArticles


@plugin_pool.register_plugin
class RSSArticlesPlugin(CMSPluginBase):
    model = RSSArticles
    name = _('RSS Articles')
    admin_preview = False
    render_template = 'js-rss-articles/articles.html'

    TEMPLATE_NAMES = {
        'columns': 'cols.html',
        'rows': 'rows.html',
        'hero': 'hero.html',
        'articles': 'articles.html',
    }

    def render(self, context, instance, placeholder):
        layout = instance.layout
        self.render_template = 'js-rss-articles/' + self.TEMPLATE_NAMES[layout]
        context.update({
            'object': instance,
            'placeholder': placeholder,
        })
        return context
