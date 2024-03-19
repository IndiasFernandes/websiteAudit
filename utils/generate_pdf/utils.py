from reportlab.lib.units import cm as cm_unit

def cm(val):
    if val != 0:
        return val * cm_unit
    else:
        return cm_unit

def diff(arr):
    total = arr[0]
    for i in arr[1:]:
        total -= i

    return total
