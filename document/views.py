from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from  rest_framework.authentication import TokenAuthentication

from .models import Document
from .serializers import DocumentSerializer, DocumentCreationSerializer

class DocumentListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes=[TokenAuthentication]
    serializer_class = DocumentSerializer

    def get_queryset(self):
        return Document.objects.filter(owner=self.request.user)

class DocumentCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes=[TokenAuthentication]
    def post(self, request):
        serializer = DocumentCreationSerializer(data=request.data)

        if serializer.is_valid():
            document = Document(
                name=serializer.validated_data['name'],
                owner=request.user,
                content=serializer.validated_data['content']
            )
            document.save()
            return Response({'unique_id': document.unique_id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DocumentDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes=[TokenAuthentication]

    def delete(self, request, unique_id):
        try:
            document = Document.objects.get(unique_id=unique_id, owner=request.user)
            document.delete()
            return Response({'message': 'Document deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Document.DoesNotExist:
            return Response({'message': 'Document not found or you do not have permission to delete it'}, status=status.HTTP_404_NOT_FOUND)
