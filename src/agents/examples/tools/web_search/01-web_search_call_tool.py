# https://platform.openai.com/docs/guides/tools-web-search?api-mode=responses
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


def web_search_with_location(query: str) -> str:
    response = client.responses.create(
        model="gpt-4o-mini",
        tools=[{
            "type": "web_search_preview",
            "user_location": {
                "type": "approximate",
                "country": "GB",
                "city": "London",
                "region": "London"
            }
        }],
        input=query,
    )

    return response


def web_search_customize_context_size(query: str) -> str:
    response = client.responses.create(
        model="gpt-4o-mini",
        tools=[{
            "type": "web_search_preview",
            "search_context_size": "low", # {low, medium, high}
        }],
        input=query,
    )

    return response


if __name__ == "__main__":
    # Example usage
    search_query1 = "Latest news on AI advancements"
    results1 = web_search(search_query1)
    print(f"Response: {results1}")
    print("Search Results:", results1.output_text)

# response output text
#Response: 
#Response(
#    id='resp_684d4292acfc819ca43c207f7c9d9d2c017f391869486737', 
#    created_at=1749893778.0, 
#    error=None, 
#    incomplete_details=None, 
#    instructions=None, 
#    metadata={}, 
#    model='gpt-4o-mini-2024-07-18', 
#    object='response', 
#    output=[
#        ResponseFunctionWebSearch(
#            id='ws_684d429333cc819cad760f690660645a017f391869486737', 
#            status='completed', 
#            type='web_search_call'), 
#            ResponseOutputMessage(
#                id='msg_684d4295e438819c8c127b6c0df01798017f391869486737', 
#                content=[ResponseOutputText(
#                    annotations=[
#                        AnnotationURLCitation(
#                            end_index=720, 
#                            start_index=627, 
#                            title='Nvidia CEO Jensen Huang unveils new Rubin AI chips at GTC 2025', 
#                            type='url_citation', 
#                            url='https://apnews.com/article/457e9260aa2a34c1bbcc07c98b7a0555?utm_source=openai'), 
#                        AnnotationURLCitation(end_index=1405, start_index=1258, title='Google introduces new AI models for rapidly growing robotics industry', type='url_citation', 
#                            url='https://www.reuters.com/technology/google-introduces-new-ai-models-rapidly-growing-robotics-industry-2025-03-12/?utm_source=openai'), AnnotationURLCitation(end_index=2015, start_index=1922, title='AI can learn to think before it speaks', type='url_citation', url='https://www.ft.com/content/894669d6-d69d-4515-a18f-569afbf710e8?utm_source=openai'), AnnotationURLCitation(end_index=2579, start_index=2444, title='INDIAai', type='url_citation', url='https://indiaai.gov.in/article/the-future-is-now-latest-ai-breakthroughs-and-their-impact-in-2024?utm_source=openai'), AnnotationURLCitation(end_index=3072, start_index=2993, title='Latest AI Innovations Transforming Industries', type='url_citation', url='https://www.koombea.com/blog/ai-innovations/?utm_source=openai'), AnnotationURLCitation(end_index=3262, 
#                            start_index=3119, 
#                            title='Nvidia CEO Jensen Huang unveils new Rubin AI chips at GTC 2025', 
#                            type='url_citation', 
#                            url='https://apnews.com/article/457e9260aa2a34c1bbcc07c98b7a0555?utm_source=openai'), 
#                        AnnotationURLCitation(
#                            end_index=3468, 
#                            start_index=3265, 
#                            title='Google introduces new AI models for rapidly growing robotics industry', 
#                            type='url_citation', 
#                            url='https://www.reuters.com/technology/google-introduces-new-ai-models-rapidly-growing-robotics-industry-2025-03-12/?utm_source=openai'), 
#                        AnnotationURLCitation(end_index=3594, start_index=3471, title='AI can learn to think before it speaks', type='url_citation', url='https://www.ft.com/content/894669d6-d69d-4515-a18f-569afbf710e8?utm_source=openai')], text="Artificial intelligence (AI) continues to make significant strides across various sectors. Here are some of the latest advancements:\n\n**Nvidia's AI Chip Innovations**\n\nAt the GPU Technology Conference (GTC) 2025, Nvidia CEO Jensen Huang unveiled the Blackwell Ultra and Vera Rubin AI chips. These next-generation chips are expected to revolutionize AI processing capabilities. Nvidia anticipates its data center infrastructure revenue to reach $1 trillion by 2028, driven by the increasing demand for GPUs from top cloud service providers. The Rubin AI chip is slated for release in late 2026, followed by Rubin Ultra in 2027. ([apnews.com](https://apnews.com/article/457e9260aa2a34c1bbcc07c98b7a0555?utm_source=openai))\n\n**Google's AI Model Releases**\n\nGoogle introduced two new AI models, Gemini Robotics and Gemini Robotics-ER, based on the Gemini 2.0 model, to support the rapidly expanding robotics industry. Gemini Robotics is an advanced vision-language-action model for physical actions output, while Gemini Robotics-ER enables advanced spatial understanding and program development using reasoning abilities. These models aim to assist diverse robot types, including industrial humanoids, and help startups reduce costs and accelerate market entry. ([reuters.com](https://www.reuters.com/technology/google-introduces-new-ai-models-rapidly-growing-robotics-industry-2025-03-12/?utm_source=openai))\n\n**Advancements in AI Deliberation**\n\nOpenAI's latest development, the o1 large language model (LLM), incorporates deliberation capabilities akin to human reasoning. This advancement enhances coherence and planning in AI responses, marking a significant milestone in AI development. However, it also raises concerns about potential risks, including increased deception and the creation of biological weapons. The need for regulation and safety considerations is emphasized as AI approaches human-level intelligence. ([ft.com](https://www.ft.com/content/894669d6-d69d-4515-a18f-569afbf710e8?utm_source=openai))\n\n**AI in Healthcare**\n\nAI is revolutionizing healthcare by improving diagnostic accuracy and enabling personalized treatment plans. Machine learning models analyze medical images to detect early signs of diseases like cancer, and AI-driven systems develop tailored treatments based on genetic data. Additionally, AI is accelerating drug discovery, significantly reducing the time required to identify potential new medications. ([indiaai.gov.in](https://indiaai.gov.in/article/the-future-is-now-latest-ai-breakthroughs-and-their-impact-in-2024?utm_source=openai))\n\n**Autonomous Vehicles and Robotics**\n\nAI advancements are propelling the development of autonomous vehicles and robotics. Companies like Waymo are integrating AI with urban infrastructure to create safer and more efficient transportation options. In robotics, AI is enhancing capabilities in manufacturing, logistics, and healthcare, with autonomous drones used for deliveries and robots assisting in surgeries. ([koombea.com](https://www.koombea.com/blog/ai-innovations/?utm_source=openai))\n\n\n## Recent Breakthroughs in AI Technology:\n- [Nvidia CEO Jensen Huang unveils new Rubin AI chips at GTC 2025](https://apnews.com/article/457e9260aa2a34c1bbcc07c98b7a0555?utm_source=openai)\n- [Google introduces new AI models for rapidly growing robotics industry](https://www.reuters.com/technology/google-introduces-new-ai-models-rapidly-growing-robotics-industry-2025-03-12/?utm_source=openai)\n- [AI can learn to think before it speaks](https://www.ft.com/content/894669d6-d69d-4515-a18f-569afbf710e8?utm_source=openai) ", type='output_text')], role='assistant', status='completed', type='message')], parallel_tool_calls=True, temperature=1.0, tool_choice='auto', tools=[WebSearchTool(type='web_search_preview', search_context_size='medium', user_location=UserLocation(type='approximate', city=None, country='US', region=None, timezone=None))], top_p=1.0, background=False, max_output_tokens=None, previous_response_id=None, reasoning=Reasoning(effort=None, generate_summary=None, summary=None), service_tier='default', status='completed', text=ResponseTextConfig(format=ResponseFormatText(type='text')), truncation='disabled', usage=ResponseUsage(input_tokens=306, input_tokens_details=InputTokensDetails(cached_tokens=0), output_tokens=799, output_tokens_details=OutputTokensDetails(reasoning_tokens=0), total_tokens=1105), user=None, store=True)
#Search Results: Artificial intelligence (AI) continues to make significant strides across various sectors. Here are some of the latest advancements:
#
#**Nvidia's AI Chip Innovations**
#
#At the GPU Technology Conference (GTC) 2025, Nvidia CEO Jensen Huang unveiled the Blackwell Ultra and Vera Rubin AI chips. These next-generation chips are expected to revolutionize AI processing capabilities. Nvidia anticipates its data center infrastructure revenue to reach $1 trillion by 2028, driven by the increasing demand for GPUs from top cloud service providers. The Rubin AI chip is slated for release in late 2026, followed by Rubin Ultra in 2027. ([apnews.com](https://apnews.com/article/457e9260aa2a34c1bbcc07c98b7a0555?utm_source=openai))
#
#**Google's AI Model Releases**
#
#Google introduced two new AI models, Gemini Robotics and Gemini Robotics-ER, based on the Gemini 2.0 model, to support the rapidly expanding robotics industry. Gemini Robotics is an advanced vision-language-action model for physical actions output, while Gemini Robotics-ER enables advanced spatial understanding and program development using reasoning abilities. These models aim to assist diverse robot types, including industrial humanoids, and help startups reduce costs and accelerate market entry. ([reuters.com](https://www.reuters.com/technology/google-introduces-new-ai-models-rapidly-growing-robotics-industry-2025-03-12/?utm_source=openai))
#
#**Advancements in AI Deliberation**
#
#OpenAI's latest development, the o1 large language model (LLM), incorporates deliberation capabilities akin to human reasoning. This advancement enhances coherence and planning in AI responses, marking a significant milestone in AI development. However, it also raises concerns about potential risks, including increased deception and the creation of biological weapons. The need for regulation and safety considerations is emphasized as AI approaches human-level intelligence. ([ft.com](https://www.ft.com/content/894669d6-d69d-4515-a18f-569afbf710e8?utm_source=openai))
#
#**AI in Healthcare**
#
#AI is revolutionizing healthcare by improving diagnostic accuracy and enabling personalized treatment plans. Machine learning models analyze medical images to detect early signs of diseases like cancer, and AI-driven systems develop tailored treatments based on genetic data. Additionally, AI is accelerating drug discovery, significantly reducing the time required to identify potential new medications. ([indiaai.gov.in](https://indiaai.gov.in/article/the-future-is-now-latest-ai-breakthroughs-and-their-impact-in-2024?utm_source=openai))
#
#**Autonomous Vehicles and Robotics**
#
#AI advancements are propelling the development of autonomous vehicles and robotics. Companies like Waymo are integrating AI with urban infrastructure to create safer and more efficient transportation options. In robotics, AI is enhancing capabilities in manufacturing, logistics, and healthcare, with autonomous drones used for deliveries and robots assisting in surgeries. ([koombea.com](https://www.koombea.com/blog/ai-innovations/?utm_source=openai))
#
## Recent Breakthroughs in AI Technology:
#- [Nvidia CEO Jensen Huang unveils new Rubin AI chips at GTC 2025](https://apnews.com/article/457e9260aa2a34c1bbcc07c98b7a0555?utm_source=openai)
#- [Google introduces new AI models for rapidly growing robotics industry](https://www.reuters.com/technology/google-introduces-new-ai-models-rapidly-growing-robotics-industry-2025-03-12/?utm_source=openai)
#- [AI can learn to think before it speaks](https://www.ft.com/content/894669d6-d69d-4515-a18f-569afbf710e8?utm_source=openai)

    # Example usage
    search_query2 = "What are the best restaurants around Granary Square?"
    results2 = web_search_with_location(search_query2)
    print(f"Response: {results2}")
    print("Search Results:", results2.output_text)

