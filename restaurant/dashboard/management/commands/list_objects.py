from django.core.management.base import BaseCommand
from dashboard.models import CustomUser, Dish, DishReview, Driver

class Command(BaseCommand):
    help = "List all objects in the database with their fields for CustomUser, Dish, DishReview, and Driver models"

    def handle(self, *args, **kwargs):
        users = CustomUser.objects.all()
        if users.exists():
            self.stdout.write("CustomUser objects:")
            for user in users:
                self.stdout.write(f" - {user}")
                self._print_object_fields(user)
        else:
            self.stdout.write("No CustomUser objects found.")
        
        dishes = Dish.objects.all()
        if dishes.exists():
            self.stdout.write("\nDish objects:")
            for dish in dishes:
                self.stdout.write(f" - {dish}")
                self._print_object_fields(dish)
        else:
            self.stdout.write("\nNo Dish objects found.")
        
        dish_reviews = DishReview.objects.all()
        if dish_reviews.exists():
            self.stdout.write("\nDishReview objects:")
            for review in dish_reviews:
                self.stdout.write(f" - {review}")
                self._print_object_fields(review)
        else:
            self.stdout.write("\nNo DishReview objects found.")
        
        drivers = Driver.objects.all()
        if drivers.exists():
            self.stdout.write("\nDriver objects:")
            for driver in drivers:
                self.stdout.write(f" - {driver}")
                self._print_object_fields(driver)
        else:
            self.stdout.write("\nNo Driver objects found.")

    def _print_object_fields(self, obj):
        """Helper method to print all fields and their values for an object"""
        for field in obj._meta.get_fields():
            if field.is_relation:
                continue
            field_name = field.name
            field_value = getattr(obj, field_name)
            self.stdout.write(f"    {field_name}: {field_value}")
