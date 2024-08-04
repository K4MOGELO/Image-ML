from backend.calculations.regModel.pothole_model import getPotholePrice
from crack import getCrackPrice
from full import getRepairPrice

def getPrice(service):
    if service == 'pothole':
        price = getPotholePrice(6.2, 1, 0)
    if service == 'crack':
        price = getCrackPrice(2.3, 1, 0)
    elif service == 'full':
        price = getRepairPrice(5.5, 1)
    else:
        return 'Error'
    return price
    
    