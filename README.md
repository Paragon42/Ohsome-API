# Ohsome-API


This Python application is an imitation of the proof of concept ChatGeoPT app that performs geospatial searches using an AI assistant. However, instead of using the initial prototype's search mechanisms, this application queries the Ohsome API.

## Getting Started

To use this app, you will need to have Python 3.6 or higher installed on your machine. You can download Python from the official website: https://www.python.org/downloads/.

Once you have Python installed, you can clone this repository to your local machine using Git or simply download the ZIP file and extract it to a directory of your choice.

## Installing Dependencies

This app requires several dependencies to be installed before it can be run. You can install them all at once by running the following command in your terminal or command prompt, from within the cloned or extracted directory:

```
pip install -r requirements.txt
```

## Configuring the App

Before running the app, you will need to configure the app to use your Ohsome API credentials. To do this, copy the `config.example.py` file and rename it to `config.py`. Then, open `config.py` in your favorite text editor and replace the placeholder values with your own Ohsome API credentials.

## Running the App

To run the app, simply execute the following command from within the cloned or extracted directory:

```
python app.py
```

This will start the app and launch a web server at `http://localhost:5000`. You can then navigate to that URL in your web browser to use the app.

## Using the App

When you first load the app, you will see a simple user interface that prompts you to enter a geospatial query. You can enter any valid Ohsome API query, including a bounding box, time range, and other filters.

Once you enter your query and click the "Search" button, the app will send the query to the Ohsome API and display the results in the browser. You can then interact with the results by clicking on them to view more information or zooming in and out on the map.

## Contributing

If you would like to contribute to this project, feel free to submit a pull request or open an issue on the project's GitHub repository: https://github.com/paragon42/Ohsome-API

## License

This app is licensed under the MIT license. See the LICENSE file for more details.
