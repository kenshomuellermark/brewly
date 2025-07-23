# ☕ Brewly - Study Cafe Finder

> Discover and share the perfect study cafes in your area

Brewly is a comprehensive web application that helps students and remote workers find the ideal cafes for studying and working. With interactive maps, detailed reviews, and a vibrant community, Brewly makes it easy to discover your next favorite study spot.

![Brewly Screenshot](screenshot.png)

## 🌟 Features

### 🗺️ **Interactive Map Discovery**
- **Real-time Location**: Find cafes near your current location
- **Interactive Maps**: Powered by Leaflet.js and OpenStreetMap
- **Distance Sorting**: Automatically sorts cafes by proximity
- **Address Search**: Search for cafes in any neighborhood

### ☕ **Comprehensive Cafe Profiles**
- **Detailed Information**: Name, address, description, and amenities
- **Business Hours**: Opening/closing times with "Open Now" status
- **Amenity Filters**: WiFi, power outlets, restroom availability
- **Photo Galleries**: Multiple photos per cafe with modal viewing

### ⭐ **Community Reviews**
- **5-Star Rating System**: Rate cafes from 1-5 stars
- **Written Reviews**: Share detailed experiences and tips
- **Average Ratings**: See community consensus at a glance
- **Review Management**: Edit or delete your own reviews

### 👥 **Social Features**
- **User Profiles**: Custom bio and profile pictures
- **Follow System**: Follow other users and see their activity
- **Bookmark System**: Save your favorite cafes for quick access
- **Activity Stats**: Track followers, following, and posted cafes

### 📱 **Modern Responsive Design**
- **Mobile-First**: Optimized for all screen sizes
- **Coffee Shop Aesthetic**: Warm brown color scheme with cozy vibes
- **Intuitive Navigation**: Clean, user-friendly interface
- **Accessibility**: Keyboard navigation and screen reader friendly

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Django 5.1.6
- SQLite (included with Python)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/brewly.git
   cd brewly
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Start the development server**
   ```bash
   python manage.py runserver
   ```

7. **Open your browser**
   ```
   http://127.0.0.1:8000
   ```

## 📖 User Guide

### Getting Started

#### 1. **Create Your Account**
- Click "Sign Up" in the navigation bar
- Fill in your username, email, and password
- Welcome to Brewly! 🎉

#### 2. **Set Up Your Profile**
- Click on your username in the top right
- Select "Edit Profile" to add a bio and profile picture
- Your profile shows your activity and helps others connect with you

### Finding Cafes

#### **Browse All Cafes**
- Visit the homepage to see all available cafes
- Use the search bar to find cafes by name or address
- Filter by amenities using the checkboxes (WiFi, Power, Restrooms)

#### **Use the Map**
- Click "Map" in the navigation to see all cafes on an interactive map
- Allow location access to see cafes sorted by distance
- Click the compass button (🧭) to center the map on your location
- Search for cafes in specific neighborhoods using the address search

#### **Cafe Details**
- Click on any cafe card to view detailed information
- See opening hours with current status (Open/Closed)
- Browse the photo gallery by clicking on images
- Read community reviews and ratings

### Adding Content

#### **Post a New Cafe**
- Click "+ Add Cafe" in the navigation (requires login)
- Fill in basic information: name, address, description
- Add amenities: WiFi, power outlets, restroom availability
- Set business hours
- **Interactive Map**: Drag the red marker to the exact location
- Upload a main photo
- Submit your cafe for the community!

#### **Add Photos to Existing Cafes**
- Visit any cafe detail page
- Click "+ Add Photo" in the photo gallery section
- Upload images to help others visualize the space

#### **Write Reviews**
- On any cafe detail page, find the "Add Your Review" section
- Select a star rating (1-5 stars)
- Write an optional comment about your experience
- Submit to help others make informed decisions

### Social Features

#### **Follow Other Users**
- Visit any user's profile or see them on cafe pages
- Click "Follow" to stay updated on their activity
- View your followers and following on your profile page

#### **Bookmark Cafes**
- Click the bookmark icon on any cafe detail page
- Access your saved cafes from your profile
- Perfect for creating your personal study spot list

#### **Manage Your Content**
- **Your Cafes**: Edit or delete cafes you've posted
- **Your Reviews**: Manage reviews from your profile or cafe pages
- **Your Photos**: Delete photos you've uploaded

### Profile Management

#### **Edit Your Profile**
- Update your username and email
- Add or change your profile picture
- Write a bio to tell others about yourself
- Change your password securely

## 🔧 Technical Information

### **Built With**
- **Backend**: Django 5.1.6 (Python web framework)
- **Frontend**: HTML5, CSS3, JavaScript
- **Database**: SQLite (development), PostgreSQL ready
- **Maps**: Leaflet.js with OpenStreetMap
- **Authentication**: Django's built-in user system
- **Styling**: Custom CSS with coffee shop aesthetic

### **Key Features**
- **MVT Architecture**: Clean separation of concerns
- **Responsive Design**: Mobile-first CSS approach
- **Interactive Maps**: Real-time geocoding and location services
- **Image Upload**: Multiple photo support with organized storage
- **Permission System**: Secure access control for content management
- **Search & Filter**: Advanced querying with URL parameter preservation

## 📁 Project Structure

```
brewly/
├── cafes/                          # Main Django app
│   ├── models.py                   # Database models
│   ├── views.py                    # View logic
│   ├── forms.py                    # Form definitions
│   ├── urls.py                     # URL routing
│   ├── static/cafes/css/           # Custom stylesheets
│   └── templates/                  # HTML templates
├── media/                          # User uploads
│   ├── cafes/                      # Main cafe images
│   ├── cafe_photos/                # Gallery photos
│   └── profile_pics/               # User avatars
├── static/                         # Static files
├── manage.py                       # Django management
└── requirements.txt                # Dependencies
```

## 🎯 Usage Tips

### **For Students**
- Use amenity filters to find cafes with WiFi and power outlets
- Check opening hours to ensure your study session isn't interrupted
- Read reviews for insights on noise levels and study atmosphere
- Bookmark your favorite spots for quick access

### **For Cafe Owners**
- Create detailed profiles with high-quality photos
- Keep business hours updated for accuracy
- Encourage customers to leave reviews and photos
- Respond to community feedback through the platform

### **For Contributors**
- Add photos to help others visualize spaces
- Write helpful reviews with specific details
- Follow active community members for cafe recommendations
- Keep your profile updated to build trust with other users

## 🔒 Privacy & Security

- **Data Protection**: Your personal information is securely stored
- **Content Ownership**: You retain rights to your uploaded content
- **Privacy Controls**: Manage your profile visibility and activity
- **Secure Authentication**: Passwords are encrypted and protected

## 🙏 Acknowledgments

- **OpenStreetMap**: Free geographic data for our mapping features
- **Leaflet.js**: Open-source JavaScript library for interactive maps
- **Django Community**: Excellent framework and documentation
- **Google Fonts**: Poppins and Inter font families
- **Beta Testers**: Students and cafe enthusiasts who provided valuable feedback

---

**Built with ☕ and 💻 by Kensho**

*Find your perfect place with Brewly.*
