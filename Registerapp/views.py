from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ProfileSerializer ,UserSerializer ,BlogSerializer ,AppointmentSerializer,StudentSerializer ,AdminSerializer,PlacementDriveSerializer
from django.views.decorators.http import require_POST
from .models import Profile ,Blog ,Appointment ,Student,Admin,PlacementDrive
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import user_passes_test 
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import status
from django.views.decorators.csrf import csrf_protect
from datetime import datetime, timedelta

@api_view(['GET', 'POST'])
def create_profile(request):
    if request.method == 'POST':
        serializer = ProfileSerializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            profile = serializer.save()
            request.session['profile_id'] = profile.id  # Store the profile ID in session
            return render(request, 'register_user.html')  # Redirect to the user creation page
        return Response(serializer.errors, status=400)
    return render(request, 'admin_profile.html')


def profile_list(request):
    profiles = Profile.objects.all()
    return render(request, 'profile_list.html', {'profiles': profiles})

@api_view(['GET', 'POST'])
@require_POST
def delete_profile(request, profile_id):
    profile = get_object_or_404(Profile, id=profile_id)
    profile.delete()
    return redirect('profile_list')



def edit_profile(request, profile_id):
    profile = get_object_or_404(Profile, id=profile_id)
    user = profile.user  # Retrieve the associated User instance

    if request.method == 'POST':
        # Update profile fields
        profile.first_name = request.POST.get('first_name')
        profile.last_name = request.POST.get('last_name')
        profile.address_line1 = request.POST.get('address_line1')
        profile.city = request.POST.get('city')
        profile.state = request.POST.get('state')
        profile.pincode = request.POST.get('pincode')
        
        if 'profile_picture' in request.FILES:
            profile.profile_picture = request.FILES['profile_picture']

        # Save profile changes
        profile.save()

        # Optionally update associated User instance
        # user.user_type = request.POST.get('username')
        # user.save()

        return redirect('dashboard')  # Redirect to dashboard or another view

    return render(request, 'edit_profile.html', {'profile': profile, 'user': user})



# @api_view(['GET', 'POST'])
# def create_profile(request):
#     if request.method == 'POST':
#         serializer = ProfileSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return redirect('dashboard')  # Redirect to a list of profiles or any other page
#         return Response(serializer.errors, status=400)
#     return render(request, 'profile_form.html')


# @login_required

@api_view(['GET', 'POST'])
def homepage(request):
    return render(request, 'home_page.html')

@api_view(['GET', 'POST'])
def success_form(request):
    return render(request, 'sucess_form.html')

@api_view(['GET', 'POST'])
def blog_create(request):
    return render(request, 'blog_upload.html')





@api_view(['GET', 'POST'])
def log_out(request):
    return render(request, 'logged_out.html')


@api_view(['GET', 'POST'])
def dashboard(request):
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        # If the profile doesn't exist, redirect to create profile page
        return redirect('create_profile')
    
    if profile.user_type == 'Patient':
        # Exclude blogs with status 'drafted' for patients
        blogs = Blog.objects.exclude(status='drafted').order_by('-created_at')
        doctors = Profile.objects.filter(user_type='Doctor')
        return render(request, 'dashboard.html', {'profile': profile, 'blogs': blogs, 'doctors': doctors})
    
    elif profile.user_type == 'Doctor':
        messages.success(request, 'Post uploaded successfully!')
        profile = request.user.profile
        # Exclude blogs with status 'drafted' for doctors
        blogs = Blog.objects.filter(username=request.user.username).order_by('-created_at')
        
        return render(request, 'doctor_dashboard.html', {'profile': profile, 'blogs': blogs})
    else:
        # Handle other user types if needed
        return redirect('home')  # Redirect to appropriate page



@api_view(['GET', 'POST'])
def create_user(request):
    profile_id = request.session.get('profile_id')
    

    profile = Profile.objects.get(pk=profile_id)
    
    username = request.data.get('username')
    password = request.data.get('password')
    confirm_password = request.data.get('confirm_password')
    
    if password != confirm_password:
        return render(request, 'register_user.html', {'error': 'Passwords do not match'})
    
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        user.set_password(password)  
        user.save()

        profile.user = user
        profile.save()
        
        login(request, user) 
        del request.session['profile_id']
        
        return redirect('dashboard')
    return Response(serializer.errors, status=400)

# def login_view(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect('dashboard')
#         else:
#             return render(request, 'login.html', {'error': 'Invalid username or password'})
#     return render(request, 'login.html')


