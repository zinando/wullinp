# 🎁 WULLINP - Multi-Vendor Gifting Platform

WULLINP is a **multi-vendor gifting eCommerce platform** that allows users to create wishlists, receive contributions towards gifts, and send surprise gifts to friends. The platform ensures a seamless gifting experience with progress tracking and gift redemption.

## ✨ Features
- **User Authentication**: Register and log in using a phone number.
- **Wishlist Management**: Create, update, share, and receive contributions towards wishlist items.
- **Contribution System**: Visitors can donate towards wishlist items (Min: ₦100, Max: Item price).
- **Surprise Gifting**: Buy and send surprise gifts instantly.
- **Gift Code System**: Recipients can accept, reject, or exchange gifts before redemption.
- **Fully Responsive UI**: Mobile-first design with Tailwind CSS.

## 📌 Tech Stack
- **Backend**: Django, Django REST Framework, PostgreSQL
- **Frontend**: HTML, Tailwind CSS, JavaScript
- **Authentication**: Custom phone-based authentication
- **Deployment**: Railway, Render, or DigitalOcean

## 🚀 Getting Started
### Prerequisites
- Python 3.10+
- PostgreSQL

### Installation
```bash
# Clone the repository
git clone https://github.com/yourusername/giftflow.git
cd giftflow

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

# Install dependencies
pip install -r requirements.txt

# Run database migrations
python manage.py migrate

# Start the development server
python manage.py runserver

📜 License
This project is licensed under the MIT License - see the LICENSE file for details.

💡 Contributions are welcome! Feel free to open an issue or submit a pull request. 🎉
