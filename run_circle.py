"""跑步轨迹记录器 v2：换一组数据（环形跑），对比看图形怎么变

跑法：python D:\learn\12-run-tracker\run_circle.py
产出：D:\learn\12-run-tracker\route_circle.svg（原来的 route.svg 不会被覆盖）
"""
from math import asin, cos, radians, sin, sqrt

EARTH_RADIUS_KM = 6371.0

# 一组环形路线的点（假设在操场附近绕了一圈），纬度经度都在变
POINTS = [
    (39.9080, 116.3970),
    (39.9088, 116.3972),
    (39.9094, 116.3980),
    (39.9096, 116.3990),
    (39.9092, 116.3998),
    (39.9084, 116.3999),
    (39.9078, 116.3992),
    (39.9076, 116.3982),
    (39.9080, 116.3970),   # 回到起点，闭合
]
MINUTES = 18
SECONDS = 40

WIDTH, HEIGHT, PAD = 480, 480, 40
OUT = r"D:\learn\12-run-tracker\route_circle.svg"


def distance_km(lat1, lon1, lat2, lon2):
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    return 2 * EARTH_RADIUS_KM * asin(sqrt(a))


def total_distance(points):
    return sum(distance_km(*points[i], *points[i + 1]) for i in range(len(points) - 1))


def to_xy(points):
    lats = [p[0] for p in points]
    lons = [p[1] for p in points]
    lat_min, lon_min = min(lats), min(lons)
    span = max(max(lats) - lat_min, max(lons) - lon_min, 1e-6)
    scale = (min(WIDTH, HEIGHT) - 2 * PAD) / span
    return [(PAD + (lon - lon_min) * scale,
             HEIGHT - PAD - (lat - lat_min) * scale) for lat, lon in points]


def main():
    km = total_distance(POINTS)
    total_seconds = MINUTES * 60 + SECONDS
    pace_seconds = total_seconds / km
    m, s = divmod(pace_seconds, 60)

    xy = to_xy(POINTS)
    polyline = " ".join(f"{x:.1f},{y:.1f}" for x, y in xy)
    dots = "".join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4" fill="#ef4444"/>' for x, y in xy)
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}">
  <rect width="100%" height="100%" fill="#f8fafc"/>
  <polyline points="{polyline}" fill="none" stroke="#16a34a" stroke-width="4" stroke-linejoin="round"/>
  {dots}
  <text x="{PAD}" y="28" font-family="system-ui" font-size="16" fill="#111">环形跑 {km:.3f} 公里 · 配速 {int(m)}'{int(s):02d}\"/km</text>
</svg>"""
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(svg)

    print(f"点数：{len(POINTS)}（{len(POINTS) - 1} 段）")
    print(f"总距离：{km:.3f} 公里（{km * 1000:.0f} 米）")
    print(f"总时长：{total_seconds} 秒（{MINUTES} 分 {SECONDS} 秒）")
    print(f"平均配速：{int(m)}'{int(s):02d}\"/公里")
    print(f"新图已生成：{OUT}")


if __name__ == "__main__":
    main()
