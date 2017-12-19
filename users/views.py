from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, render_to_response
from django.template import RequestContext

from django.contrib.auth.decorators import login_required

from django.http import HttpResponseRedirect, Http404
from users.models import Profile, UserSubmissions

# Create your views here.
def signup(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			user = form.save()
			user.refresh_from_db()  # load the profile instance created by the signal
			user.save()
			raw_password = form.cleaned_data.get('password1')
			user = authenticate(username=user.username, password=raw_password)
			login(request, user)
			return redirect('home')
	else:
		form = UserCreationForm()
	return render(request, 'users/signup.html', {'form': form})

@login_required
def home(request):
	try:
		user = Profile.objects.get(user = request.user)
	except Profile.DoesNotExist:
		raise Http404

	if user.user_type == 0:
		try:
			submission = UserSubmissions.objects.get(profile = user)    
		except UserSubmissions.DoesNotExist:
			return render(request, 'participants/challenge.html')

		#TODO
		if submission.status == 0:
			return render(request, 'participants/submission_in_review.html')

		#TODO
		elif submission.status == 1:
			return render(request, 'participants/submission_post_review.html')

		elif submission.status == 2:
			return render(request, 'users/submission_approved.html')

	elif user.user_type == 1:
		submissions = SubmissionsReviewer.objects.filter(reviewer = user, status = 0)
		return render_to_response( 'reviewers/submission_list.html', {'submissions': submissions})

	elif user_type == 2:
		return render(request, 'administrator/home.html')

	else:
		return Http404

	return render(request, 'users/home.html')

#TODO
def submit(request):
	if request.method == 'POST':
		form = DocumentForm(request.POST, request.FILES)
		if form.is_valid():
			newdoc = Document(docfile = request.FILES['docfile'])
			newdoc.save()

			try:
				profile = Profile.objects.get(user = request.user)
			except Profile.DoesNotExist:
				raise Http404
			
			try:
				UserSubmissions.objects.create(profile = profile, submission = newdoc)
			except Exception as e:
				raise e

			return render(request, 'participants/submission_in_review.html')
	else:
		form = DocumentForm()
	
	return render(request, 'participants/challenge.html', {'form': form})

def reviews_list(request):
	submissions = UserSubmissions.objects.filter(status = 0)
	reviewers = Profile.objects.filter(user_type = 1).select_related('user')
	return render_to_response( 'administrator/submissions.html', {'submissions': submissions, 'reviewers': reviewers})

def participant_list(request):
	participants = Profile.objects.filter(user_type = 0).select_related('user')
	return render_to_response( 'administrator/participants.html', {'participants': participants})

def assign_reviewer(request):
	'''
	submission = request.POST.get('submission', )
	reviewer = request.POST.get('reviewer', )
	try:
		SubmissionsReviewer.objects.create(submission = submission, reviewer = reviewer)
	'''
	return

def promote(request):	
	return

def add_comment():
	return

def finish_review():
	return

def approve_submission():
	return
