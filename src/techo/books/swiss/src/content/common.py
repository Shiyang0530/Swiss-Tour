# Helpers for content files
def S(id, ja, g, t, lv, d, i=None, tip=None, u=None, star=0, dur=90, fl="", sm=None, n=None, ext=None):
    return dict(id=id, ja=ja, g=g, t=t.split(), lv=lv, d=d, i=i or {}, tip=tip, u=u,
                star=star, dur=dur, fl=fl, sm=sm, n=n, ext=ext)

def A(id, ja, d, c, i=None, tip=None, t="", n=None):
    return dict(id=id, ja=ja, d=d, c=c, i=i or {}, tip=tip, t=t.split(), n=n)

def R(id, ja, d, c, hub, hubn, i=None, tip=None, t="", n=None):
    return dict(id=id, ja=ja, d=d, c=c, hub=hub, hubn=hubn, i=i or {}, tip=tip, t=t.split(), n=n)

# season segments (month.fraction)
SKI = [[12.4, 13], [1, 4.5]]
SKI_LONG = [[11.2, 13], [1, 5.0]]
HIKE = [[6.0, 10.0]]
HIKE_HIGH = [[6.5, 9.9]]
HIKE_LOW = [[4.5, 10.9]]
AUTUMN = [[9.6, 10.9]]
LARCH = [[10.1, 10.9]]
XMAS = [[11.75, 12.8]]
