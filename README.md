# Stock Dashboard

Welcome to my visual stock information dashboard!  

<p>This project uses Python to access polygon.io's free RESTful API, collect data on a specified stock, and display it on the dashboard. It also uploads the opening/closing price of a stock to a MySQL database if it has not been added to the database already. Now, there are a few notes on the functionality of this project.</p>

1. If you choose to download/clone this repository, you will need to get an API key from [polygon.io](https://polygon.io/) in order to access the data. I am using the free one, which comes with its own set of caveats:
    - The free version of polygon's API limits you to 5 API calls per minute.
    - It also only gives you End of Day data, meaning if it is 11:00 AM EST on a certain day you will not be able to view data on any stock for that day. You must wait for the market to close at 4:30 PM EST.
2. In dashboard -> api_requests.py, comment out <code>from dashboard import key_vault</code>. That is where *my* key is saved on my local repository, which I have added to the gitignore file. You can create add you key to this file by ediiting line 4 as <code>key = insert your key here</code>.
3. I recommed creating a [virtual environment](https://docs.python.org/3/library/venv.html) with Python and installing all the requirements in that virtual environment with <code>pip install requirements.txt</code>. You can then run the program in the command line. All the steps would look like this:
    cd C:\...\Stock_Dashboard
    (name_of_your_virtual_env)\Scripts\activate.bat
    pip install requirements.txt
    python server.py
4. Then, go to the link that the command line provides to run view the dashboard.
Done!
