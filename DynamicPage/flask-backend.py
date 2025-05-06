from flask import Flask, request, jsonify, send_from_directory
import os
import smtplib
from email.message import EmailMessage
import logging

app = Flask(__name__)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS', 'your-email@example.com')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD', 'your-email-password')
RECIPIENT_EMAIL = os.environ.get('RECIPIENT_EMAIL', 'your-email@example.com')

# Serve static files
@app.route('/', defaults={'path': 'index.html'})
@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

# Process contact form submissions
@app.route('/api/contact', methods=['POST'])
def contact():
    try:
        data = request.get_json()
        
        # Extract form data
        name = data.get('name')
        email = data.get('email')
        subject = data.get('subject')
        message = data.get('message')
        
        # Validate form data
        if not all([name, email, subject, message]):
            return jsonify({'status': 'error', 'message': 'All fields are required'}), 400
        
        # Send email
        send_email(name, email, subject, message)
        
        logger.info(f"Contact form submitted by {name} ({email})")
        return jsonify({'status': 'success', 'message': 'Message sent successfully'})
    
    except Exception as e:
        logger.error(f"Error processing contact form: {str(e)}")
        return jsonify({'status': 'error', 'message': 'Server error, please try again later'}), 500

def send_email(name, email, subject, message):
    """Send email with form data"""
    msg = EmailMessage()
    msg.set_content(f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}")
    
    msg['Subject'] = f"Portfolio Contact: {subject}"
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = RECIPIENT_EMAIL
    msg['Reply-To'] = email
    
    try:
        # Connect to SMTP server and send email
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        logger.info(f"Email sent successfully from {email}")
    except Exception as e:
        logger.error(f"Failed to send email: {str(e)}")
        raise

# Project data API endpoint
@app.route('/api/projects', methods=['GET'])
def get_projects():
    """Return project data in JSON format"""
    projects = [
        {
            'id': 1,
            'title': 'E-commerce Website',
            'description': 'A fully responsive e-commerce platform with product filters, cart functionality, and payment integration.',
            'image': 'project1.jpg',
            'technologies': ['Python', 'Django', 'React', 'PostgreSQL', 'Stripe API'],
            'link': 'project1.html'
        },
        {
            'id': 2,
            'title': 'Task Management App',
            'description': 'A productivity application to manage tasks with drag-and-drop functionality and progress tracking.',
            'image': 'project2.jpg',
            'technologies': ['Python', 'Flask', 'Vue.js', 'SQLite', 'Socket.io'],
            'link': 'project2.html'
        },
        {
            'id': 3,
            'title': 'Portfolio Website',
            'description': 'A personal portfolio website with dynamic content loading and interactive elements.',
            'image': 'project3.jpg',
            'technologies': ['HTML', 'CSS', 'JavaScript', 'Python'],
            'link': 'project3.html'
        }
    ]
    
    return jsonify(projects)

@app.route('/api/project/<int:project_id>', methods=['GET'])
def get_project(project_id):
    """Return detailed data for a specific project"""
    # In a real application, this would fetch data from a database
    projects = {
        1: {
            'id': 1,
            'title': 'E-commerce Website',
            'description': 'A fully responsive e-commerce platform built with Django and React.',
            'full_description': 'This e-commerce platform is a comprehensive solution for online retail businesses. Features include product filtering, cart functionality, user authentication, and payment integration with Stripe.',
            'image': 'project1.jpg',
            'screenshots': ['ecommerce-1.jpg', 'ecommerce-2.jpg', 'ecommerce-3.jpg'],
            'technologies': ['Python', 'Django', 'React', 'PostgreSQL', 'Stripe API'],
            'challenges': 'One of the main challenges was implementing real-time inventory tracking across multiple concurrent users.',
            'link': 'project1.html'
        },
        2: {
            'id': 2,
            'title': 'Task Management App',
            'description': 'A productivity application to manage tasks with drag-and-drop functionality.',
            'full_description': 'This task management application helps teams and individuals organize their work efficiently with real-time collaboration features.',
            'image': 'project2.jpg',
            'screenshots': ['taskapp-1.jpg', 'taskapp-2.jpg', 'taskapp-3.jpg'],
            'technologies': ['Python', 'Flask', 'Vue.js', 'SQLite', 'Socket.io'],
            'challenges': 'Creating the real-time collaboration feature was challenging.',
            'link': 'project2.html'
        },
        3: {
            'id': 3,
            'title': 'Portfolio Website',
            'description': 'A personal portfolio website with dynamic content loading.',
            'full_description': 'This portfolio website showcases my work and skills as a web developer with interactive elements that enhance the user experience.',
            'image': 'project3.jpg',
            'screenshots': ['portfolio-1.jpg', 'portfolio-2.jpg', 'portfolio-3.jpg'],
            'technologies': ['HTML', 'CSS', 'JavaScript', 'Python', 'Flask'],
            'challenges': 'Ensuring cross-browser compatibility and responsive design across all device types.',
            'link': 'project3.html'
        }
    }
    
    if project_id not in projects:
        return jsonify({'status': 'error', 'message': 'Project not found'}), 404
    
    return jsonify(projects[project_id])

if __name__ == '__main__':
    # Use environment variables for configuration in production
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
