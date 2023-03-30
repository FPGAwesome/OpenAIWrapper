# OpenAI API Wrapper

This repository provides a simple Python interface to interact with several OpenAI models, including Chatgpt, GPT-3, and Openai Whisper. The purpose of this software is to help users and developers learn about the caveats of these models, their APIs, and offer a potentially useful resource. This project is currently in active development and is subject to rapid changes and improvements.

## Features

- Python interface to interact with Chatgpt, GPT-3, and Openai Whisper
- Understandable(WIP) code for learning purposes
- Flask app example included for demonstration purposes

## Installation

Clone the repository:

```
git clone https://github.com/FPGAwesome/OpenAIWrapper.git
cd OpenAIWrapper
```

Install the required dependencies:

```
pip install -r requirements.txt
```

## Usage

After installing the required dependencies, export your OpenAI API key as an environment variable:

```
export OPENAI_API_KEY=your_api_key
```

For the Flask app implementation, run the following command:

```
flask --app test_flaskinterface.py run
```

## Note for Developers

As this project is still under active development, it is subject to rough and rapid changes. The code in this repository is intended primarily for learning, and the functionality is subject to change. Contributions and feedback are welcome.

## Acknowledgments

This project references and makes use of code from several different resources. Attribution is provided within the code, where applicable.
