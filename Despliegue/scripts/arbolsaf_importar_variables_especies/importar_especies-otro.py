import matplotlib.pyplot as plt
from shapely.geometry import Polygon





polygon1_coords = [
    (-86.109286248,11.946898956),
    (-86.109159886,11.947196373),
    (-86.108962101,11.947092456),
    (-86.10886504,11.946897164),
    (-86.109286248,11.946898956)]

polygon2_coords = [
    (-86.110055411,11.946895372),
    (-86.110046254,11.94718204),
    (-86.109172705,11.947194581),
    (-86.109313718,11.946900747),
    (-86.110055411,11.946895372)
    ]


polygon1_coordsold = [
    (11.946898956, -86.109286248),
    (11.947196373, -86.109159886),
    (11.947092456, -86.108962101),
    (11.946897164, -86.10886504),
    (11.946898956, -86.109286248)
    ]

polygon2_coordsold = [
    (11.946895372, -86.110055411),
    (11.94718204 , -86.110046254),
    (11.947194581, -86.109172705),
    (11.946900747, -86.109313718),
    (11.946895372, -86.110055411)
    ]

polygon3_coords = [
    (-86.110062,11.946459),
    (-86.110062,11.946889),
    (-86.10886,11.946889),
    (-86.10886,11.946459),
    (-86.110062,11.946459)
    ]


x1 = [p[0] for p in polygon1_coords]
y1 = [p[1] for p in polygon1_coords]

fig, ax = plt.subplots()
ax.plot(x1, y1)

x2 = [p[0] for p in polygon2_coords]
y2 = [p[1] for p in polygon2_coords]


ax.plot(x2, y2)

x3 = [p[0] for p in polygon3_coords]
y3 = [p[1] for p in polygon3_coords]


ax.plot(x3, y3)

for i, p in enumerate(polygon1_coords):
    ax.annotate(f"{i}", (p[0], p[1]))

for i, p in enumerate(polygon2_coords):
    ax.annotate(f"{i}", (p[0], p[1]))
for i, p in enumerate(polygon3_coords):
    ax.annotate(f"{i}", (p[0], p[1]))

label_location = Polygon(polygon1_coords).representative_point()
ax.annotate("A", label_location.coords[:][0])

label_location = Polygon(polygon2_coords).representative_point()
ax.annotate("B", label_location.coords[:][0])

label_location = Polygon(polygon3_coords).representative_point()
ax.annotate("C", label_location.coords[:][0])

plt.axis('off')


plt.savefig('foo.png', bbox_inches='tight')
plt.show()

print(plt)
"""
import staticmaps

context = staticmaps.Context()
context.set_tile_provider(staticmaps.tile_provider_OSM)

polygon = [
    (11.946898955783189, -86.1092862482307 ),
    (11.947196373156675, -86.10915988584337 ),
    (11.947196373156675, -86.10896210123707),
    (11.946897164111272, -86.1088650402729),
    (11.946898955783189, -86.1092862482307)
]

polygon2 = [
    (12.132481, -86.239511),
    (12.132093,-86.239344 ),
    (12.132287, -86.23876),
    (12.132481, -86.239511)
]



context.add_object(
    staticmaps.Area(
        [staticmaps.create_latlng(lat, lng) for lat, lng in polygon2],
        fill_color=staticmaps.parse_color("#00FF003F"),
        width=2,
        color=staticmaps.BLUE,
    )
)

frankfurt = staticmaps.create_latlng(12.132093,-86.239344 )
context.add_object(staticmaps.Marker(frankfurt, color=staticmaps.RED, size=12))
context.set_zoom(19)
# render non-anti-aliased png
image = context.render_pillow(800, 500)
image.save("polygon.pillow.png")

# render anti-aliased png (this only works if pycairo is installed)
image = context.render_cairo(800, 500)
image.write_to_png("polygon.cairo.png")

# render svg
svg_image = context.render_svg(800, 500)
with open("polygon.svg", "w", encoding="utf-8") as f:
    svg_image.write(f, pretty=True)


import staticmaps

context = staticmaps.Context()
context.set_tile_provider(staticmaps.tile_provider_OSM)
#context.set_tile_provider(staticmaps.tile_provider_StamenToner)

staticmaps.tile_provider_OSM
frankfurt = staticmaps.create_latlng(50.110644, 8.682092)
newyork = staticmaps.create_latlng(40.712728, -74.006015)


managua = staticmaps.create_latlng(12.1150, -86.2362)


#context.add_object(staticmaps.Line([frankfurt, newyork], color=staticmaps.BLUE, width=4))
#context.add_object(staticmaps.Marker(frankfurt, color=staticmaps.GREEN, size=12))
#context.add_object(staticmaps.Marker(newyork, color=staticmaps.RED, size=12))

context.add_object(staticmaps.Marker(managua, color=staticmaps.GREEN, size=12))

# render non-anti-aliased png
image = context.render_pillow(800, 500)
image.save("frankfurt_newyork.pillow.png")

# render anti-aliased png (this only works if pycairo is installed)
image = context.render_cairo(800, 500)
image.write_to_png("frankfurt_newyork.cairo.png")

# render svg
svg_image = context.render_svg(800, 500)
with open("frankfurt_newyork.svg", "w", encoding="utf-8") as f:
    svg_image.write(f, pretty=True)
"""


