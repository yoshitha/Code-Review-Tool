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
			#TODO
			return render(request, 'participants/challenge.html')

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

	elif user.user_type == 2:
		return render(request, 'administrator/home.html')

	else:
		return Http404

	return render(request, 'users/home.html')

# Participant views
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

# Admin views
@login_required
def reviews_list(request):
	try:
		profile = Profile.objects.get(user = request.user)
	except Profile.DoesNotExist:
		raise Http404

	if profile.user_type != 2:
		raise Http404
	
	submissions = UserSubmissions.objects.filter(status = 0)
	reviewers = Profile.objects.filter(user_type = 1).select_related('user')
	return render_to_response( 'administrator/submissions.html', {'submissions': submissions, 'reviewers': reviewers})

@login_required
def participant_list(request):
	try:
		profile = Profile.objects.get(user = request.user)
	except Profile.DoesNotExist:
		raise Http404

	if profile.user_type != 2:
		raise Http404
	
	participants = Profile.objects.filter(user_type = 0).select_related('user')
	return render_to_response( 'administrator/participants.html', {'participants': participants})

@login_required
def assign_reviewer(request):

	if request.method == POST:

		try:
			profile = Profile.objects.get(user = request.user)
		except Profile.DoesNotExist:
			raise Http404

		if profile.user_type != 2:
			raise Http404

		submission = request.POST.get('submission', None)
		reviewer = request.POST.get('reviewer', None)
		
		try:
			SubmissionsReviewer.objects.create(submission = submission, reviewer = reviewer)
		except Exception as e:
			return render_to_response( 'administrator/submissions.html', {'status': 'fail'})
		
		return render_to_response( 'administrator/submissions.html', {'status': 'success'})

	else:

		return render_to_response( 'administrator/submissions.html', {'status': 'fail'})

@login_required
def promote(request):

	if request.method == POST:

		try:
			profile = Profile.objects.get(user = request.user)
		except Profile.DoesNotExist:
			raise Http404

		if profile.user_type != 2:
			raise Http404

		participant = request.POST.get('participant', None)

		try:
			profile = Profile.objects.get(user = request.user)
		except Profile.DoesNotExist:
			raise Http404

		if profile.user_type == 0:
			profile.user_type = 1
			profile.save()

		return render_to_response( 'administrator/participants.html', {'status': 'success'})

	else:
		return render_to_response( 'administrator/participants.html', {'status': 'fail'})

# Reviewer views
#TODO
def add_comment():
	return

@login_required
def finish_review(request):
	if request.method == POST:
		try:
			profile = Profile.objects.get(user = request.user)
		except Profile.DoesNotExist:
			raise Http404

		if profile.user_type != 1:
			raise Http404

		submission = request.POST.get(submission, None)

		try:
			submission_rev = SubmissionsReviewer.objects.get(submission = submission)
			submission_rev.status = 1
			submission_rev.save()
			user_submission = UserSubmissions.objects.get(submission = submission)
			user_submission.status = 1
			user_submission.save()
		except Exception as e:
			print (e)
			raise Http404

	else:
		return redirect('home')

	return redirect('home')

@login_required
def approve_submission(request):
	if request.method == POST:
		try:
			profile = Profile.objects.get(user = request.user)
		except Profile.DoesNotExist:
			raise Http404

		if profile.user_type != 1:
			raise Http404

		submission = request.POST.get(submission, None)

		try:
			submission_rev = SubmissionsReviewer.objects.get(submission = submission)
			submission_rev.status = 2
			submission_rev.save()
			user_submission = UserSubmissions.objects.get(submission = submission)
			user_submission.status = 2
			user_submission.save()
		except Exception as e:
			print (e)
			raise Http404

	else:
		return redirect('home')

	return redirect('home')
