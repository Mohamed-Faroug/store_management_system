# 🏪 Inventory Management System

A comprehensive inventory and sales management system with advanced POS capabilities and professional invoicing system.

## ✨ Key Features

### 🛒 Point of Sale (POS)
- **User-friendly interface** with 3×3 product layout
- **Smart shopping cart** with quantity control and deletion
- **Automatic calculation** of taxes and discounts
- **Quick search** by name or code
- **Category filtering** for easy navigation

### 📊 Dashboard
- **Comprehensive statistics** for sales and inventory
- **Daily sales** with real-time updates
- **Best-selling products** with performance analysis
- **Low stock alerts** for supply control
- **Recent invoices** with complete details

### 📋 Inventory Management
- **Add and edit products** with images and descriptions
- **Product categorization** in organized categories
- **Inventory tracking** with reorder levels
- **Purchase recording** with supplier details
- **Manual inventory adjustment** when needed

### 🧾 Invoicing System
- **Professional invoice creation** with customer details
- **Multiple print formats** (A4 and 58mm)
- **Data export** in various formats
- **Sales tracking** with detailed reports
- **Automatic backups** of data

### 👥 User Management
- **Advanced role system** (Admin and Cashier)
- **Specific permissions** for each role
- **Secure login** with data protection
- **User management** with add and edit capabilities

## 🚀 Installation and Setup

### Requirements
- Python 3.8 or higher
- SQLite (included with Python)
- Modern web browser

### Quick Installation

1. **Clone the project**
```bash
git clone https://github.com/yourusername/inventory-system.git
cd inventory-system
```

2. **Install requirements**
```bash
pip install -r requirements.txt
```

3. **Run the application**
```bash
python run.py
```

4. **Open browser**
```
http://127.0.0.1:5000
```

### Windows Installation

1. **Run install script**
```bash
install.bat
```

2. **Start application**
```bash
start.bat
```

## 📁 Project Structure

```
inventory-system/
├── app/                          # Main application
│   ├── __init__.py              # Flask configuration
│   ├── models/                  # Data models
│   │   └── database.py          # Database management
│   ├── static/                  # Static files
│   │   ├── css/
│   │   │   └── style.css        # CSS styles
│   │   └── js/
│   │       └── main.js          # JavaScript
│   ├── templates/               # HTML templates
│   │   ├── base.html           # Base template
│   │   ├── dashboard.html      # Dashboard
│   │   ├── categories/         # Category pages
│   │   ├── invoices/           # Invoice pages
│   │   ├── items/              # Product pages
│   │   ├── sales/              # Sales pages
│   │   └── users/              # User pages
│   ├── utils/                  # Utility functions
│   │   └── auth.py             # Authentication system
│   └── views/                  # View controllers
│       ├── main.py             # Main page
│       ├── sales.py            # Sales management
│       ├── invoices.py         # Invoice management
│       ├── items.py            # Product management
│       └── users.py            # User management
├── backups/                     # Backup files
├── config.py                    # Application settings
├── backup.py                    # Backup system
├── run.py                       # Main run file
├── start.bat                    # Quick start (Windows)
├── requirements.txt             # Python requirements
├── inventory.db                 # Database
└── README.md                    # This file
```

## 🔧 Configuration

### Database Settings
```python
# config.py
DATABASE_PATH = 'inventory.db'
SECRET_KEY = 'your-secret-key-here'
```

### Backup Settings
```python
# backup.py
BACKUP_DIR = 'backups'
BACKUP_RETENTION_DAYS = 30
```

## 👤 Default Users

### System Administrator
- **Username:** admin
- **Password:** admin123
- **Permissions:** All permissions

### Cashier
- **Username:** cashier
- **Password:** cashier123
- **Permissions:** Sales and invoices only

## 📱 Usage

### 1. Login
- Open browser and navigate to `http://127.0.0.1:5000`
- Use default user credentials
- Change password after first login

### 2. Product Management
- Navigate to "Products" from menu
- Add new products with details
- Categorize products appropriately
- Set reorder levels

### 3. Point of Sale
- Navigate to "Point of Sale" from menu
- Search products or use filtering
- Add products to cart
- Calculate total and complete sale

### 4. Invoice Management
- View all invoices from "Invoices"
- Print invoices in required format
- Export data for analysis

## 🔒 Security

### Data Protection
- **Password encryption** using bcrypt
- **Secure sessions** with Flask-Session
- **CSRF protection** with Flask-WTF
- **Database encryption** (optional)

### Backups
- **Automatic backups** daily
- **Data compression** to save space
- **Easy restoration** when needed
- **Backup encryption** (optional)

## 📊 Reports

### Sales Reports
- **Daily sales** with product details
- **Weekly sales** with trend analysis
- **Monthly sales** with period comparison
- **Yearly sales** with comprehensive statistics

### Inventory Reports
- **Low stock products** with alerts
- **Best-selling products** with performance analysis
- **Purchase reports** with supplier details
- **Adjustment reports** with change logs

## 🛠️ Development

### Adding New Features
1. **Create new Blueprint** in `app/views/`
2. **Add templates** in `app/templates/`
3. **Update menu** in `base.html`
4. **Add permissions** in `auth.py`

### Customizing Design
1. **Modify CSS** in `app/static/css/style.css`
2. **Add JavaScript** in `app/static/js/main.js`
3. **Customize templates** in `app/templates/`

## 🐛 Troubleshooting

### Common Issues

#### Application won't start
```bash
# Check Python
python --version

# Check requirements
pip install -r requirements.txt

# Check port
netstat -an | findstr :5000
```

#### Database issues
```bash
# Recreate database
rm inventory.db
python -c "from app.models.database import init_db; init_db()"
```

#### Backup issues
```bash
# Run backup manually
python backup.py
```

## 📞 Support

### Getting Help
- **GitHub Issues:** Report problems
- **Documentation:** Detailed documentation
- **Community:** Discussions and questions

### Contributing
1. **Fork** the project
2. **Create branch** for new feature
3. **Commit** changes
4. **Push** to branch
5. **Create Pull Request**

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Flask** - Python web framework
- **Bootstrap** - CSS library
- **SQLite** - Database
- **Bootstrap Icons** - Icons

## 📈 Development Roadmap

### Next Release
- [ ] Mobile application
- [ ] Advanced API
- [ ] Advanced reports
- [ ] Multi-currency support
- [ ] Payment system integration

### Future Releases
- [ ] AI-powered forecasting
- [ ] Advanced data analytics
- [ ] E-commerce integration
- [ ] Multi-language support

---

**This system has been carefully developed to be a comprehensive tool for inventory and sales management. We hope it will be useful for your business! 🚀**