from django.http import JsonResponse

def build_response(messages):
    if type(messages) is not list:
        messages = [messages]
    return JsonResponse({ 'messages' : messages })

