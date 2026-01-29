from django.contrib import admin
from django.urls import include, path
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.conf import settings
from django.shortcuts import redirect
from django.views.i18n import set_language


# --- root redirect: / -> /en/ or /uk/ ---
def root_redirect(request):
    return redirect(f'/{request.LANGUAGE_CODE}/')


urlpatterns = [
    # redirect from root
    path("", root_redirect),

    # admin without language prefix
    path("admin/", admin.site.urls),
    path("i18n/setlang/", set_language, name="set_language"),

]

# --- i18n URLs ---
urlpatterns += i18n_patterns(
    path("", include(("pages.urls", "pages"), namespace="pages")),
)

# --- media in DEBUG ---
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
