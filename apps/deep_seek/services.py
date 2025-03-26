import logging

from django.core.cache import cache
from openai import OpenAI, APIStatusError

from apps.deep_seek.serializers import ShopsHeavyInfoSerializer
from apps.shops.models import Shop
from config import settings

# for backward compatibility, you can still use `https://api.deepseek.com/v1` as `base_url`.


def get_message_from_assistant(message, model_name='openai'):
    system_prompt = cache.get('system_prompt', None)
    if system_prompt is None:
        shops = Shop.objects.select_related(
            'city',
        ).prefetch_related(
            'categories',
            'categories__products',
            'commodity_group_categories',
            'commodity_group_categories__commodity_groups__products'
        )
        shops_data = ShopsHeavyInfoSerializer(shops, many=True)

        system_prompt = f"""
        The user is a client of web site related to child support. And you are AI assistant called "Kampitik-Bot".
        About web site: Clients can find shops, products, activities (Courses, Events, Services(Baby sitters etc.))
        Your position here is to give advices and answer any question only related to child care.
    
        additional info about shops we have:
        {shops_data.data}
        """
        cache.set('system_prompt', system_prompt)
    response = ""
    if model_name == 'openai':
        response = get_response_from_openai(message)
    elif model_name == 'deep_seek':
        response = get_response_from_deep_seek(message)
    result = dict()
    result['message'] = response
    return result


def get_response_from_openai(message):
    try:
        client = OpenAI(api_key=settings.OPEN_AI_API_KEY)
        prompt = cache.get('system_prompt')

        response = client.chat.completions.create(
            model='gpt-4o',
            messages=[
                {"role": "developer", "content": prompt},
                {"role": "user", "content": message},
            ],
            max_tokens=1024,
            temperature=1.2,
            stream=False
        )
        result = response.choices[0].message.content
        return result
    except APIStatusError as e:
        logging.warning(f"openai: {e}")


def get_response_from_deep_seek(message):
    try:
        client = OpenAI(api_key=settings.DEEP_SEEK_API_KEY, base_url=settings.DEEP_SEEK_BASE_URL)
        prompt = cache.get('system_prompt')

        response = client.chat.completions.create(
            model='gpt-4o',
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": message},
            ],
            max_tokens=1024,
            temperature=1.2,
            stream=False
        )
        result = response.choices[0].message.content
        return result
    except APIStatusError as e:
        logging.warning(f"deepseek: {e}")