from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .models import *
from .serializers import *
from rest_framework.exceptions import PermissionDenied
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class CreateUserView(generics.CreateAPIView):
    """
    Register a new user
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @swagger_auto_schema(
        operation_summary="Register new user",
        operation_description="Create a new user with username and password",
        request_body=UserSerializer,
        responses={201: UserSerializer},
        tags=['Authentication']
        )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)



class UserListView(generics.ListAPIView):
    """
    List all registered users (requires authentication)
    """
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="List all users",
        operation_description="Returns a list of all registered users",
        tags=['Users']
        )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class ConversationListCreateView(generics.ListCreateAPIView):
    """
    list:
    Retrieve all conversations of the logged-in user.

    create:
    Create a new conversation with exactly two participants. 
    Validates duplicates and ensures the request user is included.
    """

    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (Conversation.objects
                .filter(participants=self.request.user)
                .prefetch_related('participants'))
    
    @swagger_auto_schema(
        operation_summary="List user conversations",
        operation_description="Retrieve all conversations for the logged-in user",
        tags=['Conversations']
        )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    # create method
    @swagger_auto_schema(
        operation_summary="Create a conversation",
        operation_description="Create a conversation with exactly two participants (request user included). Validates duplicates.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['participants'],
            properties={
                'participants': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Items(type=openapi.TYPE_INTEGER),
                    description='IDs of the two participants (must include request user)'
                )
            }
        ),
        responses={
            201: ConversationSerializer,
            400: 'Bad Request (invalid participants or conversation already exists)',
            403: 'Forbidden (request user not included)'
        },
        tags=['Conversations']
    )
    def post(self, request, *args, **kwargs):
        participants_data = request.data.get('participants', [])
     
    # Check exactly two participants
        if len(participants_data) != 2:
            return Response(
                {'error': 'A conversation needs exactly two participants'},
                status=status.HTTP_400_BAD_REQUEST
            )

    # Check request user is participant
        if str(request.user.id) not in map(str, participants_data):
            return Response(
                {'error': 'You are not a participant of this conversation'},
                status=status.HTTP_403_FORBIDDEN
            )
    # Fetch users from DB
        users = User.objects.filter(id__in=participants_data)
        if users.count() != 2:
            return Response(
                {'error': 'A conversation needs exactly two participants'},
                status=status.HTTP_400_BAD_REQUEST
            )

    # Check if conversation already exists

        existing_conversation = Conversation.objects.filter(
            participants__id=participants_data[0]
        ).filter(
            participants__id=participants_data[1]
        ).distinct()

        if existing_conversation.exists():
            return Response(
                {'error': 'A conversation already exists between these participants'},
                status=status.HTTP_400_BAD_REQUEST
            )
        conversation = Conversation.objects.create()
        conversation.participants.set(users)

        #serialize the conversation
        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    


class MessageListCreateView(generics.ListCreateAPIView):
    """
    list:
    List all messages in a conversation.

    create:
    Send a new message in a conversation. Only participants can send messages.
    """
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        conversation_id = self.kwargs['conversation_id']
        conversation = self.get_conversation(conversation_id)

        return conversation.messages.order_by('timestamp')

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateMessageSerializer
        return MessageSerializer

    def perform_create(self, serializer):
        #fetch conversation and validate user participation
        print("Incoming conversation", self.request.data)
        conversation_id = self.kwargs['conversation_id']
        conversation = self.get_conversation(conversation_id)

        serializer.save(sender=self.request.user, conversation=conversation)

    def get_conversation(self, conversation_id):
        #check if user is a participant of the conversation, it helps to fetch the conversation and 
        #validate the participants
        conversation = get_object_or_404(Conversation, id=conversation_id)
        if self.request.user not in conversation.participants.all():
            raise PermissionDenied('You are not a participant of this conversation')
        return conversation
    
    @swagger_auto_schema(
        operation_summary="List messages",
        operation_description="List all messages for a conversation",
        tags=['Messages']
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Send message",
        operation_description="Send a new message in a conversation",
        request_body=CreateMessageSerializer,
        responses={201: MessageSerializer},
        tags=['Messages']
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class MessageRetrieveDestroyView(generics.RetrieveDestroyAPIView):
    """
    retrieve:
    Retrieve a single message.

    destroy:
    Delete a message if the request user is the sender.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = MessageSerializer

    def get_queryset(self):
        conversation_id = self.kwargs['conversation_id']
        return Message.objects.filter(conversation__id=conversation_id)

    def perform_destroy(self, instance):
        if instance.sender != self.request.user:
            raise PermissionDenied('You are not the sender of this message')
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
       # --- Swagger decorator for GET (retrieve) ---
    @swagger_auto_schema(
        operation_summary="Retrieve a single message",
        operation_description="Retrieve the details of a single message by message ID",
        responses={200: MessageSerializer},
        tags=['Messages']
        )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    # --- Swagger decorator for DELETE (destroy) ---
    @swagger_auto_schema(
        operation_summary="Delete a message",
        operation_description="Delete a message only if the logged-in user is the sender",
        responses={204: 'Message deleted successfully'},
        tags=['Messages']
        )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
    
    