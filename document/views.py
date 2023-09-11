from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from  rest_framework.authentication import TokenAuthentication
from django.contrib.auth.models import User
from .models import Document
from .serializers import DocumentSerializer, DocumentCreationSerializer,DocumentContentSerializer

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
                content=serializer.validated_data['content'],
            )
            document.save()
            document.shared_with.set(serializer.validated_data['shared_with'])
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

class DocumentSharedUsersView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes=[TokenAuthentication]

    def get(self, request, unique_id):
        document = get_object_or_404(Document, unique_id=unique_id, owner=request.user)
        shared_users = document.shared_with.exclude(id=request.user.id)
        shared_user_phones = [user.username for user in shared_users]
        return Response({'shared_users': shared_user_phones})
    

class DocumentShareView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes=[TokenAuthentication]

    def post(self, request, unique_id):
        document = get_object_or_404(Document, unique_id=unique_id, owner=request.user)
        data = request.data.get('shared_users', [])
        valid_users = []
        for phone in data:
            try:
                user = User.objects.get(username=phone)
                valid_users.append(user)
            except User.DoesNotExist:
                return Response({'message': f'Invalid mobile number: {phone}'}, status=status.HTTP_400_BAD_REQUEST)
        document.shared_with.set(valid_users)
        return Response({'message': 'Document shared successfully'})
    
class SharedDocumentsListView(generics.ListAPIView):
    serializer_class = DocumentSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes=[TokenAuthentication]

    def get_queryset(self):
        return Document.objects.filter(shared_with=self.request.user)
    

class ViewDocument(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, unique_id):
        document = get_object_or_404(Document, unique_id=unique_id)
        if request.user == document.owner or request.user in document.shared_with.all():
            serializer = DocumentContentSerializer(document)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'You do not have access to this document.'}, status=status.HTTP_403_FORBIDDEN)