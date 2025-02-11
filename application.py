import os, re, time, requests, json
from flask import Flask, request, render_template, jsonify
from openai import OpenAI, AzureOpenAI
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use a non-interactive backend
import matplotlib.pyplot as plt
from math import pi
import time



# Regular Expresion to determine if valid URL
URL_REGEX = re.compile(
    r'^(?:http|ftp)s?://'  # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]*[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
    r'localhost|'  # localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  # ...or ipv4
    r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'  # ...or ipv6
    r'(?::\d+)?'  # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)

# Initialize Flask app
load_dotenv()  # take environment variables from .env.
application = Flask(__name__)

# Load environment variables
os.environ["API_KEY"] = os.getenv("API_KEY")
model = os.getenv("GPT_MODEL")

# client = OpenAI(api_key=os.getenv("API_KEY"))

client = AzureOpenAI(
  azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"),
  api_key=os.getenv("AZURE_OPENAI_API_KEY"),
  api_version="2024-02-01"
)


@application.route('/transcript', methods=['POST'])
def transcript():
    # Check if 'question' and 'json_file' are present in the request
    question = request.form.get('question')
    json_file = request.files.get('json_file')

    if question and json_file:
        try:
            # Read and decode JSON data
            json_data = json_file.read().decode('utf-8')

            # Process transcripts
            transcript_results = remove_strings(transcript_analyzer_with_questions(question, json_data))
            print(transcript_results)

            # Write results to file
            with open('data.json', 'w') as f:
                f.write(transcript_results)

            # Read data from JSON file
            input_metrics = read_json('data.json')

            # Transform data for plotting
            transformed_metrics = transform_data(input_metrics)

            # Generate radar chart
            filename = plot_radar_chart(transformed_metrics)

            # Formulate response
            response = {
                "json_data": json.loads(transcript_results),
                "file_url": filename
            }

            # Return JSON response
            return jsonify(response)

        except Exception as e:
            return f"Error processing request: {str(e)}", 500

    # If necessary parameters are missing, return an error message
    return "Error: 'question' and 'json_file' are required.", 400


# This endpoint receives only POST requests
@application.route('/transcript', methods=['GET'])
def transcript_get():
    return "This endpoint receives POST requests"


@application.route('/', methods=['GET', 'POST'])
def root():
    print("Route / is accessed.")
    start_time = time.time()


    if request.method == 'POST':
        question = request.form['question']
        question, url_link = check_for_url(question) # Check if question is a URL if it is then get URL data, and return original URL
        #print(question)
        transcript_results = remove_strings(transcript_analizer(question))
        #print(transcript_results)
        # Open the file in write mode ('w')
        with open('data.json', 'w') as f:
            # Write the string to the file
            f.write(transcript_results)

        # Specify the path to your JSON file
        json_file_path = 'data.json'

        # Read data from JSON
        input_metrics = read_json(json_file_path)
        print(input_metrics)

        # Transform data to required format
        transformed_metrics = transform_data(input_metrics)

        json_data = json.loads(transcript_results)
        print(json_data)
        # Plot radar chart
        filename = plot_radar_chart(transformed_metrics)
        return render_template("index.html", data=json_data, image=filename, question=question)


    return render_template("index.html")



def read_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def transform_data(input_data):
    metrics = []
    for key, value in input_data.items():
        if isinstance(value, dict) and 'Score' in value:
            metric = {
                "Metric": key,
                "Value": value["Score"]
            }
            metrics.append(metric)
    return metrics

def plot_radar_chart(metrics):
    # Extract categories and values
    categories = [metric["Metric"] for metric in metrics]
    values = [metric["Value"] for metric in metrics]
    N = len(categories)

    # What will be the angle of each axis in the plot? (we divide the plot / number of variables)
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]

    # We need values to be a closed loop
    values += values[:1]

    # Initialise the spider plot
    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(polar=True))

    # Draw one axe per variable + add labels
    plt.xticks(angles[:-1], categories, color='black', size=8)

    # Draw y-labels
    ax.set_rlabel_position(0)
    plt.yticks([2, 4, 6, 8, 10], ["2", "4", "6", "8", "10"], color="grey", size=7)
    plt.ylim(0, 10)

    # Plot data
    ax.plot(angles, values, linewidth=2, linestyle='solid')

    # Fill area
    ax.fill(angles, values, 'b', alpha=0.1)

    plt.title('Candidate Interview - Performance Radar Chart', size=18, color='black', y=1.1)

    # Get current Unix timestamp
    timestamp = int(time.time())

    # Convert to string and take the last 8 digits
    file_timestamp = str(timestamp)[-8:]

    filename = 'static/images/radar_chart' + file_timestamp + '.png'
    # Save the plot as an image file
    plt.savefig(filename)
    plt.close()
    return filename






