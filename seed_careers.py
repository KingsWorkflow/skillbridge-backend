#!/usr/bin/env python
"""Script to add dummy CareerPath data for testing skill gap page."""

import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skillbridge.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from apps.skills.models import Skill
from apps.careers.models import CareerPath

def get_skill(name):
    return Skill.objects.filter(name__iexact=name).first()

# Define dummy careers using existing skills
careers_data = [
    {
        'title': 'Full Stack Developer',
        'description': 'Build complete web applications using frontend and backend technologies. Work across the entire stack from UI design to database architecture.',
        'category': 'Technology',
        'required_skills': [
            ('Python Programming', 40),
            ('Django', 60),
            ('React', 50),
            ('UI/UX Design', 40),
            ('Docker', 30),
            ('AWS', 30),
        ],
        'average_salary': 'NPR 1,500,000 - 3,500,000 per year',
        'growth_outlook': '+28% YoY',
    },
    {
        'title': 'Data Scientist',
        'description': 'Extract insights from complex datasets, build predictive models, and drive data-informed decisions for businesses.',
        'category': 'Data',
        'required_skills': [
            ('Python Programming', 50),
            ('Data Analysis', 60),
            ('Machine Learning', 70),
            ('UI/UX Design', 20),
        ],
        'average_salary': 'NPR 1,800,000 - 4,000,000 per year',
        'growth_outlook': '+35% YoY',
    },
    {
        'title': 'Digital Marketing Specialist',
        'description': 'Plan and execute online marketing campaigns. Manage SEO, SEM, social media, and content marketing to drive growth.',
        'category': 'Marketing',
        'required_skills': [
            ('Digital Marketing', 40),
            ('SEO', 50),
            ('Content Writing', 60),
            ('Graphic Design', 30),
            ('Data Analysis', 20),
        ],
        'average_salary': 'NPR 900,000 - 2,200,000 per year',
        'growth_outlook': '+20% YoY',
    },
    {
        'title': 'DevOps Engineer',
        'description': 'Bridge development and operations by automating pipelines, managing CI/CD, and ensuring system reliability at scale.',
        'category': 'Technology',
        'required_skills': [
            ('Docker', 40),
            ('AWS', 60),
            ('Python Programming', 30),
            ('Machine Learning', 20),
        ],
        'average_salary': 'NPR 1,800,000 - 4,200,000 per year',
        'growth_outlook': '+32% YoY',
    },
    {
        'title': 'UI/UX Designer',
        'description': 'Design intuitive user interfaces and seamless user experiences for digital products. Conduct user research and iterate on designs.',
        'category': 'Design',
        'required_skills': [
            ('UI/UX Design', 60),
            ('Graphic Design', 50),
            ('React', 30),
            ('Photography', 20),
        ],
        'average_salary': 'NPR 1,200,000 - 3,000,000 per year',
        'growth_outlook': '+24% YoY',
    },
    {
        'title': 'Mobile App Developer',
        'description': 'Build cross-platform mobile applications using modern frameworks. Focus on performance, usability, and native-like experience.',
        'category': 'Technology',
        'required_skills': [
            ('Flutter', 60),
            ('Dart', 50),
            ('Python Programming', 20),
            ('UI/UX Design', 30),
        ],
        'average_salary': 'NPR 1,400,000 - 3,200,000 per year',
        'growth_outlook': '+26% YoY',
    },
    {
        'title': 'Content Creator',
        'description': 'Produce engaging multimedia content for social media, YouTube, and brand campaigns. Skilled in video, photography, and copywriting.',
        'category': 'Media',
        'required_skills': [
            ('Video Editing', 50),
            ('Photography', 40),
            ('Content Writing', 50),
            ('Graphic Design', 30),
        ],
        'average_salary': 'NPR 800,000 - 2,500,000 per year',
        'growth_outlook': '+22% YoY',
    },
]

created = []
for data in careers_data:
    career, created_flag = CareerPath.objects.get_or_create(
        title=data['title'],
        defaults={
            'description': data['description'],
            'category': data['category'],
            'average_salary': data['average_salary'],
            'growth_outlook': data['growth_outlook'],
            'estimated_hours_per_skill': {},
        }
    )
    if created_flag:
        skill_objs = []
        hours_map = {}
        for skill_name, hours in data['required_skills']:
            skill = get_skill(skill_name)
            if skill:
                skill_objs.append(skill)
                hours_map[str(skill.id)] = hours
            else:
                print(f'  Warning: skill "{skill_name}" not found for career "{data["title"]}"')
        if skill_objs:
            career.required_skills.set(skill_objs)
            career.estimated_hours_per_skill = hours_map
            career.save()
            created.append(career.title)
            print(f'Created career: {career.title} ({len(skill_objs)} skills)')
        else:
            career.delete()
            print(f'  Skipped "{data["title"]}" — no valid skills found')
    else:
        print(f'Already exists: {data["title"]}')

print(f'\nDone. Created {len(created)} new careers.')
