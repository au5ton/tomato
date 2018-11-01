![robot](img/eddie.gif)

# トマトTOMATO
Satellite from days of old, lead me to your access code!

## Functionality
This project generates QR codes for usage at a specific ᴀʀᴄᴀᴅᴇ. This project uses `selenium` for browser automation, so Chrome and selenium/webdriver must be installed.

## Dependencies
- Python 3
- pip modules specified in `requirements.txt`

## Usage
- Clone repo
- Intall pip modules: `pip install -r requirements.txt`
- Make a copy of the example .env file: `cp .env.example .env`
- Edit it as appropriately: `nano .env`
- Install and start [`chromedriver`](https://sites.google.com/a/chromium.org/chromedriver/)
- Run `./tomato.py --help` to learn about how to use
- Images are saved to the local directory

## Naming
The name is a [Cowboy Bebop reference](http://cowboybebop.wikia.com/wiki/Edward). The intention is for this project to not show up on search engines relating to the ᴀʀᴄᴀᴅᴇ. That [weird unicode](http://qaz.wtf/u/convert.cgi) text is part of that effort too.