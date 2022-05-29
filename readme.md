# Hello, and Welcome to the Project Attendance Tracking Using Face Recognition
![There was supposed to be an image here ](static/img/digital.jpg)
### Overview of the project
1. **There are 2 roles**
    1. Employee - can only check his attendance in the records
    2. Manager  - has complete access to the page.
2. **There is an option to login in the main page**
    - if employees login - Opens the profile of the employee and allows them to only view their attendance
    - if managers login  - Opens the manager's profile and allows them to go the access the features of the site. 
3. **In manager's tab, there are the following options**
   - Take attendance
   - profiles     - To view all profiles registered and also edit,delete existing or add new profiles.
   - Present      - Shows who all are Present today
   - Absent       - Shows who all are not Present today
   - History      -Shows all the entries recorded. It has 2 subfeatures
        1. Search History of a User
        1. Filter By date

4. **In Profiles tab,the manager has the following options**
    - Edit Profile
    - Delete Profile
    - Add new Profile
    - See the no. of days employees are present

5. **On clicking on Take Attendance**
    - You will be redirected to a new page where profile of employee whose attendance was last taken will be displayed
    - The Camera will turn on and try to recognise a face
    - After recognising the face, it will display the profile of the recognised face
    - The process carries on until the manager turns the camera off
  
6.  **On Clicking on Login**
    - You will be redirected to a new buffer page
    - The Camera will turn on and try to recognise a face
    - After recognising the face, it will display the profile of the recognised face
    - There will also be a dynamically loaded option based on the role of person to either view attendance(for employee) and manage attendance(for manager)
    - The person will have to turn of the camera by pressing 'q' on it after navigating to the next page.
---
# How to open the project?

1. Install Python on your PC.
2. Clone this repository into your PC.
3. Activate Virtual Environment.
4. Type ' pip install -r requirements.txt ' in the python terminal(or conda prompt) after navigating to the correct folder directory.(Make sure everything is properly installed)
> pip install -r requirements.txt 
5. Type ' python manage.py runserver ' in the terminal and open the local host.
>python manage.py runserver

---
# How to check the working of project?
1. Go to the 'media' folder and save all the images from there into other device
2. Click on Login
3. If you want to login as a manager take photos 'modi.jpg' or 'joe.jpg' and keep it in front of the camera
    1. After logging in click on 'Manage Attendance' button to navigate to manager page and then turn off camera by pressing 'q'
    2. See who all is present,absent and history.
    3. Click on take attendance and display the images from media folder one by one
    4. Keep the manager tab open in another tab and refresh it after every beep sound, you will see the attendance being marked.
    5. Turn off camera by pressing 'q' and return to home after you have displayed some images.
    6. Click on history and see whether all the images are displayed in the same order
    7. check the functioning of search by name by clicking on it and selecting a username.
    8. After that check the working of search/filter by date
    9. After Checking return to home and go to profiles section and view all the profiles
    10. Add a new profile, edit an existing profile and delete a profile to check the working
    11. After everything has been done click on exit to return to home page
4. If you want to login as employee, take any of the remaining photos and show it to the camera after clicking on login
    1. Click on the check Attendance Button.
    2. See the attendance records.
    3. Press Exit to return to the home page. 
---
# Where can the project be used?
- It can be connected to CCTV camera at the entrance of office to mark the attendance of employees and track when are they coming.
###
-- THE END --
 
>Thank you for your time and patience :)
