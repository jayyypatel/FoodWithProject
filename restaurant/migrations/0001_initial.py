# Generated by Django 3.2.7 on 2022-02-01 11:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('branch', models.CharField(max_length=30)),
                ('street_address', models.CharField(max_length=70)),
                ('city', models.CharField(max_length=35)),
                ('pincode', models.IntegerField()),
                ('state', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=20, null=True)),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('time', models.TimeField(default=django.utils.timezone.now)),
                ('num_of_person', models.CharField(max_length=3)),
                ('reserved_table', models.CharField(blank=True, max_length=3, null=True)),
                ('total_price', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'get_latest_by': 'pk',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Decoration_category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('decoration_type', models.CharField(choices=[('none', 'None'), ('birthday', 'Birthday'), ('anniversary', 'Anniversary'), ('wedding', 'Wedding'), ('party', 'Party'), ('Candle-light', 'Candle-light')], default='none', max_length=20)),
                ('deco_price', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('final_price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('order_date', models.DateField(default=django.utils.timezone.now)),
                ('order_status', models.CharField(choices=[('confirmed', 'Confirmed'), ('canceled', 'Canceled')], default='confirmed', max_length=10)),
                ('tbl_bookingid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_Booking', to='restaurant.booking')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_usertbl', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.DecimalField(decimal_places=2, max_digits=7)),
                ('feedback', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('restaurant_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=30)),
                ('contact_no', models.CharField(max_length=10)),
                ('opening_hours', models.CharField(max_length=15)),
                ('takeaway', models.BooleanField()),
                ('picture', models.ImageField(blank=True, null=True, upload_to='images')),
                ('minimum_or', models.IntegerField(blank=True, null=True)),
                ('description', models.CharField(blank=True, max_length=100, null=True)),
                ('address_fk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rest_address', to='restaurant.address')),
                ('category_fk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rest_category', to='restaurant.category')),
                ('rating_fk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rest_rating', to='restaurant.rating')),
            ],
        ),
        migrations.CreateModel(
            name='Table',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=False)),
                ('date', models.DateField(blank=True, default=django.utils.timezone.now, null=True)),
                ('time', models.TimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('tbl_name', models.CharField(blank=True, max_length=10, null=True, unique=True)),
                ('restaurant_fk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='table_rest', to='restaurant.restaurant')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(db_index=True, max_length=30)),
                ('price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('description', models.CharField(max_length=83)),
                ('product_img', models.ImageField(blank=True, null=True, upload_to='images')),
                ('discount', models.IntegerField()),
                ('available', models.BooleanField(blank=True, default=True, null=True)),
                ('category_fk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_category', to='restaurant.category')),
                ('restaurant_fk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rest_product', to='restaurant.restaurant')),
            ],
        ),
        migrations.CreateModel(
            name='Order_details',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=8)),
                ('order_fk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_detail_order', to='restaurant.order')),
                ('product_fk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_detail_product', to='restaurant.product')),
            ],
        ),
        migrations.CreateModel(
            name='Decoration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('decoration_cat_fk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='deco_deco_category', to='restaurant.decoration_category')),
                ('restaurant_fk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='deco_restaurant', to='restaurant.restaurant')),
            ],
        ),
        migrations.CreateModel(
            name='booking_details',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, default=django.utils.timezone.now, null=True)),
                ('time', models.TimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('booking_fk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bdetails_booking', to='restaurant.booking')),
                ('table_fk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bdetails_table', to='restaurant.table')),
            ],
        ),
        migrations.AddField(
            model_name='booking',
            name='decoration_fk',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='booking_decocat', to='restaurant.decoration_category'),
        ),
        migrations.AddField(
            model_name='booking',
            name='restaurant_fk',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='booking_rest', to='restaurant.restaurant'),
        ),
        migrations.AddField(
            model_name='booking',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='booking_usertbl', to=settings.AUTH_USER_MODEL),
        ),
    ]