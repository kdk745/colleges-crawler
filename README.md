# College Crawler Project

This project is a web crawler that scrapes college information and stores it in a SQLite database using Scrapy and Selenium.

## Setup Instructions

### Prerequisites

- Python 3.x
- Git

### Clone the Repository

First, clone the repository to your local machine and access the directory:

```sh
git clone https://github.com/your-username/web-crawler.git
cd web-crawler
```

### Create the Virtual Machine and Install the Packages
```
# for windows
python -m venv crawler
.\crawler\Scripts\activate

# for mac and linux
python3 -m venv crawler
source crawler/bin/activate


# install the dependencies
pip install -r requirements.txt
```

### Run the Crawler
```
cd collegescraper
scrapy crawl colleges
```


### Viewing the data
The data will be stored in a sqlite storage file `colleges-crawler\collegescraper\colleges.db`

There is a table called `colleges` inside of this database. 

If you wish to view the output in a file, simply run the command below:
```
scrapy crawl colleges -o output.json
```
The `output.json` file will be located in the same directory as `colleges.db`.

Below is a preview of the table from my own test run:

<table><tr><th>school_name</th><th>school_city</th><th>school_state</th><th>college_board_code</th><tr><tr><td>California State University: Dominguez Hills</td><td>Carson</td><td>CA</td><td>4098</td></tr><tr><td>Iowa State University</td><td>Ames</td><td>IA</td><td>6306</td></tr><tr><td>University of Texas at San Antonio</td><td>San Antonio</td><td>TX</td><td>6919</td></tr><tr><td>Indiana University South Bend</td><td>South Bend</td><td>IN</td><td>1339</td></tr><tr><td>Oakland University</td><td>Rochester</td><td>MI</td><td>1497</td></tr><tr><td>Adams State University</td><td>Alamosa</td><td>CO</td><td>4001</td></tr><tr><td>University of Saint Francis</td><td>Fort Wayne</td><td>IN</td><td>1693</td></tr><tr><td>Madonna University</td><td>Livonia</td><td>MI</td><td>1437</td></tr><tr><td>Emmaus Bible College</td><td>Dubuque</td><td>IA</td><td>1215</td></tr><tr><td>University of Southern Indiana</td><td>Evansville</td><td>IN</td><td>1335</td></tr><tr><td>University of Texas of the Permian Basin</td><td>Odessa</td><td>TX</td><td>0448</td></tr></table>

### Notes about the project
Due to the length of time to scrape the full website, I have not actually persisted all of the data.

There is a line inside of the `collegescraper\collegescraper\spiders\colleges.py` file where the crawler continues to click the 'Show More Colleges' button until no new results appear. I have chosen to only click this 10 times.
