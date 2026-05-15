import requests
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def chat_page(request):

    if 'chat_history' not in request.session:
        request.session['chat_history'] = []

    return render(request, 'ai/chat.html', {
        'chat_history': request.session['chat_history']
    })


@login_required
def chat_api(request):

    if request.method == 'POST':

        user_message = request.POST.get('message')

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

        history = request.session.get('chat_history', [])

        history.append({
            'user': user_message,
            'ai': ai_response
        })

        request.session['chat_history'] = history

        return JsonResponse({
            'user': user_message,
            'ai': ai_response
        })

    return JsonResponse({
        'error': 'Invalid request'
    })