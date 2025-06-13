# Allows model to search the web for latest information before generating a response
# import necessary libraries
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI()

# Define the web search function
def web_search(query: str) -> str:
    """
    Perform a web search using the OpenAI API.
    Args:
        query (str): The search query.
    Returns:
        str: The search results.
    """
    response = client.responses.create(
        model="gpt-4o-mini",
        tools=[{"type": "web_search_preview"}],
        input=query,
    )

    return response


if __name__ == "__main__":
    # Example usage
    search_query = "Latest news on AI advancements"
    results = web_search(search_query)
    print(f"Response: {results}")
    print("Search Results:", results.output_text)


# response output text
#
#Search Results: Artificial intelligence (AI) continues to make significant strides across various sectors. Here are some of the latest advancements:
#
#**Nvidia's AI Chip Innovations**
#
#At the GPU Technology Conference (GTC) 2025, Nvidia CEO Jensen Huang unveiled the Blackwell Ultra and Vera Rubin AI chips. These next-generation chips are designed to enhance AI capabilities, with the Rubin AI chip slated for release in late 2026 and Rubin Ultra in 2027. Nvidia anticipates that its data center infrastructure revenue will reach $1 trillion by 2028, driven by increasing demand for GPUs from leading cloud service providers. ([apnews.com](https://apnews.com/article/457e9260aa2a34c1bbcc07c98b7a0555?utm_source=openai))
#
#**Google's Gemini 2.0 and AI Models**
#
#Google introduced Gemini 2.0, an upgrade to its AI system, aiming to transition generative AI from merely answering questions to autonomously performing tasks. This enhancement is crucial for AI agents to operate reliably with less human supervision. Additionally, Google launched Gemini Robotics and Gemini Robotics-ER models to support the rapidly growing robotics industry, enabling advanced spatial understanding and program development through reasoning abilities. ([axios.com](https://www.axios.com/2024/12/11/gemini-20-demis-hassabis-agents-ai?utm_source=openai), [reuters.com](https://www.reuters.com/technology/google-introduces-new-ai-models-rapidly-growing-robotics-industry-2025-03-12/?utm_source=openai))
#
#**Advancements in AI for Healthcare**
#
#AI is revolutionizing healthcare by improving diagnostics and personalized medicine. Machine learning models are now being used to analyze medical images, detect early signs of diseases like cancer, and even predict patient outcomes based on genetic data. These technologies are helping doctors make more accurate diagnoses and develop personalized treatment plans tailored to individual patients. ([aist.ac](https://aist.ac/news/the-latest-ai-news-innovations-and-developments-in-artificial-intelligence/?utm_source=openai))
#
#**AI's Role in Mental Health**
#
#AI is increasingly being integrated into mental health care, with startups developing AI-driven chatbots and virtual therapists to provide support. For instance, Cedars-Sinai physician-scientists developed XAIA, a program that uses immersive virtual reality and generative AI to offer mental health support, resembling a human therapist. ([en.wikipedia.org](https://en.wikipedia.org/wiki/Artificial_intelligence_in_mental_health?utm_source=openai))
#
#**AI in Music Production**
#
#The music industry is embracing AI to enhance creativity and efficiency. AI tools assist artists in various stages of composition and production, suggesting chord progressions, melodies, and harmonies that align with the artist's style. This collaboration opens up new possibilities and helps artists overcome creative barriers. ([en.wikipedia.org](https://en.wikipedia.org/wiki/AI_in_the_Music_Industry?utm_source=openai))

## Recent AI Developments:
#- [Nvidia CEO Jensen Huang unveils new Rubin AI chips at GTC 2025](https://apnews.com/article/457e9260aa2a34c1bbcc07c98b7a0555?utm_source=openai)
#- [Google introduces new AI models for rapidly growing robotics industry](https://www.reuters.com/technology/google-introduces-new-ai-models-rapidly-growing-robotics-industry-2025-03-12/?utm_source=openai)
#- [Gemini 2.0 is the next chapter for Google AI](https://www.axios.com/2024/12/11/gemini-20-demis-hassabis-agents-ai?utm_source=openai)