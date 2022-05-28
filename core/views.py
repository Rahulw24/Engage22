from datetime import timedelta
import time
from django.shortcuts import render, HttpResponse, redirect
from .models import *
from .forms import *
import face_recognition
import cv2
import numpy as np
import winsound
from django.db.models import Q
from playsound import playsound
import os
from django.utils import timezone
from dateutil import parser

global video_capture
last_face ='no_face'
login_face ='no_face'
current_path = os.path.dirname(__file__)
sound_folder = os.path.join(current_path, 'sound/')
face_list_file = os.path.join(current_path, 'face_list.txt')
sound = os.path.join(sound_folder, 'beep.wav')

# Returns the landing page 
def index(request):
    return render(request, 'core/index.html')

#Runs login scan to recognise a employee/manager and then displays their profile
def login(request):
    global login_face
    try:
        login_face = LoginDetails.objects.last()      # last login id != Unknown
        profile = Profile.objects.get(Q(image__icontains=login_face))
    except:
        login_face = None
        profile = None
    records = LastFace.objects.all().filter(last_face=login_face)
    context = {
        'profile': profile,
        'last_face': login_face,
        'records':records
    }
    print('No face detected')
    return render(request, 'core/login.html', context)


# Returns known face names and encodings
def Known_faces():
    known_face_encodings = []
    known_face_names = []
    profiles = Profile.objects.all()
    for profile in profiles:
        person = profile.image
        image_of_person = face_recognition.load_image_file(f'media/{person}')
        person_face_encoding = face_recognition.face_encodings(image_of_person)[0]
        known_face_encodings.append(person_face_encoding)
        known_face_names.append(f'{person}'[:-4])  # removing .jpg from file name
    return [known_face_encodings ,known_face_names];

#draws a rectangle around recognised face and places the name
def show_recognised_face(frame,face_locations, face_names):
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # as we have scaled down earlier by multiplying by 0.25
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        cv2.rectangle(frame, (left, bottom - 35),
                          (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)
    cv2.imshow('Video', frame)


def initialise_frame(video_capture):
    ret, frame = video_capture.read()
    if frame.any():
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)  #reducing size so as to increase speed
        rgb_small_frame = small_frame[:, :, ::-1]  #BGR to RGB
        return frame,rgb_small_frame
    return [frame,[]]


# function to scan and store user login detais
def login_scan(request):
    print('login scan being called')
    global login_face
    [known_face_encodings, known_face_names]=Known_faces();

    video_capture = cv2.VideoCapture(0)

    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True

    while True:

        [frame,rgb_small_frame] =initialise_frame(video_capture);

        if process_this_frame:

            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
            face_names = []
            
            for face_encoding in face_encodings:
            
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                
                if matches[best_match_index]:
            
                    name = known_face_names[best_match_index]
                    profile = Profile.objects.get(Q(image__icontains=name))
                    if login_face != name:  # to avoid multiple entries when same person is in 2 consecutive frames 
                        login_face = LoginDetails(last_face=name)
                        login_face.save()
                        login_face = name
                        winsound.PlaySound(sound, winsound.SND_ASYNC)
            
                face_names.append(name)

        process_this_frame = not process_this_frame
        show_recognised_face(frame,face_locations, face_names);

        if cv2.waitKey(1) & 0xFF == ord('q'):   #Exit Mechanism
            video_capture.release()
            cv2.destroyAllWindows()
            name='Unknown'
            login_face = LoginDetails(last_face=name)
            login_face.save()   # dummy name so as to prevent loading of previous visitors' details
            break

    return HttpResponse('scaner closed', login_face)

#Returns the employees' attendance records
def employee_details(request):
    last_face=LoginDetails.objects.last();
    records=LastFace.objects.filter(last_face=last_face)
    return render(request,'core/employee_details.html',context={'records' :records,'last_face':last_face})

# Manager's Home Page
def manager(request):
    scanned = LastFace.objects.all().order_by('date').reverse()
    present = Profile.objects.filter(present=True).order_by('updated').reverse()
    absent = Profile.objects.filter(present=False).order_by('shift')
    form = DateForm()
    context = {
        'scanned': scanned,
        'present': present,
        'absent': absent,
        }
    return render(request, 'core/manager.html', context)

