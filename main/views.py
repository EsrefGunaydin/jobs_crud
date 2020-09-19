from django.shortcuts import render, redirect, HttpResponse
from main.models import User, Job, Category
from django.contrib import messages
import bcrypt

def index(request):
    return render(request, 'index.html')

def register(request): 
    errors = User.objects.register_validator(request.POST)
    if len(errors) > 0:
        for msg in errors:
            messages.error(request, errors[msg])
        return redirect('/')
    password = request.POST['password']
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    new_user = User.objects.create(
        first_name = request.POST['first_name'],
        last_name = request.POST['last_name'],
        email = request.POST['email'],
        password = pw_hash,
    )
    
    request.session['user_id'] = new_user.id
    return redirect('/dashboard')

def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for msg in errors:
            messages.error(request, errors[msg])
        return redirect('/')

    all_users = User.objects.filter(email = request.POST['email'])
    if len(all_users) > 0:
        user = all_users[0]
        if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
            request.session['user_id'] = user.id
            return redirect('/dashboard')
    return redirect('/')

def logout(request):
    request.session.clear()
    return redirect('/')

def dashboard(request):
    if 'user_id' not in request.session:
        return redirect('/')
    logged_user = User.objects.get(id = request.session['user_id'])
    all_jobs = Job.objects.all().order_by('-created_at')
    logged_user_jobs = Job.objects.filter(user = logged_user).order_by('-created_at')
    context = {
        'all_jobs' : all_jobs,
        'logged_user' : logged_user,
        'logged_user_jobs' : logged_user_jobs
    }
    return render(request, 'dashboard.html', context)

def newjob(request):
    all_categories = Category.objects.all()
    context = {
        'all_categories': all_categories
    }
    return render(request, 'newjob.html',context)
    

def createjob(request):
    errors = Job.objects.job_validator(request.POST)
    if len(errors) > 0:
        for msg in errors:
            messages.error(request, errors[msg])
        return redirect('/jobs/new')
    
    this_user = User.objects.get(id = request.session['user_id'])
    
    Job.objects.create(
        title = request.POST['title'],
        desc = request.POST['desc'],
        location = request.POST['location'],
        user = this_user,
    )

    Category.objects.create(name= request.POST['add_category'])
    new_category = Category.objects.last()
    this_job = Job.objects.last()
    this_job.jobs.add(new_category)
    print(request.POST.getlist('category'))
    categories = request.POST.getlist('category')
    for category in categories:
        this_job.jobs.add(category)

    return redirect('/dashboard')

def showjob(request, job_id):
    if 'user_id' not in request.session:
        return redirect('/')
    this_job = Job.objects.get(id = job_id)
    print(this_job.jobs.name)
    logged_user = User.objects.get(id = request.session['user_id'])
    context = {
        'this_job' : this_job,
        'logged_user' : logged_user
    }
    return render(request, 'showjob.html', context)

def editjob(request, job_id):
    if 'user_id' not in request.session:
        return redirect('/')
    this_job = Job.objects.get(id = job_id)
    logged_user = User.objects.get(id = request.session['user_id'])
    context = {
        'this_job' : this_job,
        'logged_user' : logged_user
    }
    return render(request, 'editjob.html', context)

def updatejob(request):
    this_job = Job.objects.get(id = request.POST['job_id'])
    this_job.title = request.POST['title']
    this_job.desc = request.POST['desc']
    this_job.location = request.POST['location']
    this_job.save()
    return redirect('/dashboard')

def addtomyjobs(request):
    logged_user = User.objects.get(id = request.session['user_id'])
    this_job = Job.objects.get(id = request.POST['job_id'])
    logged_user_jobs = Job.objects.filter(user = logged_user)
   
    if this_job not in logged_user_jobs:
        Job.objects.create(
            title = this_job.title,
            location = this_job.location,
            desc = this_job.desc,
            user = logged_user
        )
        
    print(logged_user_jobs)
    print(this_job.title)
    return redirect('/dashboard')
    
def changelist(request, job_id):
    if 'user_id' not in request.session:
        return redirect('/')
    logged_user = User.objects.get(id = request.session['user_id'])
    all_jobs = Job.objects.exclude(id=job_id).order_by('-created_at')
    logged_user_jobs = Job.objects.filter(user = logged_user).order_by('-created_at')
    excluded_jobs = []
    excluded_jobs.append(Job.objects.get(id=job_id))
    context = {
        'all_jobs' : all_jobs,
        'logged_user' : logged_user,
        'logged_user_jobs' : logged_user_jobs,
        'excluded_jobs' : excluded_jobs
    }
    return render(request, 'dashboard.html', context)

def deletejob(request):
    this_job = Job.objects.get(id = request.POST['job_id'])
    this_job.delete()
    return redirect('/dashboard')