# @api_view(['GET', 'POST'])
# def create_blog_post(request):
#     if request.method == 'POST':
#         blog_serializer = BlogSerializer(data=request.data)
#         if blog_serializer.is_valid():
#             blog_serializer.save()
#             return render(request, 'doctor_dashboard.html', {'message': "Record Submitted Successfully"})
#         return Response(blog_serializer.errors, status=400)
#     return render(request, 'blog_upload.html')

@api_view(['GET', 'POST'])
def create_blog_post(request):
    if request.method == 'POST':
        data = request.data.copy()
        data['username'] = request.user.username
        if not data.get('status'):
            data['status'] = 'published'
        
        # Print the final status
        print("Final status:", data['status'])
        blog_serializer = BlogSerializer(data=data)
        if blog_serializer.is_valid():
            blog_serializer.save()
            # print(blog_serializer)
            messages.success(request, ' Blog Post uploaded successfully!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Failed to upload post. Please check your input.')
            return Response(blog_serializer.errors, status=400)

    return render(request, 'blog_upload.html', {'user': request.user})

@api_view(['POST'])
def draft_blog(request):
    if request.method == 'POST':
        data = request.data.copy()
        data['username'] = request.user.username
        
        # Print the status from the request data
        print("Status from request:", data.get('status'))
        
        # Set status to 'drafted' if not provided or if it's None/null
        if not data.get('status'):
            data['status'] = 'drafted'
        
        # Print the final status
        print("Final status:", data['status'])
        
        blog_serializer = BlogSerializer(data=data)
        if blog_serializer.is_valid():
            blog_post = blog_serializer.save()
            # Print the saved status
            print("Saved status:", blog_post.status)
            messages.success(request, 'Blog Post saved successfully!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Failed to upload post. Please check your input.')
            return Response(blog_serializer.errors, status=400)

    return render(request, 'blog_upload.html', {'user': request.user})
    



@api_view(['GET', 'POST'])
@login_required
def edit_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id, username=request.user.username)
    
    if request.method == 'POST':
        serializer = BlogSerializer(blog, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            messages.success(request, 'Blog post updated successfully!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Failed to update blog post. Please check your input.')
            return render(request, 'edit_blog.html', {'blog': blog, 'errors': serializer.errors})
    
    # If it's a GET request, just render the form
    serializer = BlogSerializer(blog)
    return render(request, 'edit_blog.html', {'blog': serializer.data})



# @api_view(['GET', 'POST'])
# @require_POST
# def delete_blog(request, blog_id):
#     blog = get_object_or_404(Blog, id=blog_id)
#     blog.delete()
#     return JsonResponse({'success': True})

@api_view(['GET', 'POST'])
@login_required
def delete_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id, username=request.user.username)
    blog.delete()
    messages.success(request, 'Blog post deleted successfully.')
    return redirect('dashboard')


@api_view(['GET', 'POST'])
def book_appointment(request):
    if request.method == 'POST':
        # Create a mutable copy of the request data
        mutable_data = request.data.copy()

        # Calculate end_time (45 minutes after start_time)
        start_time = datetime.strptime(mutable_data['start_time'], '%H:%M')
        end_time = (start_time + timedelta(minutes=45)).strftime('%H:%M')
        mutable_data['end_time'] = end_time

        serializer = AppointmentSerializer(data=mutable_data)
        if serializer.is_valid():
            serializer.save()
            return redirect('success_form')  
        return Response(serializer.errors, status=400) 
    return render(request, 'book_appointment.html')

def check_availability(request):
    slot_booked_date = request.POST.get('slot_booked_date')
    start_time = request.POST.get('start_time')
    
    existing_appointment = Appointment.objects.filter(
        slot_booked_date=slot_booked_date,
        start_time=start_time
    ).exists()
    
    return JsonResponse({'available': not existing_appointment})

@api_view(['GET', 'POST'])
def add_student(request):
    return render(request, 'admin_profile.html')

@api_view(['GET', 'POST'])
def create_student(request):
    if request.method == 'POST':
        serializer = StudentSerializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            profile = serializer.save()
            request.session['profile_id'] = profile.id  # Store the profile ID in session
            return render(request, 'register_user.html')  # Redirect to the user creation page
        return Response(serializer.errors, status=400)
    return render(request, 'admin_profile.html')


def save_student(request):
    if request.method == 'POST':
        enrollment_id = request.POST.get('enrollmentid')
        password = request.POST.get('password')
        
        if enrollment_id and password:
            try:
                student = Student(enrollment_id=enrollment_id, password=password)
                student.save()
                messages.success(request, 'Enrollment ID and password saved successfully.')
                return redirect('sucess_form')  # Replace with the name of your success page URL pattern
            except Exception as e:
                messages.error(request, f'Error saving enrollment ID and password: {e}')
        else:
            messages.error(request, 'Please provide both enrollment ID and password.')

    return render(request, 'login.html')

