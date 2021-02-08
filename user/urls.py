from django.conf.urls import url

from user.views import questionaire_submit
# from login.views import user
from user.views import answer_save, user

# router = DefaultRouter()
# router.register(r'questionnaire', views.QuestionContentViewSet, basename='questionnaire')

urlpatterns = [
    url('/questions', user, name='questions'),
    # url(r'/questionaire_submit$', questionaire_submit, name='questionaire_submit'),
    url(r'/answer_save$', answer_save, name='answer_save'),
    # url(r'/visualization', visualization, name='visualization')
]