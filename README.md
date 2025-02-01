# Recipe Sharing & Rating Platform - Backend

## Overview
This project is a backend implementation for a social media platform focused on sharing and rating recipes. It is developed using Django Rest Framework (DRF) and provides APIs for authentication, recipe management, and rating functionalities. The platform supports two types of users: **Customers** and **Sellers**.

## Features

### 1. Authentication & Authorization
- Token-based authentication for Customers and Sellers.
- Role-based permissions to restrict access.
- Rate limiting and throttling to prevent abuse.

### 2. API Development
- **Login & Logout APIs** for user authentication.
- **Recipe APIs** for Sellers to create, update, and delete recipes.
- **Recipe Retrieval API** for Customers to browse recipes.
- **Rating API** for Customers to submit ratings and reviews.

### 3. Asynchronous Tasks
- **Image Optimization**: Converts uploaded recipe images to WebP format and resizes them asynchronously using Celery.
- **Scheduled Email Notifications**: Sends daily emails at 6 AM, excluding Saturdays and Sundays.

### 4. Scheduled Services
- **Weekly Data Backup**: Exports user data to an Amazon S3 bucket in CSV format every Monday at 6 AM.

## Technologies Used
- **Backend**: Django Rest Framework (DRF)
- **Database**: PostgreSQL / MySQL
- **Task Queue**: Celery with Redis
- **Scheduling**: APScheduler
- **Storage**: Amazon S3
- **Authentication**: Token-based authentication (DRF Auth Token)

## Installation & Setup

### Prerequisites
Ensure you have the following installed:
- Python (>= 3.8)
- PostgreSQL / MySQL
- Redis (for Celery tasks)
- Amazon S3 credentials (for scheduled services)

### Steps to Run
1. Clone the repository:
   ```sh
   git clone https://github.com/your-repo.git
   cd your-repo
   ```
2. Create and activate a virtual environment:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Configure environment variables (update `.env` file):
   ```sh
   SECRET_KEY=your-secret-key
   DATABASE_URL=your-database-url
   REDIS_URL=redis://localhost:6379
   AWS_ACCESS_KEY_ID=your-aws-key
   AWS_SECRET_ACCESS_KEY=your-aws-secret
   ```
5. Apply database migrations:
   ```sh
   python manage.py migrate
   ```
6. Create a superuser (optional):
   ```sh
   python manage.py createsuperuser
   ```
7. Run the development server:
   ```sh
   python manage.py runserver
   ```
8. Start Celery worker for background tasks:
  celery -A star_clinch worker -l info -P eventlet

10. Start the scheduler for periodic tasks:
   ```sh
   python manage.py shell
   >>> from master.scheduler import start
   >>> start()
   ```

## API Endpoints

### Authentication
- `POST /api/login/` - User login
- `POST /api/logout/` - User logout

### Recipe Management
- `GET /api/recipe/` - List all recipes (Customers & Sellers)
- `POST /api/recipe/` - Create a new recipe (Sellers only)
- `PUT /api/recipe/?id=<recipe_id>` - Update an existing recipe (Sellers only)
- `DELETE /api/recipe/?id=<recipe_id>` - Delete a recipe (Sellers only)

### Ratings
- `POST /api/rating/` - Submit a rating for a recipe (Customers only)

## Scheduled Tasks
- **Daily Email Notifications**: Sends daily updates to users at 6 AM (excluding weekends).
- **Weekly Data Export**: Uploads user data to Amazon S3 every Monday at 6 AM.

## Contributing
Contributions are welcome! Please follow best practices and ensure code is well-documented before submitting pull requests.

## License
This project is licensed under the MIT License.

## Contact
For any issues or suggestions, feel free to contact: `your-email@example.com`

