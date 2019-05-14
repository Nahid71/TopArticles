# TopArticles
This application  scrape top articles from GITHUB, REDDIT and HACKER NEWS  every day and rander it home page

## For Install
run commend:
  1. git clone github.com/Nahid71/TopArticles.git
  2. pip install -r requirements/dev.txt
  3. python manage.py migrate
  4. python manage.py loaddata services.json
### For running crawl manually run:
  5. python manage.py crawl reddit hn github
### Finaly run:
  6. python manage.py runserver
Thats it Now its running at http://127.0.0.1:8000