@api_view(['GET', 'POST'])
def signup_student(request):
    return render(request, 'signup.html')

@api_view(['GET', 'POST'])
def signup_admin(request):
    return render(request, 'admin_signup.html')

def signup_admin(request):
    if request.method == 'POST':
        admin_id = request.POST.get('admin_id')
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        photo = request.FILES.get('photo')
        
        if admin_id and name and email and password:
            try:
                admin = Admin(admin_id=admin_id, name=name, email=email, password=password ,photo=photo)
                admin.save()
                messages.success(request, 'Admin account created successfully.')
                return redirect('home')  # Replace with the name of your success page URL pattern
            except Exception as e:
                messages.error(request, f'Error creating admin account: {e}')
        else:
            messages.error(request, 'Please fill out all fields.')

    return render(request, 'signup_admin.html')





def login_view(request):
    if request.method == 'POST':
        enrollment_id = request.POST.get('enrollment_id')
        password = request.POST.get('password')

        print(f"Login attempt with Enrollment ID: {enrollment_id} and Password: {password}")

        if enrollment_id and password:
            # Try to authenticate as a student
            try:
                student = Student.objects.get(enrollment_id=enrollment_id, password=password)
                print(f"Student authenticated: {student.enrollment_id}")
                request.session['user_id'] = student.enrollment_id
                request.session['user_type'] = 'student'
                messages.success(request, 'Login successful.')
                return redirect('student_dashboard')
            except Student.DoesNotExist:
                print(f"Student with Enrollment ID {enrollment_id} does not exist")

                # Try to authenticate as an admin
                try:
                    admin = Admin.objects.get(admin_id=enrollment_id, password=password)
                    print(f"Admin authenticated: {admin.admin_id}")
                    request.session['user_id'] = admin.admin_id
                    request.session['user_type'] = 'admin'
                    messages.success(request, 'Login successful.')
                    return redirect('admin_dashboard')
                except Admin.DoesNotExist:
                    print(f"Admin with ID {enrollment_id} does not exist")
                    messages.error(request, 'Invalid enrollment ID or password.')

    return render(request, 'login.html')

def student_dashboard(request):
    user_id = request.session.get('user_id')
    user_type = request.session.get('user_type')
    placement_drives = PlacementDrive.objects.all()
    print(f"Accessing Student Dashboard with User ID: {user_id} and User Type: {user_type}")
    
    if user_type != 'student' or not user_id:
        print("User is not authenticated as a student. Redirecting to login.")
        return redirect('login')  # Redirect to login if not authenticated

    try:
        student = Student.objects.get(enrollment_id=user_id)
        print(f"Student found: {student.enrollment_id}")
    except Student.DoesNotExist:
        print(f"Student with ID {user_id} does not exist")
        return redirect('login')  # Redirect to login if student not found
    
    return render(request, 'student_dashboard.html', {'student': student ,  'placement_drives': placement_drives})

def admin_dashboard(request):
    user_id = request.session.get('user_id')
    user_type = request.session.get('user_type')
    placement_drives = PlacementDrive.objects.all()
    print(f"Accessing Admin Dashboard with User ID: {user_id} and User Type: {user_type}")

    if user_type != 'admin' or not user_id:
        print("User is not authenticated as an admin. Redirecting to login.")
        return redirect('login')  # Redirect to login if not authenticated

    try:
        admin = Admin.objects.get(admin_id=user_id)
        print(f"Admin found: {admin.admin_id}")
    except Admin.DoesNotExist:
        print(f"Admin with ID {user_id} does not exist")
        return redirect('login')  # Redirect to login if admin not found
        
    return render(request, 'admin_dashboard.html', {'admin': admin ,  'placement_drives': placement_drives})


