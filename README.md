<div align="center">
    <a href="https://hike-logger.herokuapp.com/" target="_blank"><img src="static/images/readme/home_screenshot.png" alt="hike logger home"></a>
    <h3><a href="https://hike-logger.herokuapp.com/" target="_blank">Click here</a> to view the site on Heroku.</h3>
</div>

## Table of Contents

1. [**Introduction**](#introduction)
2. [**User Experience**](#user-experience)
    - [**User Stories**](#user-stories)
    - [**Wireframes**](#wireframes)
    - [**Design**](#design)
3. [**Features**](#features)
    - [**Existing Features**](#existing-features)
    - [**Future Features**](#future-features)
5. [**Database Schema**](#database-schema)  
6. [**Technologies Used**](#technologies-used)  
7. [**Testing**](#testing)
8. [**Deployment**](#deployment)
9. [**Credits**](#credits)
10. [**Acknowledgements**](#acknowledgements)

## Introduction

![Image](static/images/readme/mockup.png)

Hike Logger is a website that allows hiking enthusiasts in Ireland to log and store details about the hikes they have undertaken. Users can also view their stats and view hikes that their fellow hikers have added to the site. Full CRUD functionality is a feature of the site allowing users to add, edit and delete hikes. 

## User Experience

- ### User Stories

    As a **guest**, I want to be able to:

    1. View the latest hikes that have been added to the website.
    2. Register an account with the site so I can have the ability to view all of the hikes on the site and add my own.

    As a **registered user**, I want to be able to:
 
    1. Login to my account so I can create a new hike.
    2. By creating a new hike, I want to be able to:
        1. Give the hike a name.
        2. Add the hike area.
        3. Add the hike length.
        4. Add the approximate time it takes to complete the hike.
        5. Add some notes about the hike.
        6. Add a photo of the hike.
        7. Add the date I completed the hike.

    3. View all the hikes I have completed in a table that I can sort based on the hike length or time to complete.
    4. Search the table of hikes so I can filter the hikes based on the search terms.
    5. View each hike on a separate page which shows all the information on the hike.
    6. Update the information of a hike I have added to the website.
    7. Delete a hike that I have added.
    8. View statistics about my hikes such as the total amount of hikes I have completed and the average length of all my hikes.
    9. View all the hikes on the website that other users have added and be able to search and filter these hikes.
    10. Have the opportunity to mark hikes that other users have added as completed and add them to the list of my completed hikes. 
 
    As an **admin**:

    In addition to the above, I want to be able to: 

    1. Edit a hike that has been added to the website by a user.
    2. Delete a hike that has been added to the website by a user.
    3. Add a new hike category to the website such as new hike areas and times.
   

- ### Wireframes

  The wireframes for this project were created using Balsamiq.

  - [Register](https://github.com/Johnny-Morgan/hike-logger/blob/master/static/wireframes/register.pdf)

  - [Login](https://github.com/Johnny-Morgan/hike-logger/blob/master/static/wireframes/login.pdf)
  
  - [Homepage](https://github.com/Johnny-Morgan/hike-logger/blob/master/static/wireframes/home.pdf)

  - [Hikes](https://github.com/Johnny-Morgan/hike-logger/blob/master/static/wireframes/all_hikes.pdf)

  - [Profile](https://github.com/Johnny-Morgan/hike-logger/blob/master/static/wireframes/profile.pdf)

  - [Hike](https://github.com/Johnny-Morgan/hike-logger/blob/master/static/wireframes/hike.pdf)

  - [Add Hike](https://github.com/Johnny-Morgan/hike-logger/blob/master/static/wireframes/add_hike.pdf)

  - [Dashboard](https://github.com/Johnny-Morgan/hike-logger/blob/master/static/wireframes/dashboard.pdf)

  Deviations from the wireframes.

  - On the registration page, the text under the text boxes was removed to give the registration form a cleaner look.

  - Guests do not have direct access to the hikes page. The hikes page was replaced with a home page. 

  - Social media links were added to the footer.

- ### Design

  - #### Colour Scheme

    I used a green with brown colour scheme for this project which I obtained from [schemecolor](https://www.schemecolor.com/green-with-brown-color-combination.php).
    This palette has 5 colours which are Café Noir (#543B23), Pastel Brown (#846954), White Coffee (#DFDFD4), June Bud (#A5D74D) and Dark Lemon Lime (#81BE1C).
    
    ![Image](static/images/readme/palette.png)

  - #### Typography

    [Montserrat](https://fonts.google.com/specimen/Montserrat) was chosen as the main font for this website with sans-serif as the fallback font.

## Features

### Existing Features

- ### Sitewide features

  - Responsive Bootstrap Navigation bar

    The links in the navigation bar change depending on the type of user visiting the site. For a guest or a user not logged-in, the navbar displays links to the home page as well as the login and register pages. 

    ![Image](static/images/readme/navbar_logged_out.png)

     For a logged-in user, the navbar displays links to the home page, hikes page, profile page, add a hike page and the logout page. A welcome message is displayed with the user's name.

    ![Image](static/images/readme/navbar_user.png)

    For an admin, a link to the admin dashboard is displayed.

    ![Image](static/images/readme/navbar_admin.png)

    The navigation is fully responsive with a hamburger icon and dropdown menu a feature for mobile devices.

    ![Image](static/images/readme/navbar_mobile.png)


  - Footer with social media links.

  - Flash messages are featured across the site for when a user performs certain actions such as editing or deleting a hike.

  - Custom Error 403 page for if a non-admin user attempts to access the admin dashboard page.

  - Custom Error 404 page for if a user tries to open a page that does not exist.


- ### Home page

  ![Image](static/images/readme/latest.png)

  The homepage shows the last four hikes added to the website. For users that are logged-in, a button is displayed with the text view. This button redirects the user to a page that displays more information about that hike. For guests to the website, the button is replaced with a login button which redirects the user to the login page. 


- ### Hikes page

  ![Image](static/images/readme/hikes_stats.png)


  The hikes page shows stats about all the hikes on the site. The stats include the total number of hikes, the total length of all the hikes combined and the average hike length. It also displays the number of hikes for each area.


  ![Image](static/images/readme/hikes_table.png)

  A table is displayed below the hike stats which contains all the hikes on the site. The table is responsive, a user can sort the table by clicking on the table headers. This is useful if the user wants to sort the hikes by length or by time. A search bar is provided which allows the user to filter the hikes based on their search terms. This feature allows the user to see, for example, only hikes located in the Kerry area.


- ### Profile page

  ![Image](static/images/readme/profile.png)

  The profile page is similar to the hikes pages with the difference being that the profile page shows the stats and hikes relevant to the logged-in user.


- ### Hike page

  ![Image](static/images/readme/hike.png)

  Each hike on the site has its own page which displays the name, notes, stats and a picture of the hike. The stats section has a feature that displays all the registered users that have completed the hike. Below the stats card, there is a card that displays the date that the logged-in user completed the hike. The user can mark the hike as incomplete if they wish to do so.

  ![Image](static/images/readme/incomplete_btn.png)
  ![Image](static/images/readme/incomplete_form.png)

  If they have not completed the hike they have the option to do so by clicking on the complete button. This will redirect the user to a new page where they can choose a date for when they completed the hike. Marking a hike as complete will add the user's name to the 'hiked by' list in the stats section. Marking a hike as incomplete will remove them from the list. 

  ![Image](static/images/readme/complete_btn.png)
  ![Image](static/images/readme/complete_form.png)

  The user has the option to edit or delete the hike provided they are the user who added the hike to the website. If they did not add the hike, the edit and delete buttons will not be visible to them. Clicking on the 'Edit Hike' button will redirect the user to a new page where a form is displayed with the current hike details.

  ![Image](static/images/readme/edit_hike.png)

  Clicking on the 'Delete Hike' button will redirect the user to a new page to confirm they want to delete the hike.

  ![Image](static/images/readme/delete_hike.png)


- ### Add Hike page

  ![Image](static/images/readme/add_hike.png)

  A form is provided for the user to add a hike. The user must add a hike name, area, length, time, hike notes, photo URL and a date. If the user does not fill out a section of the form and tries to submit the form, a message is displayed prompting the user to complete the required field. The form can be only be submitted once each field is filled correctly. A dropdown menu is provided for the areas and times. At present, the user has three choices to choose from for the area and time. Additional areas and times can be added by an admin account.
  
  ![Image](static/images/readme/areas.png)
  
  ![Image](static/images/readme/times.png)


- ### Dashboard

  ![Image](static/images/readme/admin.jpg)

  The admin dashboard is only accessible by admin users. Here the admin can add, edit or delete hike areas and times. 

### Future features

The following are elements that could be added to the site in future development:

- An option for a user to upload a hike to Google Maps or OpenStreetMap.

- A user can upload an image instead of a URL.

- A gallery of photos or each hike.

- A user can give each hike a rating.

- Forgotten password functionality.

- A contact form to contact the site owner.

- The ability for a user to mark a hike as complete multiple times, with a different date for each time.

- An option for a user to submit the exact time they took to walk a hike and use this information to calculate the users average speed. 

- An option for a user to submit additional hike statistics such as the elevation gain, total ascent or descent.

- A section for a user to store personal notes about the hike that they can keep private or mark as public should they wish to do so.

## Database Schema

  [MongoDB](https://www.mongodb.com/1) was chosen as the database for this project. The database contains 4 collections:

  - users
  
  |       Key     |         Data Type      |   Notes                                     |
  | :-----------: | :--------------------: | :-----------------------------------------: |
  | _id           |        ObjectId        |  This is automatically generated by MongoDB |
  | username      |        String          |  The username of the user, this is created when the user chooses their username at registration. |
  | password      |        String          |  The password of the user, this is created when the user chooses their password at registration. |

 - areas
  
  |       Key     |         Data Type      |   Notes                                     |
  | :-----------: | :--------------------: | :-----------------------------------------: |
  | _id           |        ObjectId        |  This is automatically generated by MongoDB |
  | name          |        String          |  The name of the area, an area is created by an admin through the admin dashboard |

- times
  
  |       Key     |         Data Type      |   Notes                                     |
  | :-----------: | :--------------------: | :-----------------------------------------: |
  | _id           |        ObjectId        |  This is automatically generated by MongoDB |
  | time          |        String          |  The name of the time, a time is created by an admin through the admin dashboard |

- hikes
  
  |       Key     |         Data Type      |   Notes                                     |
  | :-----------: | :--------------------: | :-----------------------------------------: |
  | _id           |        ObjectId        |  This is automatically generated by MongoDB |
  | name          |        String          |  The name of the hike                       |
  | area          |        String          |  The area of the hike                       |
  | length        |        Double          |  The length of the hike to two decimal places |
  | time          |        String          |  The approximate time the hike takes to complete |
  | added_by      |        String          |  The user who added the hike                |
  | img_url       |        String          |  A URL of an image of the hike              |
  | hiked_by      |        Array           |  An array of Objects representing the users who have completed the hike. Each object has a key containing a username and a date in the form of a String |

  ![Image](static/images/readme/ERD.jpeg)


## Technologies Used

### Languages Used

- [HTML5](https://en.wikipedia.org/wiki/HTML5)

- [CSS3](https://en.wikipedia.org/wiki/Cascading_Style_Sheets)

- [JavaScript](https://www.javascript.com/)

- [Python](https://www.python.org/)

### Frameworks, Libraries & Programs Used

- [Flask](https://flask.palletsprojects.com/en/1.1.x/)

  - Flask is the framework used to develop this website.

- [jQuery](https://jquery.com/)

  - jQuery is used to simplify the JavaScript code and DOM manipulation.

  - It is also used for generating the data tables and date picker.

- [Bootstrap 4.5](https://getbootstrap.com/)

  - Bootstrap is used to assist with the responsiveness and styling of the website.

- [MongoDB](https://www.mongodb.com/)

  - MongoDB is used to store and retrieve the data used in this website.

- [Heroku](https://www.heroku.com/home)

  - Heroku is used to deploy this website.

- [GitPod](https://gitpod.io)

  - GitPod was used as the IDE for this project.

- [Git](https://git-scm.com/)

  - Git is used for version control by utilizing the Gitpod terminal to commit to Git and Push to GitHub.

- [GitHub](https://github.com/)

  - GitHub is used to store the project's code after being pushed from Git.

- [Balsamiq](https://balsamiq.com/)

  - Balsamiq is used to create the wireframes during the design process.

- [Google Fonts](https://fonts.google.com/)

  - Google Fonts is used to obtain the Montserrat font.

- [Font Awesome](https://fontawesome.com/)

  - Font Awesome is used to obtain the icons used in this website.

- [Autoprefixer](https://autoprefixer.github.io/)

  - Autoprefixer was used to add vendor prefixes.

- [GitHub Wiki TOC generator](https://ecotrust-canada.github.io/markdown-toc/)

  - Used to generate the table of contents in this document.

### Dependencies

- [click](https://click.palletsprojects.com/en/7.x/)

  - Used for creating command line interfaces.

- [dnspython](https://www.dnspython.org/)

  - Dnspython is a DNS toolkit for Python.

- [pymongo](https://pypi.org/project/pymongo/)

  - Contains tools for interacting with MongoDB database from python.

- [Flask-PyMongo](https://flask-pymongo.readthedocs.io/en/latest/)

  - Bridges Flask and PyMongo and provides some convenience helpers.

- [itsdangerous](https://readthedocs.org/projects/itsdangerous/)

  - Uses various helpers to pass data to untrusted environments and to get it back safe and sound. Data is cryptographically signed to ensure that a token has not been tampered with.

- [Werkzeug](https://werkzeug.palletsprojects.com/en/1.0.x/)

  - Werkzeug is a comprehensive WSGI web application library.

## Testing

The testing data for this project can be found in a separate file called [TESTING.md](https://github.com/Johnny-Morgan/hike-logger/blob/master/static/testing/TESTING.md).

## Deployment

### Cloning the GitHub Repository

1. Log in to GitHub and locate the projects [repository](https://github.com/Johnny-Morgan/hike-logger/).
2. Click on the Code button which is located above the list of project files.
3. Copy the URL link located under the HTTPS tab.
4. Open a terminal in your IDE. [Visual Studio Code](https://code.visualstudio.com/) is recommended.
5. Change the current working directory to the location where you want the cloned directory.
6. Type `git clone`, and paste the URL you copied in Step 3.
7. Press Enter to create your local clone.
8. Further information can be found [here](https://docs.github.com/en/free-pro-team@latest/github/creating-cloning-and-archiving-repositories/cloning-a-repository).


## Credits

### Code

- The glass effect was taken from [envatatotuts+](https://webdesign.tutsplus.com/tutorials/how-to-create-a-frosted-glass-effect-in-css--cms-32535).

- The password field regex pattern was taken [w3schools](https://www.w3schools.com/tags/tryit.asp?filename=tryhtml5_input_pattern3).

- The layout to control the position of the footer was taken from [freecodecamp](https://www.freecodecamp.org/news/how-to-keep-your-footer-where-it-belongs-59c6aa05c59c/).

- The code for the home page hero section was taken from the Code Institute [Love Running](https://www.youtube.com/watch?v=zI349F1o0YM&t=46s&ab_channel=MediaUpload) project.

- The [DataTables](https://cdn.datatables.net/) CDN was used to build the hike tables.

- The jQuery plugin to create the date picker was taken from [xdsoft](https://xdsoft.net/jqplugins/datetimepicker/).

- The code to dynamically set the active class for the navigation links was taken from [stackoverflow](https://stackoverflow.com/questions/55895502/dynamically-setting-active-class-with-flask-and-jinja2/55895621#55895621).

- The code for the 'role_required' decorator was taken from [stackoverflow](https://stackoverflow.com/questions/25233188/what-is-the-best-way-to-protect-a-flask-endpoint) and edited.

### Media

- The home page hero image is taken from [goworldtravel](https://www.goworldtravel.com/hiking-in-patagonia/).

- The background image is taken from [wikipedia](https://en.wikipedia.org/wiki/Wicklow_Way#/media/File:J_B_Malone_Memorial.jpg).

- The site logo and favicon is from [flaticon](https://www.flaticon.com/free-icon/mountains_762437?term=mountain&page=1&position=18&page=1&position=18&related_id=762437&origin=search).

## Acknowledgements

Thank you to my mentor Gerard McBride for his support and guidance during this project.

Thank you to the Code Institute Slack community for their advice and tips.

Thank you to the numerous family members and friends who tested the site.

> [Back to Top](#table-of-contents)