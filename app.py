from flask import Flask, render_template, request, redirect, url_for
import json

__app_id = None 

# --- FIREBASE SETUP ---
# CRITICAL: We only need the APP_ID for constructing the collection path.
# All database operations are  handled client-side.

# Default values for local development (if variables are not defined)
APP_ID = "default-app-id"
LOCAL_DEV_MODE = False

try:
    APP_ID = __app_id
    
except NameError:
    # This block executes when running locally in VS Code/terminal
    print("--- WARNING: Running in Local Dev Mode. Firebase config variables not defined. ---")
    LOCAL_DEV_MODE = True

# --- DATA STORAGE PATHS (MANDATORY FOR CANVAS) ---
def get_public_collection_path():
    """Returns the public Firestore collection path for found items."""
    return f"artifacts/{APP_ID}/public/data/found_items"


# --- FLASK APP INITIALIZATION ---
app = Flask(__name__)


# --- ROUTES ---

@app.route('/')
def home():
    # Renders the main index page (listing and search).
    return render_template('index.html', 
        title='School Lost-and-Found',
        collection_path=get_public_collection_path() # Pass path for client-side usage
    )

@app.route('/report', methods=['GET'])
def report_item():
    # Only handles the GET request to display the form.
    # Submission is handled via JavaScript in report.html.
    return render_template('report.html', 
        title='Report Found Item', 
        # Pass the collection path to the client-side JavaScript
        collection_path=get_public_collection_path() 
    )


@app.route('/success')
def success():
    return render_template('success.html', title='Submission Successful')

# --- ADMIN ROUTE (needs to be updated) ---

@app.route('/admin')
def admin_panel():
    """
    Displays the administrative view of all found items.
    The data fetching is now handled entirely client-side in admin.html.
    """
    # Pass the collection path to the client-side JavaScript
    collection_path = get_public_collection_path()
    
    
    return render_template('admin.html', 
        title='Admin Management Panel', 
        collection_path=collection_path
    )


# To run the application
if __name__ == '__main__':
    # Setting debug=True allows for automatic reloading when making changes
    app.run(debug=True)