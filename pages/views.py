import requests
import os
import time

from django.shortcuts import render
from django.conf import settings
from django.http import FileResponse
from django.utils.translation import get_language
from django.http import HttpResponse
from django.views.decorators.http import require_POST


def index(request):

    context ={
        'title': "Neverland Labs",
    }
    return render(request, 'pages/index.html', context)


def privacy(request):

    context ={
        'title': "Neverland Labs: privacy",
    }
    return render(request, 'pages/privacy.html', context)


def terms(request):

    context ={
        'title': "Neverland Labs: terms of service",
    }
    return render(request, 'pages/terms.html', context)


def development(request):

    context ={
        'title': "Neverland Labs: web development",
    }
    return render(request, 'pages/development.html', context)


def marketing(request):

    context ={
        'title': "Neverland Labs: marketing",
    }
    return render(request, 'pages/marketing.html', context)


def data(request):

    context ={
        'title': "Neverland Labs: data",
    }
    return render(request, 'pages/data.html', context)


def ux(request):

    context ={
        'title': "Neverland Labs: ux-ui",
    }
    return render(request, 'pages/ux.html', context)


def portfolio_action(request):

    context ={
        'title': "Neverland Labs: StrikeShop Action",
    }
    return render(request, 'pages/portfolio/action.html', context)


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
