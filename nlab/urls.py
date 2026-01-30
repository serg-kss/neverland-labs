from django.contrib import admin
from django.urls import include, path
from django.conf.urls.i18n import i18n_patterns
from django.shortcuts import redirect
from django.views.i18n import set_language
from django.utils.translation import get_language
from pages.views import sitemap_xml
from pages.views import robots_txt


def root_redirect(request):
    lang = get_language() or "en"
    return redirect(f"/{lang}/")


urlpatterns = [
    path("robots.txt", robots_txt, name="robots_txt"),
    path("", root_redirect),
    path("admin/", admin.site.urls),
    path("i18n/setlang/", set_language, name="set_language"),
    path("sitemap.xml", sitemap_xml, name="sitemap"),
]

urlpatterns += i18n_patterns(
    path("", include(("pages.urls", "pages"), namespace="pages")),
    prefix_default_language=True,
)

