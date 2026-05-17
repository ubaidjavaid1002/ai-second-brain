import requests

from django.http import JsonResponse
from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from django.contrib.auth.decorators import login_required

from .models import Conversation, Message


@login_required
def chat_page(request, conversation_id=None):

    conversations = Conversation.objects.filter(
        user=request.user
    ).order_by('-created_at')

    active_conversation = None
    messages = []

    if conversation_id:

        active_conversation = get_object_or_404(
            Conversation,
            id=conversation_id,
            user=request.user
        )

        messages = active_conversation.messages.all()

    return render(request, 'ai/chat.html', {
        'conversations': conversations,
        'messages': messages,
        'active_conversation': active_conversation
    })


@login_required
def new_chat(request):

    conversation = Conversation.objects.create(
        user=request.user,
        title='New Chat'
    )

    return redirect(
        'conversation_detail',
        conversation_id=conversation.id
    )


@login_required
def chat_api(request):

    if request.method == 'POST':

        user_message = request.POST.get('message')

        conversation_id = request.POST.get('conversation_id')

        conversation = get_object_or_404(
            Conversation,
            id=conversation_id,
            user=request.user
        )

        try:

            response = requests.post(
                'http://localhost:11434/api/generate',
                json={
                    'model': 'llama3',
                    'prompt': user_message,
                    'stream': False
                }
            )

            data = response.json()

            ai_response = data.get('response')

        except Exception as e:

            ai_response = f'Error: {str(e)}'

        if conversation.title == 'New Chat':

            conversation.title = user_message[:30]

            conversation.save()

        Message.objects.create(
            conversation=conversation,
            user_message=user_message,
            ai_response=ai_response
        )

        return JsonResponse({
            'user': user_message,
            'ai': ai_response,
            'title': conversation.title,
            'conversation_id': conversation.id
        })

    return JsonResponse({
        'error': 'Invalid request'
    })


@login_required
def delete_chat(request, conversation_id):

    conversation = get_object_or_404(
        Conversation,
        id=conversation_id,
        user=request.user
    )

    conversation.delete()

    return redirect('chat')