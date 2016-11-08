# ekalay-finance
This is the eKalay Finance Module test project.

## Notes
- To install dependencies, do ```$ pip install -U -r requirements.txt```.

## How to Run Server

### Via Codeanywhere

#### Option 1
1. Press the Run Project play button beside the Project Config button above.
2. The website will be live at https://ekalay-finance-jrmanrique.codeanyapp.com/finance/.

#### Option 2
1. Open the terminal: right click the ekalay-finance tab at the left side of the interface then choose SSH Terminal.
2. Run this command on the terminal: ```$ python3 manage.py runserver 0.0.0.0:3000```
3. The website will be live at https://ekalay-finance-jrmanrique.codeanyapp.com/finance/.

### Via Local

#### Option 1
1. Run this command on the terminal: ```$ python3 manage.py runserver```.
2. The website will be live at http://127.0.0.1:8000/ and can only be accessed in the machine.

#### Option 2
1. Find your local network address using ```$ ifconfig``` (```ipconfig``` for Windows).
2. Run this command on the terminal: ```$ python3 manage.py runserver {inet addr}:8000```. Any port will do.
3. The website will be live at [http://{inet addr}:8000/]() and can be accessed by any device connected to the local network.
