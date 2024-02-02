from django.template.response import TemplateResponse
from django.views.decorators.http import require_GET


@require_GET
def home_view(request):
    return TemplateResponse(request, "frontpage.html")