def clear_history(request):
    history = LastFace.objects.all()
    history.delete()
    return redirect('manager')

# Makes attendance status of all employees as absent
# Basically, start of a new day
def reset(request):
    profiles = Profile.objects.all()
    for profile in profiles:
        if profile.present == True:
            profile.present = False
            profile.save()
        else:
            pass
    return redirect('manager')


# returns records of searched name in history
def search_name(request):
    records=[]
    if request.method=="POST":
        first=request.POST.get('name');
        records=LastFace.objects.all().filter(last_face=first).order_by('date').reverse()
    profiles= Profile.objects.all();
    context = {
            'records':records,
            'profiles':profiles,
        }
    print(records)
    return render(request,'core/search_name.html',context=context)

# return records of searched date in history
def search_date(request):
    model = FilterDate
    form_class = DateForm
    form = DateForm()
    entries=[]
    if request.method == 'POST' and form.is_valid:
        req_date=request.POST.get('req_date')
        print(req_date)
        entries=LastFace.objects.filter(date__range=[req_date,str((parser.parse(req_date))+timedelta(days=1))])        
    context = {
        'date_records':entries,
        'form':form,
    }
    return render(request,'core/search_date.html',context)

# Marks attendance of employees
def mark_attendance(name):
    profile = Profile.objects.get(Q(image__icontains=name))
    if profile.present == True:
        pass
    else:
        profile.days_present+=1
        profile.present = True
        profile.save()

#function to recognise face and calls mark_attendance
def scan(request):
    print(request)
    global last_face

    [known_face_encodings, known_face_names]=Known_faces();

    video_capture = cv2.VideoCapture(0)

    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True

    while True:

        [frame,rgb_small_frame] =initialise_frame(video_capture);

        if process_this_frame:
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
            face_names = []
            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)  #least distance
                name = "Unknown"
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]
                    mark_attendance(name)
                    if last_face != name:  # to prevent multiple entries of same name if he is in 2 consecutive frames
                        last_face = LastFace(last_face=name)
                        last_face.save()
                        last_face = name
                        winsound.PlaySound(sound, winsound.SND_ASYNC)  #confirmation sound
                    else:
                        pass
                face_names.append(name)
        process_this_frame = not process_this_frame
        show_recognised_face(frame,face_locations, face_names);
        if cv2.waitKey(1) & 0xFF == ord('q'):  #Exit mechanism/Camera closing procedure
            break
    video_capture.release()
    cv2.destroyAllWindows()
    return HttpResponse('scaner closed', last_face)

def stop_scan(request):
    cv2.destroyAllWindows();
    return redirect('manager')

# Displays Employee Details after taking their attendance
def details(request):
    try:
        last_face = LastFace.objects.last()
        profile = Profile.objects.get(Q(image__icontains=last_face))
    except:
        last_face = None
        profile = None

    context = {
        'profile': profile,
        'last_face': last_face
    }
    return render(request, 'core/details.html', context)

# Renders all saved profiles
def profiles(request):
    profiles = Profile.objects.all()
    context = {
        'profiles': profiles
    }
    return render(request, 'core/profiles.html', context)

# Renders a form to add new profile
def add_profile(request):
    form = ProfileForm
    if request.method == 'POST': #if form is submitted
        form = ProfileForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('profiles')
    context={'form':form}
    return render(request,'core/add_profile.html',context)

# Loads the previously filled form and renders it to edit
def edit_profile(request,id):
    profile = Profile.objects.get(id=id)
    form = ProfileForm(instance=profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST,request.FILES,instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profiles')
    context={'form':form}
    return render(request,'core/add_profile.html',context)


def delete_profile(request,id):
    profile = Profile.objects.get(id=id)
    profile.delete()
    return redirect('profiles')


def ajax(request):
    last_face = LastFace.objects.last()
    context = {
        'last_face': last_face
    }
    return render(request, 'core/ajax.html', context)