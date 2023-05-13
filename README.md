# Roman Provincial Coinage Scraper
This is a Python project that uses the Scrapy library to scrape the Roman Provincial Coinage website. The purpose of this project is to extract coin images and their descriptions from the website, as there are no download buttons available.

## Installation
 - Install Python 3.7 or later.
 - Clone this repository to your local machine.
 - Install the required Python libraries by running the following command in your terminal:
```
pip install scrapy
```

## Usage

- After installing scrapy, import os and scrapy as they will be used later on.
```
import scrapy
import os
```
- Navigate to the project directory in your terminal.
```
os.chdir('./WebScraper')
```
- Create a folder for keeping images
```
os.mkdir('images')
```
- Run the following command to start the scraper:
```
! scrapy crawl RPC_V4 -o file.csv -t csv
```
Wait for the scraper to finish scraping the website. The scraped data will be saved in a file named file.csv in the project directory.

## Contributing
If you want to contribute to the project, please follow these steps:

1. Fork the repository to your GitHub account.
2. Clone the forked repository to your local machine.
3. Make your changes to the source code.
4. Commit your changes and push them to your forked repository.
5. Submit a pull request to merge your changes into the main repository.
