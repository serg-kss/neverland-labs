import requests
import os
import time

from django.shortcuts import render
from django.conf import settings
from django.http import FileResponse
from django.utils.translation import get_language
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.urls import reverse
from django.template.loader import render_to_string
from django.utils.translation import gettext as _


def index(request):
    return render(request, 'pages/index.html', {
        'title': _("Digital Product Development, Marketing & Analytics | Neverland Labs"),
        'description': _("We design, build, and grow digital products using web development, UX design, marketing strategy, and data analytics."),
        'og_title': _("Neverland Labs — Digital Product Development & Growth"),
        'og_description': _("We build, market, and scale digital products using engineering, UX, marketing, and data analytics."),
    })


def privacy(request):
    return render(request, 'pages/privacy.html', {
        'title': _("Privacy Policy | Neverland Labs"),
        'description': _("Learn how Neverland Labs collects, uses, and protects your personal data."),
        'og_title': _("Privacy Policy — Neverland Labs"),
        'og_description': _("Information about how we collect, store, and protect user data."),
    })


def terms(request):
    return render(request, 'pages/terms.html', {
        'title': _("Terms of Service | Neverland Labs"),
        'description': _("Terms and conditions governing the use of Neverland Labs website and services."),
        'og_title': _("Terms of Service — Neverland Labs"),
        'og_description': _("Rules and conditions for using Neverland Labs services and website."),
    })


def development(request):
    return render(request, 'pages/development.html', {
        'title': _("Custom Web & SaaS Development Services | Neverland Labs"),
        'description': _("Custom web and SaaS development services focused on scalable architecture, performance, and business goals."),
        'og_title': _("Web & SaaS Development — Neverland Labs"),
        'og_description': _("We build scalable web platforms and SaaS products with modern technologies."),
    })


def marketing(request):
    return render(request, 'pages/marketing.html', {
        'title': _("Digital Marketing Strategy for SaaS & Startups | Neverland Labs"),
        'description': _("Digital marketing strategies for SaaS and digital platforms focused on growth, acquisition, and retention."),
        'og_title': _("Digital Marketing Strategy — Neverland Labs"),
        'og_description': _("Growth-focused marketing strategies for SaaS, startups, and digital products."),
    })


def data(request):
    return render(request, 'pages/data.html', {
        'title': _("Data Analytics & Growth Insights for Products | Neverland Labs"),
        'description': _("Product and business analytics to track performance, user behavior, and data-driven growth."),
        'og_title': _("Data & Analytics — Neverland Labs"),
        'og_description': _("Analytics, dashboards, and insights to drive product and business growth."),
    })


def ux(request):
    return render(request, 'pages/ux.html', {
        'title': _("UX & UI Design for Digital Products | Neverland Labs"),
        'description': _("User-centered UX and UI design for digital products, focused on usability, clarity, and conversion."),
        'og_title': _("UX & UI Design — Neverland Labs"),
        'og_description': _("User-centered UX/UI design focused on usability, clarity, and business impact."),
    })


def portfolio_action(request):
    return render(request, 'pages/portfolio/action.html', {
        'title': _("Airsoft Game Management System | Neverland Labs"),
        'description': _("A custom web platform for managing airsoft games, equipment rentals, and player coordination."),
        'og_title': _("Strike Shop Action — Case Study"),
        'og_description': _("Case study: a platform for managing airsoft games, rentals, and player coordination."),
    })



@require_POST
def contact_form(request):

    now = int(time.time())
    last_sent = request.session.get("contact_form_last_sent", 0)

    if now - last_sent < 120:
        return HttpResponse("OK")

    name = request.POST.get("name", "").strip()
    email = request.POST.get("email", "").strip()
    subject = request.POST.get("subject", "").strip()
    message = request.POST.get("message", "").strip()

    if not all([name, email, subject, message]):
        return HttpResponse("Invalid input", status=400)

    text = (
        "New Contact Message\n\n"
        f"Name: {name}\n"
        f"Email: {email}\n"
        f"Subject: {subject}\n\n"
        f"Message:\n{message}"
    )

    telegram_url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": settings.TELEGRAM_CHAT_ID,
        "text": text,
    }

    try:
        requests.post(telegram_url, data=payload, timeout=5).raise_for_status()
    except Exception as e:
        print("Telegram error:", e)
        return HttpResponse("Failed", status=500)

    request.session["contact_form_last_sent"] = now
    request.session.modified = True

    return HttpResponse("OK")


def download_ux_pdf(request):
    lang = get_language()
    filename = "ux-ui-design_uk.pdf" if lang == "uk" else "ux-ui-design_en.pdf"
    file_path = os.path.join(settings.BASE_DIR, "static", "pdfs", filename)

    return FileResponse(
        open(file_path, "rb"),
        as_attachment=True,
        filename=filename,
    )


def download_dev_pdf(request):
    lang = get_language()
    filename = "dev_uk.pdf" if lang == "uk" else "dev_en.pdf"
    file_path = os.path.join(settings.BASE_DIR, "static", "pdfs", filename)

    return FileResponse(
        open(file_path, "rb"),
        as_attachment=True,
        filename=filename,
    )


def download_marketing_pdf(request):
    lang = get_language()
    filename = "marketing_uk.pdf" if lang == "uk" else "marketing_en.pdf"
    file_path = os.path.join(settings.BASE_DIR, "static", "pdfs", filename)

    return FileResponse(
        open(file_path, "rb"),
        as_attachment=True,
        filename=filename,
    )


def download_data_pdf(request):
    lang = get_language()
    filename = "data_uk.pdf" if lang == "uk" else "data_en.pdf"
    file_path = os.path.join(settings.BASE_DIR, "static", "pdfs", filename)

    return FileResponse(
        open(file_path, "rb"),
        as_attachment=True,
        filename=filename,
    )


def sitemap_xml(request):
    urls = [
        "pages:index",
        "pages:development",
        "pages:ux",
        "pages:marketing",
        "pages:data",
        "pages:privacy",
        "pages:terms",
        "pages:strikeshopaction",
    ]

    languages = [lang[0] for lang in settings.LANGUAGES]
    domain = request.scheme + "://" + request.get_host()

    xml = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')

    for lang in languages:
        for name in urls:
            path = reverse(name)
            loc = f"{domain}/{lang}{path}"
            xml.append("<url>")
            xml.append(f"<loc>{loc}</loc>")
            xml.append("<changefreq>monthly</changefreq>")
            xml.append("<priority>0.8</priority>")
            xml.append("</url>")

    xml.append("</urlset>")

    return HttpResponse("\n".join(xml), content_type="application/xml")


def robots_txt(request):
    content = render_to_string(
        "robots.txt",
        {
            "sitemap_url": request.scheme
            + "://"
            + request.get_host()
            + "/sitemap.xml"
        },
    )
    return HttpResponse(content, content_type="text/plain")
