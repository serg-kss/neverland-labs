from django.urls import path
from pages import views


app_name = 'pages'

urlpatterns = [
    path("", views.index, name="index"),

    path("privacy", views.privacy, name="privacy"),
    path("terms", views.terms, name="terms"),

    path("development", views.development, name="development"),
    path("marketing", views.marketing, name="marketing"),
    path("data", views.data, name="data"),
    path("ux-ui-design", views.ux, name="ux"),

    path("contact/send/", views.contact_form, name="contact_send"),

    path("download/ux-pdf/", views.download_ux_pdf, name="download_ux_pdf"),
    path("download/dev-pdf/", views.download_dev_pdf, name="download_dev_pdf"),
    path("download/marketing-pdf/", views.download_marketing_pdf, name="download_marketing_pdf"),
    path("download/data-pdf/", views.download_data_pdf, name="download_data_pdf"),

    path("portfolio/strike-shop-action", views.portfolio_action, name="strikeshopaction"),
]