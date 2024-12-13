# **Evently: Comprehensive Event Management Application**

![Evently Logo](static/assets/logo.svg)

Evently is a robust event management platform designed to simplify the process of organizing, discovering, and attending events. With its advanced features, intuitive interface, and dynamic workflows, Evently ensures a seamless experience for organizers and attendees alike.

---

## **Table of Contents**
1. [Features](#features)
2. [Tech Stack](#tech-stack)
3. [Project Structure](#project-structure)
4. [Installation](#installation)
5. [What I Learned](#what-i-learned)
6. [Additional Information](#additional-information)

---

## **Features**

Evently is a feature-rich platform built to handle event management efficiently. Below is a detailed breakdown of its key features:

1. **Event Management**:
   - Role-based functionality:
     - **Organizers**: Create, edit, and delete events; manage attendees.
     - **Attendees**: Register for events, mark attendance, and rate events.
     - **Admins**: Moderate events and users through an enhanced admin panel.
   - Complex database relationships between users, events, attendees, and payments ensure scalability and dynamic workflows.

2. **Dynamic Frontend**:
   - **Filtering and Searching**: Users can filter and search events by type, price, and status for a tailored experience.
   - **Pagination**: Explore events in a paginated format, optimized for scalability and responsiveness.
   - **Dynamic Event Pages**: Content adjusts based on the user’s role (organizer, attendee, or guest) and event status (upcoming, ongoing, or completed).

3. **Payments and Feedback**:
   - Supports payment workflows for paid events, enhancing real-world applicability.
   - Allows attendees to rate events dynamically, ensuring only eligible users provide feedback.

4. **File Uploading**:
   - Profile images and event thumbnails can be uploaded and managed dynamically.

5. **Profile and Settings Pages**:
   - A personalized profile page displays user details, organized events, attended events, and attendance statistics.
   - Settings allow users to update usernames, reset passwords, and delete accounts securely.

6. **Enhanced Admin Panel**:
   - Custom branding with an updated admin site header and title.
   - Enhanced search, filtering, and display options for models in the admin panel.
   - Image previews for user profile pictures.

7. **Advanced Django Features**:
   - Utilizes properties on models for dynamic calculations, such as `is_completed`, `rating`, and `isfree`.
   - Django Messages Framework provides styled feedback for actions like successful registrations or errors.
   - Django Humanize formats numbers for better readability, such as prices and attendee counts.

8. **Mobile-Responsive Design**:
   - Fully responsive frontend ensures optimal usability across all screen sizes.

9. **Dedicated Landing Page**:
   The **landing page** serves as the first touchpoint for users, showcasing Evently's value proposition through a visually compelling design. It includes:

   - **Evently Logo**: Prominently displayed at the top to reinforce branding.
   - **Hero Section**: A bold headline with call-to-action buttons guiding users to explore events or host their own.
   - **What Evently Offers Section**: Highlights core features, such as seamless event creation, vibrant community engagement, and tailored event discovery.
   - **Testimonials**: User feedback displayed dynamically to build trust and credibility.
   - **Call-to-Action Section**: Encourages new users to sign up with an enticing message and clear action button.
   - **Optimized Design**: Mobile responsiveness ensures seamless usability across devices, and structured headings improve SEO.

   This page effectively attracts, engages, and retains users by providing an immediate overview of the platform's strengths.

---

## **Tech Stack**

- **Backend**: Django (Models, Views, Authentication, Admin)
- **Frontend**: HTML, CSS, JavaScript, Bootstrap, Font Awesome
- **Database**: SQLite

---

## **Project Structure**

```plaintext
📂 evently
├── 📄 asgi.py                 # ASGI configuration for asynchronous server
├── 📄 settings.py             # Global Django settings
├── 📄 urls.py                 # Maps project-level URLs to app views
├── 📄 wsgi.py                 # WSGI configuration for production servers
📂 main
├── 📂 migrations              # Database migration files
├── 📂 templates/main          # HTML templates
│   ├── 📂 partials            # Reusable components
│   │   ├── _eventcard.html    # Displays compact event details in cards
│   │   ├── _footer.html       # Footer with social links
│   │   ├── _header.html       # Responsive navigation bar
│   │   ├── _messages.html     # Toast notifications
│   │   └── _userbadge.html    # Displays user profile details
│   ├── change_password.html   # Change password form
│   ├── change_username.html   # Change username with password verification
│   ├── create_event.html      # Event creation form
│   ├── delete_account.html    # Account deletion with password confirmation
│   ├── edit_event.html        # Edit event form for organizers
│   ├── error.html             # Generic error page
│   ├── event_details.html     # Comprehensive event details page
│   ├── explore.html           # Searchable and paginated event listings
│   ├── index.html             # Landing page with call-to-actions
│   ├── layout.html            # Base layout template
│   ├── login.html             # User login page
│   ├── payment.html           # Payment page for paid events
│   ├── profile.html           # Displays user information and stats
│   ├── settings.html          # Settings for managing account actions
│   ├── signup.html            # Registration page for new users
│   └── update_profile.html    # Profile update form
├── 📂 static
│   ├── 📂 assets              # Logos, favicon, and hero images
│   ├── 📂 css                 # Stylesheets
│   │   └── styles.css         # Custom application-wide styles
│   ├── 📂 images              # User-uploaded images (thumbnails, profiles)
│   └── 📂 js                  # JavaScript files
│       └── script.js          # Handles toast messages, validations, and dynamic actions
├── 📄 admin.py                # Customized admin configurations
├── 📄 apps.py                 # Django app configuration
├── 📄 models.py               # Database models for User, Event, Attendee, etc.
├── 📄 views.py                # Application logic
├── 📄 urls.py                 # App-level route mappings
📄 db.sqlite3                  # SQLite database file
📄 manage.py                   # Django management script
📄 requirements.txt            # Dependencies for the project
📄 README.md                   # Documentation
```

---

## **Installation**

Follow these steps to set up the project locally:

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd evently
   ```
   Or download the code as a ZIP file, extract it, and open the extracted folder.

2. **Create and Activate a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate    # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply Database Migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Run the Development Server**:
   ```bash
   python manage.py runserver
   ```

6. **Access the Application**:
   Open a browser and visit `http://127.0.0.1:8000`.

---

## **What I Learned**

- Django Humanize  
- Django Messages Framework  
- File Uploads in Django  
- Advanced Django Admin Customization  
- Search Functionality with Django  
- Partial Templates for Reusability  
- Custom Model Properties  
- Unique Together Constraint  
- Paginated Event Listings  

---

## **Additional Information**

### **Credentials**

**Superuser**:  
- **Username**: admin | **Password**: admin  

**Other Users**:  
- **Username**: tonystark | **Password**: tony  
- **Username**: harrypotter | **Password**: harry  
- **Username**: johndoe | **Password**: john  

--- 