def update_student_profile(request):
    if request.method == 'POST':
        enrollment_id = request.POST.get('enrollment_id')
        name = request.POST.get('name')
        email = request.POST.get('email')
        city = request.POST.get('city')
        state = request.POST.get('state')
        gender = request.POST.get('gender')
        tenth_grade = request.POST.get('tenth_grade')
        twelth_grade = request.POST.get('twelth_grade')
        password = request.POST.get('password')
        resume = request.FILES.get('resume')
        profile_picture = request.FILES.get('profile_picture')

        if enrollment_id:
            try:
                student = Student.objects.get(enrollment_id=enrollment_id)
                # Update existing student
                student. name = name
                student.email = email
                student.city = city
                student.state = state
                student.gender = gender
                student.tenth_grade = tenth_grade
                student.twelth_grade = twelth_grade
                student.password = password
                if profile_picture:
                    student.profile_picture = profile_picture
                if resume:
                    student.resume = resume
                student.save()
                messages.success(request, 'Student profile updated successfully.')
            except Student.DoesNotExist:
                # Create new student
                student = Student(
                    enrollment_id=enrollment_id,
                    name=name,
                    email=email,
                    city=city,
                    state=state,
                    gender=gender,
                    password=password,
                    tenth_grade=tenth_grade,
                    twelth_grade =twelth_grade,
                    resume=resume,
                    profile_picture=profile_picture
                )
                student.save()
                messages.success(request, 'Student profile created successfully.')
        
        return redirect('admin_dashboard')

    return redirect('search_student_profile')  # Redirect to the search view if accessed directly

def search_student_profile(request):
    enrollment_id = request.GET.get('enrollment_id')
    student = None

    if enrollment_id:
        try:
            student = Student.objects.get(enrollment_id=enrollment_id)
        except Student.DoesNotExist:
            messages.error(request, 'Student not found.')

    return render(request, 'admin_profile.html', {'student': student})

def edit_student_profile(request):
    user_id = request.session.get('user_id')
    if not user_id or request.session.get('user_type') != 'student':
        return redirect('login')  # Redirect to login if not authenticated

    student = get_object_or_404(Student, enrollment_id=user_id)

    if request.method == 'POST':
        student.name = request.POST.get('name')
        student.email = request.POST.get('email')
        student.gender = request.POST.get('gender')
        student.city = request.POST.get('city')
        student.state = request.POST.get('state')
        student.tenth_grade = request.POST.get('tenth_grade')
        student.twelth_grade = request.POST.get('twelth_grade')
        student.password = request.POST.get('password')
        
        if 'resume' in request.FILES:
            student.resume = request.FILES['resume']
        if 'profile_picture' in request.FILES:
            student.profile_picture = request.FILES['profile_picture']
        
        student.save()
        messages.success(request, 'Profile updated successfully.')
        return redirect('student_dashboard')
    
    return render(request, 'edit_student_profile.html', {'student': student})

@api_view(['GET', 'POST'])
def placementdrive_page(request):
    return render(request, 'placement_drive.html')


@api_view(['GET', 'POST'])
def create_placement_drive(request):
    if request.method == 'POST':
        # Extract data from request.POST
        date = request.POST.get('date')
        time = request.POST.get('time')
        location = request.POST.get('location')
        company = request.POST.get('company')
        job_roles = request.POST.get('job_roles')
        details = request.POST.get('details')

        # Create a new PlacementDrive instance
        placement_drive = PlacementDrive(
            date=date,
            time=time,
            location=location,
            company=company,
            job_roles=job_roles,
            details=details
        )
        placement_drive.save()

        # Redirect or return a response
        return redirect('admin_dashboard')  # Replace 'success_page' with your success URL
        # Alternatively, you can return a success message directly
        # return HttpResponse("Placement Drive created successfully!")

    return render(request, 'placement_drive.html')



def edit_placement_drive(request, id):
    placement_drive = get_object_or_404(PlacementDrive, id=id)

    if request.method == 'POST':
        serializer = PlacementDriveSerializer(placement_drive, data=request.POST, partial=True)
        if serializer.is_valid():
            serializer.save()
            return redirect('admin_dashboard')
        else:
            return render(request, 'edit_placement_drive.html', {'placement_drive': placement_drive, 'errors': serializer.errors})

    return render(request, 'edit_placement_drive.html', {'placement_drive': placement_drive})

# Delete Placement Drive View
def delete_placement_drive(request, id):
    placement_drive = get_object_or_404(PlacementDrive, id=id)
    placement_drive.delete()
    return redirect('admin_dashboard')

def edit_admin_page(request):
    return render(request, 'edit_admin.html',)

def edit_admin(request, admin_id):
    admin = get_object_or_404(Admin, admin_id=admin_id)
    
    if request.method == 'POST':
        admin.name = request.POST.get('name')
        admin.email = request.POST.get('email')
        admin.password = request.POST.get('password')
        photo = request.FILES.get('photo')
        
        if photo:
            admin.photo = photo
        
        admin.save()
        messages.success(request, 'Admin profile updated successfully.')
        return redirect('admin_dashboard')
    
    return render(request, 'edit_admin.html', {'admin': admin})