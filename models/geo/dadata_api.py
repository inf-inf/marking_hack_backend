from dadata import Dadata

from config.geo import DADATA_API_KEY


def get_lon_lat_by_postal_code(postal_code: int | str):
    dadata = Dadata(DADATA_API_KEY)
    result = dadata.suggest("postal_unit", str(postal_code))
    print(result)
