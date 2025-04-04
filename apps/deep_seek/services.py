import logging

from django.core.cache import cache
from openai import OpenAI, APIStatusError

from apps.activities.models import Event, Course
from apps.activities.serializers import EventSerializer, CourseSerializer
from apps.deep_seek.serializers import ShopsHeavyInfoSerializer
from apps.services.models import Service
from apps.services.serializers import ServiceSerializer
from apps.shops.models import Shop
from apps.users.kids.models import Kid
from apps.users.kids.serializers import KidSerializer
from config import settings

# for backward compatibility, you can still use `https://api.deepseek.com/v1` as `base_url`.


def get_message_from_assistant(message, model_name='openai', user=None):
    system_prompt = cache.get('system_prompt', None)
    if system_prompt is None:
        shops = Shop.objects.select_related(
            'city',
        ).prefetch_related(
            'commodity_group_categories',
            'commodity_group_categories__commodity_groups__products'
        )
        services = Service.objects.select_related(
            'category',
            'service_provider'
        )
        events = Event.objects.select_related(
            'category'
        )
        courses = Course.objects.select_related(
            'category'
        )

        shops_data = ShopsHeavyInfoSerializer(shops, many=True)
        services_data = ServiceSerializer(services, many=True)
        events_data = EventSerializer(events, many=True)
        courses_data = CourseSerializer(courses, many=True)
        system_prompt = f"""
        The user is a client of web site related to child support. And you are AI assistant called "Kampitik-Bot".
        About web site: Clients can find shops, products, activities (Courses, Events, Services(Baby sitters etc.))
        Your position here is to give advices and answer any question only related to child care.
    
        If somebody asks you about what do we have, additional info about shops and their products is provided below:
        {shops_data.data}
        
        If somebody asks about services:
        {services_data.data}
        
        If somebody asks you about activities, you tell them about events and courses. Events:
        {events_data.data}
        
        Courses:
        {courses_data.data}
        """
        cache.set('system_prompt', system_prompt)
    response = ""
    if model_name == 'openai':
        response = get_response_from_openai(message, user)
    elif model_name == 'deep_seek':
        response = get_response_from_deep_seek(message, user)
    result = dict()
    result['message'] = response
    return result


def get_response_from_openai(message, user):
    try:
        children = []
        if hasattr(user, 'client_user'):
            client_user = user.client_user
            children = Kid.objects.filter(client_user=client_user)
        children_data = KidSerializer(children, many=True).data
        client = OpenAI(api_key=settings.OPEN_AI_API_KEY)
        prompt = cache.get('system_prompt')
        prompt += f"\n If the user have children, then here is information about them. Talk about them only and if only user asks what to buy for them:\n{children_data}"
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


def get_response_from_deep_seek(message, user):
    try:
        children = []
        if hasattr(user, 'client_user'):
            client_user = user.client_user
            children = Kid.objects.filter(client_user=client_user)
        children_data = KidSerializer(children, many=True).data

        client = OpenAI(api_key=settings.DEEP_SEEK_API_KEY, base_url=settings.DEEP_SEEK_BASE_URL)
        prompt = cache.get('system_prompt')
        prompt += f"\n If the user have children, then here is information about them. Talk about them only and if only user asks what to buy for them:\n{children_data}"

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