from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Workout, Leaderboard

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **kwargs):
        # Clear existing data
        Leaderboard.objects.all().delete()
        Activity.objects.all().delete()
        Workout.objects.all().delete()
        User.objects.all().delete()
        Team.objects.all().delete()

        # Create teams
        marvel = Team.objects.create(name='marvel', description='Marvel Superheroes')
        dc = Team.objects.create(name='dc', description='DC Superheroes')

        # Create users
        ironman = User.objects.create(name='Iron Man', email='ironman@marvel.com', team='marvel')
        captain = User.objects.create(name='Captain America', email='cap@marvel.com', team='marvel')
        batman = User.objects.create(name='Batman', email='batman@dc.com', team='dc')
        superman = User.objects.create(name='Superman', email='superman@dc.com', team='dc')

        # Create workouts
        pushups = Workout.objects.create(name='Pushups', description='Do 20 pushups', suggested_for='marvel')
        running = Workout.objects.create(name='Running', description='Run 5km', suggested_for='dc')

        # Create activities
        Activity.objects.create(user=ironman, activity_type='pushups', duration=10, date='2024-01-01')
        Activity.objects.create(user=batman, activity_type='running', duration=30, date='2024-01-02')

        # Create leaderboard
        Leaderboard.objects.create(user=ironman, points=100)
        Leaderboard.objects.create(user=batman, points=120)

        self.stdout.write(self.style.SUCCESS('Test data populated successfully.'))
