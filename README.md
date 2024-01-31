# Typing Speed Test

The Typing Speed Test App is a simple and interactive application designed to measure and improve your typing speed and accuracy. This app provides a platform for users to practice typing a set of randomly shuffled words and evaluates their typing speed in words per minute (WPM) and characters per minute (CPM).

## Features

- **Randomized Word Lists:** The application loads a set of words from a CSV file, shuffles them, and presents them to the user for typing practice.
  
- **Real-Time Feedback:** Users receive real-time feedback on their typing accuracy as they enter each word. Correctly typed letters are highlighted in blue, incorrect letters in red, and the entire word changes color upon completion.

- **Timers and Metrics:** The app includes timers for tracking the overall time spent, time left in the typing test, and calculates WPM and CPM based on the user's input.

- **Dynamic Canvas Layout:** The canvas dynamically adjusts to the user's typing speed, adding new words as needed and scrolling smoothly to maintain an optimal layout.

- **Results Display:** At the end of the typing test, the app displays the user's performance, including WPM, CPM, and a list of words with correctness indicators.

## Requirements

- Python 3.9
- Third-party libraries (specified in requirements.txt)
- CustomTkinter library
- PIL (Pillow) library

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/typing-speed-test-app.git
    ```
2. Navigate to the project directory:

    ```bash
    cd typing-speed-test-app
    ```
3. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```
4. Run the application:

    ```bash
    python main.py
    ```
## Usage

1. Launch the application by running main.py.
2. The main window will display the title, subtitle, and a dynamically generated set of words for typing practice.
3. Start typing the displayed words in the Entry widget.
4. Receive real-time feedback on your typing accuracy.
5. The timers will track your overall time, time left, and calculate WPM and CPM.
6. Once the time is up, the app will display your performance results.

## Data Source

The word data used in this application was sourced from [Word Difficulty Dataset on Kaggle](https://www.kaggle.com/datasets/kkhandekar/word-difficulty/data). Specifically, the 1000 most easy words were extracted from this dataset for use in the typing speed test application.

I would like to express our gratitude to the original creator of the dataset, [koustubhk](https://www.kaggle.com/kkhandekar), for providing this valuable resource to the community.


## Customization

- Word Lists: You can customize the word lists used in the test by modifying the CSV file located in the resources/data directory.

- Appearance: Customize the appearance of the application by adjusting fonts, colors, and other visual elements in the code.

## Contributing

Contributions are welcome! If you have any suggestions, bug reports, or feature requests, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