def check_for_url(data):
    if is_valid_url(data):
        print(f'✅ This a valid URL {data} obtaining data..')
        try:
            url_link = data
            response = requests.get(data)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            question = soup.get_text(strip=True)
            data = f'{question[:100000]}'
            print("✅ Obtained information from URL")
            return data , url_link
        except requests.RequestException as e:
            return f'Error fetching the URL: {str(e)}'
    else:
        return data, None

def is_valid_url(url):
    return re.match(URL_REGEX, url) is not None

def remove_strings(text):
    """Remove specific markup strings from the given text."""
    # Pattern to match specific text blocks (case-insensitive)
    pattern = r'```json|```plantuml|```html|```'
    cleaned_text = re.sub(pattern, '', text, flags=re.IGNORECASE)
    return cleaned_text

def query_gpt(message_text, temperature=0.8, max_tokens=800):
    """Query GPT-3 with the given message text and return the response."""
    completion = client.chat.completions.create(
        model=model,
        messages=message_text,
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None
    )
    response_text = completion.choices[0].message.content
    return response_text




def transcript_analizer(message):
    """Prompt to analyze  ."""
    message_text = [
        {"role": "system", "content": """You are an AI specialized in analyzing text transcripts from interviews. Your output will be a JSON file named : data.json, with following categories: [Relevance of Answers, Depth of Knowledge, Problem-solving Skills, Experience and Examples, Technical Proficiency, Communication Skills, Listening Skills, Interpersonal Skills, Enthusiasm and Motivation, Cultural Fit, Creativity and Innovation, Adaptability and Flexibility, Leadership Potential, Type of questions
] and include [Score] and [Comments] for each category and a field [Overall Score] and [Summary], for the [Overall Score] use this weighting criteria : [[Relevance of Answers]:0.1,	[Depth of Knowledge]:0.12,	[Problem-solving Skills]:0.12,	[Experience and Examples]:0.1,	[Technical Proficiency]:0.15,	[Communication Skills]:0.06,	[Listening Skills]:0.05,	[Interpersonal Skills]:0.05,	[Enthusiasm and Motivation]:0.05,	[Cultural Fit]:0.06,	[Creativity and Innovation]:0.05,	[Adaptability and Flexibility]:0.03,	[Leadership Potential]:0.05,	[Type of questions]:0.01 ]
  """},
        {"role": "user", "content": """Rate the candidate's performance in the following areas from 1 (poor) to 10 (excellent) based on their responses in the interview transcript.
Rate how directly and effectively the candidate's responses addressed the questions asked : """ + message}

    ]
    return query_gpt(message_text, temperature=0, max_tokens=4000)


def transcript_analyzer_with_questions(message, json_data ):
    """Prompt to analyze  ."""
    message_text = [
        {"role": "system", "content": """You are an AI specialized in analyzing text transcripts from interviews. Your output will be a JSON file named : data.json, with following categories: [Relevance of Answers, Depth of Knowledge, Problem-solving Skills, Experience and Examples, Technical Proficiency, Communication Skills, Listening Skills, Interpersonal Skills, Enthusiasm and Motivation, Cultural Fit, Creativity and Innovation, Adaptability and Flexibility, Leadership Potential, Type of questions
] and include [Score] and [Comments] for each category and a field [Overall Score] and [Summary], for the [Overall Score] use this weighting criteria : [[Relevance of Answers]:0.1,	[Depth of Knowledge]:0.12,	[Problem-solving Skills]:0.12,	[Experience and Examples]:0.1,	[Technical Proficiency]:0.15,	[Communication Skills]:0.06,	[Listening Skills]:0.05,	[Interpersonal Skills]:0.05,	[Enthusiasm and Motivation]:0.05,	[Cultural Fit]:0.06,	[Creativity and Innovation]:0.05,	[Adaptability and Flexibility]:0.03,	[Leadership Potential]:0.05,	[Type of questions]:0.01 ]
  """},
        {"role": "user", "content": """Rate the candidate's performance in the following areas from 1 (poor) to 10 (excellent) based on their responses in the interview transcript.
Rate how directly and effectively the candidate's responses addressed the questions asked : """ + message + """ use this JSON that contains the list of questions to be asked """ + json_data}

    ]
    return query_gpt(message_text, temperature=0, max_tokens=4000)



if __name__ == '__main__':
    application.run(debug=True, port=5001)