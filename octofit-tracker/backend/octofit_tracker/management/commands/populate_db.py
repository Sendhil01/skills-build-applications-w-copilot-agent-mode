
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from octofit_tracker.models import Team, Activity, Leaderboard, Workout
from django.conf import settings
from pymongo import MongoClient

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'


    def handle(self, *args, **kwargs):
        # Drop collections directly for a clean state
        client = MongoClient('mongodb://localhost:27017/')
        db = client['octofit_db']
        db['octofit_tracker_team'].drop()
        db['octofit_tracker_activity'].drop()
        db['octofit_tracker_leaderboard'].drop()
        db['octofit_tracker_workout'].drop()
        db['auth_user'].drop()

        User = get_user_model()

        # Create Teams
        marvel = Team.objects.create(name='Marvel')
        dc = Team.objects.create(name='DC')

        # Create Users (no team field, so just create users)
        ironman = User.objects.create_user(username='ironman', email='ironman@marvel.com', password='pass')
        captain = User.objects.create_user(username='captain', email='captain@marvel.com', password='pass')
        batman = User.objects.create_user(username='batman', email='batman@dc.com', password='pass')
        superman = User.objects.create_user(username='superman', email='superman@dc.com', password='pass')

        # Create Activities
        Activity.objects.create(user=ironman, type='run', duration=30)
        Activity.objects.create(user=batman, type='cycle', duration=45)

        # Create Workouts
        Workout.objects.create(name='Morning Cardio', description='Cardio for all heroes')
        Workout.objects.create(name='Strength Training', description='Strength for all heroes')

        # Create Leaderboard
        Leaderboard.objects.create(team=marvel, points=100)
        Leaderboard.objects.create(team=dc, points=90)

        self.stdout.write(self.style.SUCCESS('octofit_db populated with test data'))
