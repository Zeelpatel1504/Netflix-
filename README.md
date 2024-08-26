<!DOCTYPE html>
<html>

<body>
  <h1>Netflix README</h1>
  <h2>Project Overview</h2>
  <p>A web application that provides a Netflix-like experience, allowing users to create profiles, browse and watch content, rate and review movies/series, and personalize their recommendations.</p>

  <h2>Key Features</h2>
  <ul>
    <li>User Authentication: User registration, login, and profile management.</li>
    <li>Content Management: Organized content (movies, series, dramas) with alphabetical sorting, custom ordering, and recommendations based on ratings, reviews, and viewing history.</li>
    <li>Content Filtering: Genre-based filtering and age restrictions (children, 18+).</li>
    <li>Ratings and Reviews: User ratings, reviews, and content saving for later viewing.</li>
    <li>Language Selection: Language preferences for content.</li>
    <li>Search Functionality: Search for specific content, including top-rated movies by genre.</li>
  </ul>

  <h2>Technical Details</h2>
  <ul>
    <li>Programming Language: Python (Django)</li>
    <li>Database: PostgreSQL</li>
    <li>Front-End: (Specify your front-end technologies, e.g., HTML, CSS)</li>
    <li>Additional Libraries/Frameworks: (List any relevant libraries, e.g., for streaming, authentication, etc.)</li>
  </ul>

  <h2>Installation and Usage</h2>
  <h3>Prerequisites</h3>
  <ul>
    <li>Python</li>
    <li>PostgreSQL</li>
    <li>(Other required dependencies)</li>
  </ul>

  <h3>Installation</h3>
  <ol>
    <li>Clone the repository: `git clone https://github.com/Zeelpatel1504/Netflix-Project`</li>
    <li>Set up a virtual environment: `python -m venv env`</li>
    <li>Activate the virtual environment: `source env/bin/activate` (Windows: `env\Scripts\activate`)</li>
    <li>Install dependencies: `pip install -r requirements.txt`</li>
  </ol>

  <h3>Configuration</h3>
  <p>Configure database
create a virtual env
==> py -m venv env

activate env
==> env\scripts\activate

Make Migrations
==> py manage.py makemigrations

Migrate DB
==> py manage.py migrate


  <h3>Running the Application</h3>
  <p>Start the development server: `python manage.py runserver`</p>

  </body>
</html>
