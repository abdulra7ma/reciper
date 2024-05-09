from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

PLATFORM_PREFIX = "_platform"
API_PREFIX = "api"
DOCS_PREFIX = "docs"

api_v1_urlpatterns = [
    path(
        f"{API_PREFIX}/v1/accounts/",
        include(("reciper.apps.accounts.api.v1.urls", "accounts"), namespace="api-v1-accounts"),
    ),
    path(
        f"{API_PREFIX}/v1/common/",
        include(("reciper.apps.common.api.urls", "common"), namespace="api-v1-common"),
    ),
    path(
        f"{API_PREFIX}/v1/recipes/",
        include(("reciper.apps.recipes.api.urls", "recipes"), namespace="api-v1-recipes"),
    ),
    path(
        f"{API_PREFIX}/v1/shopping/",
        include(("reciper.apps.shopping.api.urls", "shopping"), namespace="api-v1-shopping"),
    ),
    path(
        f"{API_PREFIX}/v1/tips/",
        include(("reciper.apps.tips.api.urls", "tips"), namespace="api-v1-tips"),
    ),
]

urlpatterns = [
    path("admin/", admin.site.urls),
    *api_v1_urlpatterns,
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# enable Swagger
if "SWAGGER" in settings.RECIPER_FEATURES:
    from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

    swagger_urlpatterns = [
        path(f"{PLATFORM_PREFIX}/{DOCS_PREFIX}/v1/schema/", SpectacularAPIView.as_view(), name="schema"),
        path(
            f"{PLATFORM_PREFIX}/{DOCS_PREFIX}/v1/swagger/",
            SpectacularSwaggerView.as_view(url_name="schema"),
            name="v1-schema-swagger-ui",
        ),
        path(
            f"{PLATFORM_PREFIX}/{DOCS_PREFIX}/v1/redoc/",
            SpectacularRedocView.as_view(url_name="schema"),
            name="v1-schema-redoc",
        ),
    ]

    urlpatterns += swagger_urlpatterns

# enable debug_toolbar for local develop (if installed)
if settings.DEBUG and "debug_toolbar" in settings.INSTALLED_APPS:
    import debug_toolbar

    urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]

# enable Sentry check (by raising 500 on demand)
if not settings.DEBUG:
    from django.views.generic.base import View  # pylint: disable=ungrouped-imports


    class ServerErrorTestView(View):
        def dispatch(self, request, *args, **kwargs):
            assert False, "Server error test: response with 500 HTTP status code"  # noqa: S101


    urlpatterns += [path(f"{PLATFORM_PREFIX}/500-error-test/", ServerErrorTestView.as_view())]
