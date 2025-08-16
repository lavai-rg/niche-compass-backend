import os
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient

import time

# Get environment variables
COG_SERV_KEY = os.getenv("AZURE_COGNITIVE_SERVICES_KEY")
COG_SERV_ENDPOINT = os.getenv("AZURE_COGNITIVE_SERVICES_ENDPOINT")

# Initialize Computer Vision client
computervision_client = ComputerVisionClient(
    COG_SERV_ENDPOINT,
    CognitiveServicesCredentials(COG_SERV_KEY)
)

# Initialize Text Analytics client
text_analytics_client = TextAnalyticsClient(
    endpoint=COG_SERV_ENDPOINT,
    credential=AzureKeyCredential(COG_SERV_KEY)
)

def analyze_image_from_url(image_url):
    """Analyzes an image from a URL using Computer Vision."""
    if not COG_SERV_KEY or not COG_SERV_ENDPOINT:
        print("Azure Cognitive Services credentials not set. Skipping image analysis.")
        return {"error": "Cognitive Services credentials not configured"}

    try:
        # Select the visual feature(s) you want to analyze
        features = [VisualFeatureTypes.tags, VisualFeatureTypes.description, VisualFeatureTypes.categories]
        
        image_analysis = computervision_client.analyze_image(image_url, features)

        return {
            "description": image_analysis.description.captions[0].text if image_analysis.description.captions else None,
            "tags": [tag.name for tag in image_analysis.tags],
            "categories": [category.name for category in image_analysis.categories]
        }
    except Exception as e:
        print(f"Error analyzing image: {e}")
        return {"error": str(e)}

def analyze_sentiment(text):
    """Analyzes the sentiment of a given text using Language Service."""
    if not COG_SERV_KEY or not COG_SERV_ENDPOINT:
        print("Azure Cognitive Services credentials not set. Skipping sentiment analysis.")
        return {"error": "Cognitive Services credentials not configured"}

    try:
        documents = [text]
        response = text_analytics_client.analyze_sentiment(documents=documents)[0]

        return {
            "sentiment": response.sentiment,
            "positive_score": response.confidence_scores.positive,
            "neutral_score": response.confidence_scores.neutral,
            "negative_score": response.confidence_scores.negative
        }
    except Exception as e:
        print(f"Error analyzing sentiment: {e}")
        return {"error": str(e)}

# Example Usage (for testing purposes)
if __name__ == "__main__":
    # Make sure to set AZURE_COGNITIVE_SERVICES_KEY and AZURE_COGNITIVE_SERVICES_ENDPOINT
    # in your environment variables or .env file before running this example.

    # Test Image Analysis
    image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/1/12/Broadway_light_bulb_sign.jpg/800px-Broadway_light_bulb_sign.jpg"
    print("\n--- Image Analysis ---")
    image_result = analyze_image_from_url(image_url)
    print(image_result)

    # Test Sentiment Analysis
    review_text_positive = "This product is absolutely amazing! I love it so much."
    review_text_negative = "I am very disappointed with this purchase. It broke after one use."
    review_text_neutral = "The product arrived on time and was as described."

    print("\n--- Sentiment Analysis ---")
    print("Positive Review:", analyze_sentiment(review_text_positive))
    print("Negative Review:", analyze_sentiment(review_text_negative))
    print("Neutral Review:", analyze_sentiment(review_text_neutral))


