from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

User = get_user_model()


class BodyStatsDiary(models.Model):
    """BodyStatsDiary model with user body measurements."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='спортсмен',
        related_name='bodystats_diary',
    )
    date = models.DateField(
        verbose_name='дата параметров',
        db_index=True,
    )
    abdominal = models.FloatField(
        verbose_name='живот',
        validators=[MinValueValidator(30), MaxValueValidator(250)],
        blank=True,
        null=True,
    )
    chest = models.FloatField(
        verbose_name='грудь',
        validators=[MinValueValidator(30), MaxValueValidator(250)],
        blank=True,
        null=True,
    )
    hips = models.FloatField(
        verbose_name='бедра',
        validators=[MinValueValidator(30), MaxValueValidator(250)],
        blank=True,
        null=True,
    )
    neck = models.FloatField(
        verbose_name='шея',
        validators=[MinValueValidator(20), MaxValueValidator(100)],
        blank=True,
        null=True,
    )
    waist = models.FloatField(
        verbose_name='талия',
        validators=[MinValueValidator(30), MaxValueValidator(250)],
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ['-date']
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'date'),
                name='unique_bodystats_diary'
            )
        ]

    def __str__(self):
        return f'Дневник параметров {self.user.username} за {self.date} г.'


class FoodDiary(models.Model):
    """FoodDiary model with user food diary data."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='спортсмен',
        related_name='food_diary',
    )
    date = models.DateField(
        verbose_name='дата питания',
        db_index=True,
    )
    calories_actual = models.PositiveSmallIntegerField(
        verbose_name='калории факт',
        validators=[MinValueValidator(0), MaxValueValidator(10_000)],
        blank=True,
        null=True,
    )
    calories_target = models.PositiveSmallIntegerField(
        verbose_name='калории план',
        validators=[MinValueValidator(0), MaxValueValidator(10_000)],
        blank=True,
        null=True,
    )
    carbohydrate_actual = models.FloatField(
        verbose_name='углеводы факт',
        validators=[MinValueValidator(0), MaxValueValidator(1_000)],
        blank=True,
        null=True,
    )
    carbohydrate_target = models.PositiveSmallIntegerField(
        verbose_name='углеводы план',
        validators=[MinValueValidator(0), MaxValueValidator(1_000)],
        blank=True,
        null=True,
    )
    fat_actual = models.FloatField(
        verbose_name='жиры факт',
        validators=[MinValueValidator(0), MaxValueValidator(1_000)],
        blank=True,
        null=True,
    )
    fat_target = models.PositiveSmallIntegerField(
        verbose_name='жиры план',
        validators=[MinValueValidator(0), MaxValueValidator(1_000)],
        blank=True,
        null=True,
    )
    fiber_actual = models.FloatField(
        verbose_name='пищевые волокна факт',
        validators=[MinValueValidator(0), MaxValueValidator(1_000)],
        blank=True,
        null=True,
    )
    fiber_target = models.PositiveSmallIntegerField(
        verbose_name='пищевые волокна план',
        validators=[MinValueValidator(0), MaxValueValidator(1_000)],
        blank=True,
        null=True,
    )
    protein_actual = models.FloatField(
        verbose_name='белки факт',
        validators=[MinValueValidator(0), MaxValueValidator(1_000)],
        blank=True,
        null=True,
    )
    protein_target = models.PositiveSmallIntegerField(
        verbose_name='белки план',
        validators=[MinValueValidator(0), MaxValueValidator(1_000)],
        blank=True,
        null=True,
    )
    sugar_actual = models.FloatField(
        verbose_name='сахар факт',
        validators=[MinValueValidator(0), MaxValueValidator(1_000)],
        blank=True,
        null=True,
    )
    sugar_target = models.PositiveSmallIntegerField(
        verbose_name='сахар план',
        validators=[MinValueValidator(0), MaxValueValidator(1_000)],
        blank=True,
        null=True,
    )
    weight_actual = models.FloatField(
        verbose_name='вес факт',
        validators=[MinValueValidator(30), MaxValueValidator(250)],
        blank=True,
        null=True,
    )
    weight_target = models.FloatField(
        verbose_name='вес план',
        validators=[MinValueValidator(30), MaxValueValidator(250)],
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ['-date']
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'date'),
                name='unique_food_diary'
            )
        ]

    def __str__(self):
        return f'Дневник питания {self.user.username} за {self.date} г.'


class Project(models.Model):
    """Project model."""

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name='спортсмен',
        related_name='project_user',
    )
    coach = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='тренер',
        related_name='project_coach',
    )
    start_date = models.DateField(
        verbose_name='дата начала проекта',
        db_index=True,
    )
    start_weight = models.FloatField(
        verbose_name='начальный вес',
        validators=[MinValueValidator(30), MaxValueValidator(250)],
    )
    target_calories = models.PositiveSmallIntegerField(
        verbose_name='калории план',
        validators=[MinValueValidator(0), MaxValueValidator(10_000)],
    )
    target_carbohydrate = models.PositiveSmallIntegerField(
        verbose_name='углеводы план',
        validators=[MinValueValidator(0), MaxValueValidator(1_000)],
    )
    target_fat = models.PositiveSmallIntegerField(
        verbose_name='жиры план',
        validators=[MinValueValidator(0), MaxValueValidator(1_000)],
    )
    target_fiber = models.PositiveSmallIntegerField(
        verbose_name='пищевые волокна план',
        validators=[MinValueValidator(0), MaxValueValidator(1_000)],
    )
    target_protein = models.PositiveSmallIntegerField(
        verbose_name='белки план',
        validators=[MinValueValidator(0), MaxValueValidator(1_000)],
    )
    target_sugar = models.PositiveSmallIntegerField(
        verbose_name='сахар план',
        validators=[MinValueValidator(0), MaxValueValidator(1_000)],
    )
    target_weight = models.FloatField(
        verbose_name='целевой вес',
        validators=[MinValueValidator(30), MaxValueValidator(250)],
    )

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return f'{self.user.username}, целевой вес {self.target_weight} кг.'
