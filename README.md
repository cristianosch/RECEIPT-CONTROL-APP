❤️ Support and Motivation

Receipt Control App is free for everyone to use, and your support is highly appreciated. If you find the project useful, leaving a star ⭐ on the repository helps motivate the creator to keep improving and expanding the app. Every contribution, no matter how small, makes a difference!

# Receipt Control App - Django and Mindee Integration

<img src="pictures/receipt-example.png" >
    Example of payment receipt and data capture

## Overview

Receipt Control App is a Django-based project that helps users track their spending by scanning receipts using the [Mindee API](https://www.mindee.com/). This tool categorizes expenses and provides monthly comparisons of spending in areas like groceries, restaurants, and fuel stations.

## Features
- Upload a photo of a receipt, and the data will be automatically processed.
- Compare expenses month-over-month.
- Categorize spending by merchant type (e.g., supermarkets, restaurants, gas stations).
- Visualize spending trends with easy-to-read statistics and charts.

## Getting Started

### 💻 Prerequisites

To run this project locally, you’ll need:
- Python 3.x
- Django
- A Mindee account (free tier is sufficient)
- Redis

## Installation

1. Clone the repository:
   
    git clone https://github.com/cristianosch/receipt-control-app.git
    cd receipt-control-app

2. Create a virtual environment and activate it:
   
    python -m venv venv
    source venv/bin/activate  # For Windows: venv\Scripts\activate

3. Install dependencies:

    pip install -r requirements.txt

4. Set up your environment variables: Create a .env file in the root of your project and add your Mindee API key:

    MINDEE_API_KEY=your-mindee-api-key

5. Apply migrations: 
   
   python manage.py migrate

6. Run the development server:  

    python manage.py runserver

7. Open your browser and go to http://127.0.0.1:8000/ to start using Receipt Tracker.


## Redis and Celery Setup

To use Celery in this project, you need to have Redis installed as it acts as a message broker for Celery tasks. Here's how to get started:

**Installing Redis**

* For Ubuntu/Debian:

    sudo apt update
    sudo apt install redis-server

* For macOS (using Homebrew):
  
    brew install redis

* For Windows: You can use Redis for Windows or run Redis in a Docker container.

    Follow the link to download redis for windows
    https://github.com/microsoftarchive/redis/releases

   
**After installation, start the Redis server:**

    sudo service redis-server start

* You can check if Redis is running with:
   
    redis-cli ping

You should see PONG if Redis is running correctly.
    

**Get redis running**

With the project still running, open another terminal for the project and get redis working with the command

    celery -A core worker --loglevel=INFO


### Adjustments and improvements

The project is still under development and the next updates will focus on the following tasks:

- [x] Created models for the database
- [x] Prepared templates
- [x] Prepared the scenario for accepting the upload or photograph, and abstracting the data to the database
- [x] Sort receipts by month of purchase
- [x] Created tables with receipt information
- [x] Created logic to compare costs between months and years
- [x] Manual form to add itens
- [x] User creation / login / register
- [x] Celery - Installed and configured
  
## 📫 Contributing to RECEIPT-CONTROL-APP

To contribute to <RECEIPT-CONTROL-APP>, follow these steps:

1. Fork this repository.
2. Create a branch: `git checkout -b <branch_name>`.
3. Make your changes and commit them: `git commit -m '<commit_message>'`
4. Push to the original branch: `git push origin <RECEIPT-CONTROL-APP> / <local>`
5. Create the pull request.

Alternatively, see GitHub's documentation on [how to create a pull request](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request).


<img height="200px" width="400" src="pictures/dashboard.png"/>
    Main Dahsboard
<img height="200px" width="400" src="pictures/detail.png"/> 
    Details abstracted from receipts
<img height="400px" width="200px" src="pictures/dash-responsive.png"/> 
    Responsive
<img height="400px" width="200px" src="pictures/month.png"/> 
    Receipts organized by months
<img height="400px" width="200px" src="pictures/month-detail.png"/> 
    Graph with visual demonstration of expenses divided by category


