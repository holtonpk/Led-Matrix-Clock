# Led Matrix Clock
A clock built using a Raspberry Pi, an LED matrix, and some other components. The main objective of this project is to create a clock with a scrolling message display that can be controlled through a web interface.

## Key Features
- Control clock through a web interface
- Set time, change scrolling message, and adjust brightness of the display

## How it works
The project utilizes a Node.js server to handle the communication between the Raspberry Pi and the web interface. The code in this repository is written in JavaScript and it contains the following files:

- `index.js`: This file is the main entry point of the program, and it starts the Node.js server and sets up the web interface.
- `server.js`: This file contains the code for the Node.js server, which handles the communication between the Raspberry Pi and the web interface.
- `public`: This folder contains the static files that are served by the web server, such as the HTML, CSS, and JavaScript files for the web interface.
- `routes`: This folder contains the code for the different routes that are handled by the web server.
- `led-matrix`: This folder contains the code for the LED matrix display.
- `config.json`: This file contains the configuration settings for the project, such as the IP address of the Raspberry Pi and the port number for the web server.

## Conclusion
The clock can be controlled through a web interface that allows the user to set the time, change the scrolling message, and adjust the brightness of the display. This project is a good example of using a Raspberry Pi to control a hardware device and it showcases how to create a web interface to control a device using Node.js and JavaScript.
