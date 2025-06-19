# Expense Tracker

A comprehensive web application for tracking personal expenses built with Flask, Alpine.js, and Bootstrap 5.

## Features

- **User Authentication**: Secure registration and login system
- **Expense Management**: Add, edit, delete, and categorize expenses
- **Data Visualization**: Interactive charts and analytics
- **Export Functionality**: Export data to CSV format
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Search & Filter**: Advanced filtering options for expense data
- **Category Management**: Custom expense categories with color coding

## Technology Stack

### Backend
- **Flask**: Python web framework
- **SQLAlchemy**: Database ORM
- **Flask-Login**: User session management
- **Flask-Bcrypt**: Password hashing
- **SQLite**: Database (easily configurable to other databases)

### Frontend
- **Alpine.js**: Reactive JavaScript framework
- **Bootstrap 5**: CSS framework for responsive design
- **Chart.js**: Data visualization
- **Bootstrap Icons**: Icon library

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Quick Setup

1. **Clone or download the project**
   ```powershell
   # If using git
   git clone <repository-url>
   cd expense-tracker
   ```

2. **Run the setup script**
   ```powershell
   .\setup.ps1
   ```

   This script will:
   - Create a virtual environment
   - Install all dependencies
   - Initialize the database with default categories
   - Set up the project structure

3. **Start the application**
   ```powershell
   # Make sure virtual environment is activated
   .\venv\Scripts\Activate.ps1
   
   # Run the application
   python run.py
   ```

4. **Access the application**
   Open your web browser and go to: http://127.0.0.1:5000

### Manual Setup

If you prefer to set up manually:

1. **Create virtual environment**
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

2. **Install dependencies**
   ```powershell
   pip install -r requirements.txt
   ```

3. **Initialize database**
   ```powershell
   python init_db.py
   ```

4. **Run application**
   ```powershell
   python run.py
   ```

## Project Structure

```
expense-tracker/
├── app/
│   ├── __init__.py          # Application factory
│   ├── models/              # Database models
│   │   ├── user.py          # User model
│   │   └── expense.py       # Expense and Category models
│   ├── routes/              # Route handlers
│   │   ├── auth.py          # Authentication routes
│   │   ├── main.py          # Main application routes
│   │   └── api.py           # API endpoints
│   └── utils/               # Utility functions
│       └── validators.py    # Form validation
├── static/                  # Static files
│   ├── css/
│   │   └── style.css        # Custom styles
│   └── js/
│       └── app.js           # Custom JavaScript
├── templates/               # HTML templates
│   ├── base.html            # Base template
│   ├── index.html           # Home page
│   ├── dashboard.html       # Dashboard
│   ├── expenses.html        # Expense management
│   ├── analytics.html       # Analytics page
│   ├── categories.html      # Category management
│   ├── export.html          # Export page
│   └── auth/                # Authentication templates
├── tests/                   # Test files
├── requirements.txt         # Python dependencies
├── setup.ps1               # Setup script
├── run.py                  # Application entry point
├── init_db.py              # Database initialization
└── README.md               # This file
```

## Usage

### Getting Started

1. **Register an Account**
   - Click "Get Started" on the home page
   - Fill in your details and create an account

2. **Add Your First Expense**
   - Go to the Dashboard
   - Click "Add Expense"
   - Fill in the expense details and select a category

3. **View and Manage Expenses**
   - Use the "Expenses" page to view all your expenses
   - Search, filter, and sort your expenses
   - Edit or delete expenses as needed

4. **Analyze Spending**
   - Visit the "Analytics" page for visual insights
   - View monthly trends and category breakdowns

5. **Export Data**
   - Use the "Export" page to download your data
   - Choose between CSV formats

### Default Categories

The application comes with pre-defined categories:
- Food & Dining
- Transportation
- Shopping
- Entertainment
- Bills & Utilities
- Healthcare
- Education
- Travel
- Home & Garden
- Other

You can add, edit, or customize categories in the Categories section.

## API Endpoints

### Authentication
- `POST /auth/login` - User login
- `POST /auth/register` - User registration
- `GET /auth/logout` - User logout

### Expenses
- `GET /api/expenses` - Get expenses (with filtering)
- `POST /api/expenses` - Create new expense
- `PUT /api/expenses/<id>` - Update expense
- `DELETE /api/expenses/<id>` - Delete expense

### Categories
- `GET /api/categories` - Get all categories
- `POST /api/categories` - Create new category

### Export
- `GET /api/export/csv` - Export expenses as CSV

### Statistics
- `GET /api/stats/summary` - Get summary statistics

## Development

### Running Tests
```powershell
# Install test dependencies
pip install pytest pytest-flask

# Run tests
python -m pytest tests/
```

### Code Style
The project follows PEP 8 Python style guidelines. Key conventions:
- Use 4 spaces for indentation
- Maximum line length of 100 characters
- Descriptive variable and function names
- Comprehensive docstrings for functions and classes

### Database Schema

#### Users Table
- id (Primary Key)
- username (Unique)
- email (Unique) 
- password_hash
- first_name
- last_name
- created_at
- is_active

#### Categories Table
- id (Primary Key)
- name (Unique)
- description
- color (Hex code)
- created_at

#### Expenses Table
- id (Primary Key)
- title
- description
- amount (Decimal)
- date
- user_id (Foreign Key)
- category_id (Foreign Key)
- created_at
- updated_at

## Configuration

### Environment Variables
Create a `.env` file in the root directory:

```
SECRET_KEY=your-super-secret-key-here
DATABASE_URL=sqlite:///expense_tracker.db
FLASK_ENV=development
```

### Database Configuration
By default, the application uses SQLite. To use a different database:

1. Update the `DATABASE_URL` in your `.env` file
2. Install the appropriate database driver
3. The application will automatically create the necessary tables

## Security Features

- Password hashing using bcrypt
- CSRF protection
- User session management
- Input validation and sanitization
- SQL injection prevention through ORM

## Browser Compatibility

The application is compatible with:
- Chrome/Chromium (recommended)
- Firefox
- Safari
- Edge

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## License

This project is open source and available under the [MIT License](LICENSE).

## Support

For issues, questions, or contributions, please create an issue in the project repository.

## Roadmap

Future enhancements planned:
- [ ] PDF export functionality
- [ ] Budget tracking and alerts
- [ ] Recurring expense templates
- [ ] Mobile app (React Native)
- [ ] Multi-currency support
- [ ] Advanced analytics and reporting
- [ ] Data backup and sync
- [ ] Receipt photo upload
- [ ] Bank account integration
