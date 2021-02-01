from django.conf.urls import url

from user.views import questionaire_submit
from user.views import user,answer_save

# router = DefaultRouter()
# router.register(r'questionnaire', views.QuestionContentViewSet, basename='questionnaire')

urlpatterns = [
    url('/questions', user, name='questions'),
    # url(r'/questionaire_submit$', questionaire_submit, name='questionaire_submit'),
    url(r'/answer_save$', answer_save, name='answer_save'),
    # url(r'/visualization', visualization, name='visualization')
]