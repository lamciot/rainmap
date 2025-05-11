# management/commands/import_shapefile.py
import geopandas as gpd
from django.core.management.base import BaseCommand
from your_app.models import ShapefileFeature

class Command(BaseCommand):
    help = 'Imports shapefile data into the database'

    def add_arguments(self, parser):
        parser.add_argument('shapefile_path', type=str)

    def handle(self, *args, **options):
        path = options['shapefile_path']
        gdf = gpd.read_file(path)
        
        for index, row in gdf.iterrows():
            ShapefileFeature.objects.create(
                name=row.get('name', f'feature_{index}'),  # Adjust based on your shapefile attributes
                geometry=row.geometry.wkt
            )
        
        self.stdout.write(self.style.SUCCESS('Successfully imported shapefile'))