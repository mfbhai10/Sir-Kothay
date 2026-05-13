from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils.text import slugify

from .models import QRCode
from .serializers import QRCodeSerializer


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
    
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def generate(self, request):
        """Generate or regenerate QR code for current user"""
        import qrcode
        from io import BytesIO
        from django.core.files.base import ContentFile
        from django.conf import settings
        import os
        
        # Create QR code
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        
        # Get user details for QR code data
        user = request.user
        user_data = f"Name: {user.username}\nEmail: {user.email}"
        
        try:
            user_details = user.details
            user_data += f"\nPhone: {user_details.phone_number}\nDesignation: {user_details.designation}\nOrganization: {user_details.organization}"
        except Exception:
            pass
        
        qr.add_data(user_data)
        qr.make(fit=True)
        
        # Create image
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Save to BytesIO
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        
        # Get or create QR code object
        qr_code, created = QRCode.objects.get_or_create(user=user)
        
        # Save image (filename must be filesystem-safe)
        safe_name = slugify(str(user.username), allow_unicode=False) or 'user'
        filename = f'qr_{user.id}_{safe_name}.png'
        qr_code.image.save(filename, ContentFile(buffer.read()), save=True)
        
        serializer = QRCodeSerializer(qr_code)
        return Response({
            'message': 'QR code generated successfully',
            'qr_code': serializer.data
        })
