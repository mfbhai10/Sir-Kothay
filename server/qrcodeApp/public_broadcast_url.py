"""Resolve the absolute URL encoded in user QR codes (public broadcast landing page)."""
from urllib.parse import urlencode

from django.conf import settings
from django.urls import reverse


def public_broadcast_qr_url(request, user_slug: str) -> str:
    """
    Prefer the static client page (loads profile + message via API).
    If CLIENT_PUBLIC_BASE_URL is unset, fall back to the legacy Django /broadcast/<slug>/ URL.
    """
    base = getattr(settings, 'CLIENT_PUBLIC_BASE_URL', '').strip().rstrip('/')
    if base:
        return f'{base}/broadcast/message.html?{urlencode({"user": user_slug})}'
    return request.build_absolute_uri(
        reverse('show_broadcast_messages', kwargs={'user_slug': user_slug})
    )
