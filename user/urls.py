from django.conf.urls import url

from user.views import questionaire_submit

# router = DefaultRouter()
# router.register(r'questionnaire', views.QuestionContentViewSet, basename='questionnaire')

urlpatterns = [
    url(r'/questionaire_submit$', questionaire_submit, name='questionaire_submit'),
]