#Response: Response(id='resp_68501dd0422881918ab1c6caeb88edf70d5aba1b19f2d926', created_at=1750080976.0, error=None, incomplete_details=None, instructions=None, metadata={}, model='gpt-4o-mini-2024-07-18', object='response', output=[ResponseFunctionWebSearch(id='ws_68501dd0ad948191b9a89a22266551050d5aba1b19f2d926', status='completed', type='web_search_call'), ResponseOutputMessage(id='msg_68501dd21bb48191a56833e5dc0845f90d5aba1b19f2d926', content=[ResponseOutputText(annotations=[AnnotationURLCitation(end_index=265, start_index=181, title='Granary Square Brasserie', type='url_citation', url='https://www.granarysquarebrasserie.com?utm_source=openai'), AnnotationURLCitation(end_index=556, start_index=504, title='Dishoom', type='url_citation', url='https://www.dishoom.com?utm_source=openai'), AnnotationURLCitation(end_index=883, start_index=799, title="Caravan King's Cross", type='url_citation', url='https://caravanandco.com/pages/kings-cross?utm_source=openai'), AnnotationURLCitation(end_index=1184, start_index=1124, title='Lina Stores', type='url_citation', url='http://www.linastores.co.uk?utm_source=openai'), AnnotationURLCitation(end_index=1465, start_index=1399, title='The Lighterman', type='url_citation', url='http://www.thelighterman.co.uk?utm_source=openai'), AnnotationURLCitation(end_index=1747, start_index=1689, title='Barrafina', type='url_citation', url='http://www.barrafina.co.uk/?utm_source=openai')], text="Granary Square in King's Cross boasts a vibrant culinary scene with a variety of dining options to suit diverse tastes. Here are some notable restaurants in and around the area:\n\n**[Granary Square Brasserie](https://www.granarysquarebrasserie.com?utm_source=openai)**  \n**Open now · English · 3.8 (76 reviews)**  \n_1 Granary Square (Granary Sq), London, Greater London, N1C 4AA_  \nAn all-day dining spot offering British-European cuisine in a stylish setting with a terrace overlooking the fountains.\n\n**[Dishoom](https://www.dishoom.com?utm_source=openai)**  \n**Open now · Indian · $$ · 4.5 (35 reviews)**  \n_Battersea Power Station (42 Electric Blvd), Battersea, Greater London, SW11 8BJ_  \nA Bombay-style café serving authentic Indian dishes, including the renowned bacon naan and black daal.\n\n**[Caravan King's Cross](https://caravanandco.com/pages/kings-cross?utm_source=openai)**  \n**Open now · Breakfast · $$ · 4.5 (1550 reviews)**  \n_1 Granary Sq (Stable St), London, Greater London, N1C 4AA_  \nA relaxed eatery known for its globally inspired menu, featuring dishes like jalapeño cornbread and sourdough pizzas.\n\n**[Lina Stores](http://www.linastores.co.uk?utm_source=openai)**  \n**Open now · Gourmet · 4.4 (107 reviews)**  \n_18 Brewer St, London, Greater London, W1F 0SH_  \nAn Italian restaurant specializing in fresh pasta and classic dishes, set in a bright and welcoming atmosphere.\n\n**[The Lighterman](http://www.thelighterman.co.uk?utm_source=openai)**  \n**Open now · Gastropub · $$$ · 4.0 (415 reviews)**  \n_3 Granary Sq, London, Greater London, N1C 4BH_  \nA modern British restaurant with panoramic views of Granary Square and Regent's Canal, offering seasonal dishes.\n\n**[Barrafina](http://www.barrafina.co.uk/?utm_source=openai)**  \n**Open now · Tapas · $$$ · 4.3 (769 reviews)**  \n_26-27 Dean St, London, Greater London, W1D 3LL_  \nAn award-winning Spanish tapas restaurant known for its authentic dishes and extensive wine selection.\n\nThese establishments offer a range of cuisines and dining experiences, ensuring that visitors to Granary Square can find a meal to suit their preferences. ", type='output_text')], role='assistant', status='completed', type='message')], parallel_tool_calls=True, temperature=1.0, tool_choice='auto', tools=[WebSearchTool(type='web_search_preview', search_context_size='medium', user_location=UserLocation(type='approximate', city='London', country='GB', region='London', timezone=None))], top_p=1.0, background=False, max_output_tokens=None, previous_response_id=None, reasoning=Reasoning(effort=None, generate_summary=None, summary=None), service_tier='default', status='completed', text=ResponseTextConfig(format=ResponseFormatText(type='text')), truncation='disabled', usage=ResponseUsage(input_tokens=311, input_tokens_details=InputTokensDetails(cached_tokens=0), output_tokens=560, output_tokens_details=OutputTokensDetails(reasoning_tokens=0), total_tokens=871), user=None, store=True)
#Search Results: Granary Square in King's Cross boasts a vibrant culinary scene with a variety of dining options to suit diverse tastes. Here are some notable restaurants in and around the area:
#
#**[Granary Square Brasserie](https://www.granarysquarebrasserie.com?utm_source=openai)**  
#**Open now · English · 3.8 (76 reviews)**  
#_1 Granary Square (Granary Sq), London, Greater London, N1C 4AA_  
#An all-day dining spot offering British-European cuisine in a stylish setting with a terrace overlooking the fountains.
#
#**[Dishoom](https://www.dishoom.com?utm_source=openai)**  
#**Open now · Indian · $$ · 4.5 (35 reviews)**  
#_Battersea Power Station (42 Electric Blvd), Battersea, Greater London, SW11 8BJ_  
#A Bombay-style café serving authentic Indian dishes, including the renowned bacon naan and black daal.
#
#**[Caravan King's Cross](https://caravanandco.com/pages/kings-cross?utm_source=openai)**  
#**Open now · Breakfast · $$ · 4.5 (1550 reviews)**  
#_1 Granary Sq (Stable St), London, Greater London, N1C 4AA_  
#A relaxed eatery known for its globally inspired menu, featuring dishes like jalapeño cornbread and sourdough pizzas.
#
#**[Lina Stores](http://www.linastores.co.uk?utm_source=openai)**  
#**Open now · Gourmet · 4.4 (107 reviews)**  
#_18 Brewer St, London, Greater London, W1F 0SH_  
#An Italian restaurant specializing in fresh pasta and classic dishes, set in a bright and welcoming atmosphere.
#
#**[The Lighterman](http://www.thelighterman.co.uk?utm_source=openai)**  
#**Open now · Gastropub · $$$ · 4.0 (415 reviews)**  
#_3 Granary Sq, London, Greater London, N1C 4BH_  
#A modern British restaurant with panoramic views of Granary Square and Regent's Canal, offering seasonal dishes.
#
#**[Barrafina](http://www.barrafina.co.uk/?utm_source=openai)**  
#**Open now · Tapas · $$$ · 4.3 (769 reviews)**  
#_26-27 Dean St, London, Greater London, W1D 3LL_  
#An award-winning Spanish tapas restaurant known for its authentic dishes and extensive wine selection.
#
#These establishments offer a range of cuisines and dining experiences, ensuring that visitors to Granary Square can find a meal to suit their preferences.

    search_query3 = "Latest news on AI advancements"
    results3 = web_search_customize_context_size(search_query3)
    print(f"Response: {results3}")
    print("Search Results:", results3.output_text)

