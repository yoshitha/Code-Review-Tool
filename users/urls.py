from django.urls import path
from users import views

urlpatterns = [
	
	path('', views.home, name = 'home'),

	path('add-comment/', views.add_comment),
	path('finish/', views.finish_review),
	path('approve/', views.approve_submission),

	path('assign/', views.assign_reviewer),
	path('promote/', views.promote),
	path('submissions/', views.reviews_list),
	path('participants/', views.participant_list),

	path('submit/', views.submit),

]
