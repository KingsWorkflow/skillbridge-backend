from django.shortcuts import render


def mission_view(request):
    return render(request, 'pages/mission.html')


def our_story_view(request):
    return render(request, 'pages/our_story.html')


def success_stories_view(request):
    return render(request, 'pages/success_stories.html')


def legal_view(request):
    return render(request, 'pages/legal.html')


def privacy_policy_view(request):
    return render(request, 'pages/privacy_policy.html')


def terms_of_service_view(request):
    return render(request, 'pages/terms_of_service.html')
