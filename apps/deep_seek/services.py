import logging

from django.core.cache import cache
from openai import OpenAI, APIStatusError

from apps.deep_seek.serializers import ShopsHeavyInfoSerializer
from apps.shops.commodity_groups.models import CommodityGroupCategory, CommodityGroup
from apps.shops.models import Shop
from apps.shops.products.models import ProductCategory, Product
from config import settings

# for backward compatibility, you can still use `https://api.deepseek.com/v1` as `base_url`.

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
cache.set('deep_seek_system_prompt', system_prompt)


def test_deep_seek(message):
    try:
        print(settings.DEEP_SEEK_API_KEY)
        client = OpenAI(api_key=settings.DEEP_SEEK_API_KEY, base_url=settings.DEEP_SEEK_BASE_URL)
        prompt = cache.get('deep_seek_system_prompt')
        exception_counter = 0
        while prompt is None and exception_counter < 10:
            prompt = cache.get('deep_seek_system_prompt')
            exception_counter += 1
            logging.warning(f"Prompt for DeepSeek is empty, started exception counter: {exception_counter}")
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": cache.get('deep_seek_system_prompt')},
                {"role": "user", "content": message},
            ],
            max_tokens=1024,
            temperature=1.2,
            stream=False
        )
        result = {}
        result['message'] = response.choices[0].message.content
        return result
    except APIStatusError as e:
        print(e.message)
