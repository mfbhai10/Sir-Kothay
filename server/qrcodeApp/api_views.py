from pathlib import Path

from django.contrib.staticfiles import finders
from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from django.utils.text import slugify
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import BaseRenderer, BrowsableAPIRenderer, JSONRenderer
from rest_framework.response import Response

from dashboard.models import UserDetails

from .models import QRCode
from .public_broadcast_url import public_broadcast_qr_url
from .qr_utils import compose_qr_png_with_center_logo
from .serializers import QRCodeSerializer


class QrPngRenderer(BaseRenderer):
    """So Accept: image/png satisfies DRF content negotiation (default JSON/HTML do not)."""
    media_type = 'image/png'
    format = 'png'
    charset = None

    def render(self, data, accepted_media_type=None, renderer_context=None):
        if isinstance(data, (bytes, memoryview)):
            return bytes(data)
        if data is None:
            return b''
        raise TypeError('QrPngRenderer expects bytes')


class QRCodeViewSet(viewsets.ModelViewSet):
    """
    API endpoint for QR code management
    """
    queryset = QRCode.objects.all()
    serializer_class = QRCodeSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Filter queryset to show user's own QR code or all if staff"""
        if self.request.user.is_staff:
            return QRCode.objects.all()
        return QRCode.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_qrcode(self, request):
        """Get current user's QR code"""
        try:
            qr_code = QRCode.objects.get(user=request.user)
            serializer = QRCodeSerializer(qr_code)
            return Response(serializer.data)
        except QRCode.DoesNotExist:
            return Response({'error': 'QR code not found'}, status=status.HTTP_404_NOT_FOUND)

    @action(
        detail=False,
        methods=['get'],
        permission_classes=[IsAuthenticated],
        url_path='qr_png',
        renderer_classes=[QrPngRenderer, JSONRenderer, BrowsableAPIRenderer],
    )
    def qr_png(self, request):
        """
        Return the current user's QR PNG bytes. Used by the dashboard canvas export so the image
        is fetched from the API origin (JWT + CORS) instead of /media/, which often taints canvas.
        """
        qr_code = get_object_or_404(QRCode, user=request.user)
        if not qr_code.image:
            return Response({'error': 'No QR image'}, status=status.HTTP_404_NOT_FOUND)
        try:
            with qr_code.image.open('rb') as fh:
                data = fh.read()
        except FileNotFoundError:
            return Response({'error': 'QR file missing'}, status=status.HTTP_404_NOT_FOUND)
        return Response(
            data,
            content_type='image/png',
            headers={'Cache-Control': 'private, max-age=120'},
        )

    @action(
        detail=False,
        methods=['get'],
        permission_classes=[IsAuthenticated],
        url_path='footer_png',
        renderer_classes=[QrPngRenderer, JSONRenderer, BrowsableAPIRenderer],
    )
    def footer_png(self, request):
        """
        Branded footer PNG for the “QR with user info” canvas export (client/static/images/qr/footer.png).
        Served via the API so the dashboard can fetch it with the same JWT + CORS path as qr_png.
        """
        rel = 'images/qr/footer.png'
        found = finders.find(rel)
        if not found:
            return Response(
                {'error': f'Static asset not found: {rel}'},
                status=status.HTTP_404_NOT_FOUND,
            )
        try:
            data = Path(found).read_bytes()
        except OSError as exc:
            return Response(
                {'error': 'Could not read footer image', 'detail': str(exc)},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )
        return Response(
            data,
            content_type='image/png',
            headers={'Cache-Control': 'public, max-age=86400'},
        )

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def generate(self, request):
        """Generate or regenerate QR code: encodes this user's public broadcast URL (scannable link)."""
        user = request.user
        user_details = get_object_or_404(UserDetails, user=user)
        slug = user_details.slug
        if not slug:
            return Response(
                {'message': 'Public profile slug is not ready yet. Save your profile and try again.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        url_to_encode = public_broadcast_qr_url(request, slug)
        buffer = compose_qr_png_with_center_logo(url_to_encode)

        qr_code, _created = QRCode.objects.get_or_create(user=user)
        safe_name = slugify(str(user.username), allow_unicode=False) or 'user'
        filename = f'qr_{user.id}_{safe_name}.png'
        qr_code.image.save(filename, ContentFile(buffer.read()), save=True)

        serializer = QRCodeSerializer(qr_code)
        return Response({
            'message': 'QR code generated successfully',
            'qr_code': serializer.data,
            'public_profile_url': url_to_encode,
        })
