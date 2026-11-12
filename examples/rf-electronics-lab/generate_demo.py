"""生成完全虚构的 8m × 6m 射频/电子学实验室 A/B HouseSpec。

所有尺寸、设备、点位和接口均为演示用虚构或推断值，不来自实测。
脚本只生成 JSON；HTML 由仓库内的 build.py 构建。
"""

import argparse
import json
from pathlib import Path


def wall_h(y, x0, x1, openings=()):
    wall = {
        "a": [x0, y],
        "b": [x1, y],
        "t": 200,
        "bearing": False,
        "bearingFrom": "inferred",
    }
    if openings:
        wall["openings"] = list(openings)
    return wall


def wall_v(x, y0, y1, openings=()):
    wall = {
        "a": [x, y0],
        "b": [x, y1],
        "t": 200,
        "bearing": False,
        "bearingFrom": "inferred",
    }
    if openings:
        wall["openings"] = list(openings)
    return wall


def furniture(key, x, y, name, rot=0, **kwargs):
    return {
        "key": key,
        "at": [x, y],
        "rot": rot,
        "name": f"{name}（虚构）",
        **kwargs,
    }


def point(kind, x, y, rot, h):
    return {"kind": kind, "at": [x, y], "rot": rot, "h": h}


def free_box(x, y, name, w, d, h, rot=0, color="#59636e", z=None):
    kwargs = {
        "w": w,
        "d": d,
        "h": h,
        "color": color,
        "opt": {"shape": "box", "mat": "metal"},
    }
    if z is not None:
        kwargs["z"] = z
    return furniture("freeBox", x, y, name, rot, **kwargs)


def common_walls():
    entry = {
        "type": "door",
        "from": 900,
        "to": 2000,
        "hinge": "from",
        "into": [1450, 5000],
        "entry": True,
        "unsure": "门位、门宽和开向均为虚构演示，不是现场测绘或消防疏散设计。",
    }
    passage = {
        "type": "hole",
        "from": 3200,
        "to": 4800,
        "head": 2400,
        "unsure": "内分区与开放洞口均为虚构演示，用于讨论机柜/储物区与实验操作区的关系。",
    }
    partition = wall_v(2600, 100, 5900, [passage])
    partition["t"] = 120
    return [
        partition,
        wall_h(100, 100, 7900),
        wall_v(7900, 100, 5900),
        wall_h(5900, 100, 7900, [entry]),
        wall_v(100, 100, 5900),
    ]


def common_comments():
    return [
        {
            "at": [4000, 3000],
            "text": "完全虚构的概念实验室：无真实地址、客户、订单、实测数据或工程资料。所有尺寸和设备仅用于交互展示。",
        },
        {
            "at": [400, 400],
            "text": "墙体厚度、非承重属性和 3000mm 层高均为推断；未做结构、承重或拆改计算。",
        },
        {
            "at": [7400, 1400],
            "text": "设备外形是通用几何占位，不代表真实品牌、型号、重量、散热或安全认证。",
        },
        {
            "at": [7400, 3200],
            "text": "给排水和冷却接口仅作需求沟通；未做水力、排水、泄漏或防水计算，须由专业人员确认。",
        },
        {
            "at": [2200, 5600],
            "text": "插座、网络和自动管线是通用引擎生成的概念点位，不是配电、接地、EMC 或消防设计。",
        },
    ]


def layout_a():
    items = [
        furniture("garageShelf", 1600, 500, "耗材储物 S1", w=1600, d=600, h=2000),
        free_box(600, 1400, "机柜 R1", 800, 800, 2100, 270, "#39434e"),
        free_box(600, 2600, "机柜 R2", 800, 800, 2100, 270, "#39434e"),
        free_box(3800, 650, "真空设备 V1", 1400, 900, 1200, 0, "#9aa5ad"),
        free_box(5700, 600, "射频设备 RF1", 1000, 800, 1500, 0, "#52677b"),
        free_box(7400, 1400, "闭式冷却机组 CU1", 900, 800, 1200, 90, "#53838c"),
        furniture(
            "freeRoundBox",
            4500,
            2800,
            "光学/实验平台 T1",
            w=2400,
            d=1400,
            h=900,
            color="#4d565e",
            opt={"shape": "roundBox", "mat": "metal", "r": 40},
        ),
        free_box(4050, 2750, "示波器 T1-A", 500, 350, 300, 0, "#303b47", 900),
        free_box(4950, 2750, "射频源 T1-B", 500, 350, 300, 0, "#303b47", 900),
        furniture("desk", 4000, 5400, "控制台 C1", 180, w=2200, d=800),
        furniture("officeChair", 3500, 4500, "控制席 C1-A"),
        furniture("officeChair", 4500, 4500, "控制席 C1-B"),
        furniture("rug", 6600, 4500, "维护预留区 M1", w=1800, d=1800, color="#d5b85c"),
    ]
    elec = [
        point("socket16", 200, 2000, -90, 300),
        point("socket16", 200, 3400, -90, 300),
        point("socket16", 3000, 200, 0, 1100),
        point("socket16", 6400, 200, 0, 1100),
        point("socket16", 7800, 2200, 90, 300),
        point("socketUSB", 5000, 5800, 180, 1100),
        point("net", 5400, 5800, 180, 300),
        point("cold", 7800, 2500, 90, 600),
        point("waste", 7800, 3000, 90, 300),
    ]
    structs = [
        {"kind": "shaft", "at": [7550, 3200], "w": 300, "d": 400},
        {"kind": "drain", "at": [7350, 3200]},
    ]
    return items, elec, structs


def layout_b():
    items = [
        furniture("garageShelf", 1600, 500, "耗材储物 S1", w=1600, d=600, h=2000),
        free_box(600, 1400, "机柜 R1", 800, 800, 2100, 270, "#39434e"),
        free_box(600, 2600, "机柜 R2", 800, 800, 2100, 270, "#39434e"),
        furniture("desk", 4000, 600, "控制台 C1", 0, w=2200, d=800),
        furniture("officeChair", 3500, 1550, "控制席 C1-A", 180),
        furniture("officeChair", 4500, 1550, "控制席 C1-B", 180),
        furniture(
            "freeRoundBox",
            4500,
            3200,
            "光学/实验平台 T1",
            w=2400,
            d=1400,
            h=900,
            color="#4d565e",
            opt={"shape": "roundBox", "mat": "metal", "r": 40},
        ),
        free_box(4050, 3150, "示波器 T1-A", 500, 350, 300, 0, "#303b47", 900),
        free_box(4950, 3150, "射频源 T1-B", 500, 350, 300, 0, "#303b47", 900),
        free_box(7400, 1400, "真空设备 V1", 900, 800, 1200, 90, "#9aa5ad"),
        free_box(7400, 2900, "射频设备 RF1", 900, 800, 1500, 90, "#52677b"),
        free_box(6800, 5400, "闭式冷却机组 CU1", 1000, 800, 1200, 180, "#53838c"),
        furniture("rug", 4500, 4750, "维护预留区 M1", w=1800, d=1500, color="#d5b85c"),
    ]
    elec = [
        point("socket16", 200, 2000, -90, 300),
        point("socket16", 200, 3400, -90, 300),
        point("socketUSB", 5500, 200, 0, 1100),
        point("net", 5900, 200, 0, 300),
        point("socket16", 7800, 2200, 90, 1100),
        point("socket16", 7800, 3600, 90, 1100),
        point("socket16", 5900, 5800, 180, 300),
        point("cold", 7800, 4000, 90, 600),
        point("waste", 7800, 4600, 90, 300),
    ]
    structs = [
        {"kind": "shaft", "at": [7550, 4200], "w": 300, "d": 400},
        {"kind": "drain", "at": [7350, 4200]},
    ]
    return items, elec, structs


def make_spec(layout):
    if layout == "A":
        items, elec, structs = layout_a()
        title = "澄波实验室 · A 集中岛式（完全虚构）"
        layout_note = "A 集中岛式：中央实验平台，南侧控制台，北侧真空/射频设备，东侧冷却，东南维护区。"
    else:
        items, elec, structs = layout_b()
        title = "澄波实验室 · B 设备周边式（完全虚构）"
        layout_note = "B 设备周边式：北侧控制台，东侧真空/射频设备，中央实验平台，东南冷却，南侧维护区。"
    return {
        "name": title,
        "height": 3000,
        "heightFrom": "estimated",
        "phase": "renovate",
        "demo": True,
        "privacy": "fully_fictional",
        "dataOrigin": "synthetic_concept_only",
        "layout": layout,
        "layoutNote": layout_note,
        "engineeringStatus": "unverified_concept_not_for_construction",
        "walls": common_walls(),
        "rooms": [
            {
                "at": [1600, 2000],
                "name": "机柜/储物区（虚构）",
                "mat": "epoxy",
                "wallMat": "latexGrey",
                "ceil": {"type": "flat", "drop": 200, "color": "#e8ecef"},
                "skirting": "metal",
            },
            {
                "at": [5800, 3400],
                "name": "射频/电子学实验室（虚构）",
                "mat": "epoxy",
                "wallMat": "latexGrey",
                "ceil": {"type": "flat", "drop": 200, "color": "#e8ecef"},
                "skirting": "metal",
            }
        ],
        "structs": structs,
        "furniture": items,
        "elec": elec,
        "autoElec": True,
        "mep": {"power": "ceil", "water": "ceil", "floorStyle": "ortho"},
        "look": {"style": "diorama", "palette": "industrial", "labels": True},
        "dims": [
            {
                "name": "虚构东西向墙中线",
                "line": "y=5900",
                "from": 100,
                "segs": [7800],
                "ref": "center",
            },
            {
                "name": "虚构南北向墙中线",
                "line": "x=7900",
                "from": 100,
                "segs": [5800],
                "ref": "center",
            },
            {
                "name": "虚构内分区定位",
                "line": "y=100",
                "from": 100,
                "segs": [2500, 5300],
                "ref": "center",
            },
            {
                "name": "虚构入口门洞",
                "line": "y=5900",
                "from": 900,
                "segs": [1100],
                "ref": "face",
            },
        ],
        "expectDims": {
            "top": [200, 2340, 120, 5140, 200],
            "bottom": [200, 2340, 120, 5140, 200],
            "left": [200, 5600, 200],
            "right": [200, 5600, 200],
        },
        "comments": common_comments(),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    outputs = {
        "spec.json": make_spec("A"),
        "spec-layout-b.json": make_spec("B"),
    }
    for filename, spec in outputs.items():
        target = args.output_dir / filename
        target.write_text(json.dumps(spec, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"generated {target.name}: layout={spec['layout']}, furniture={len(spec['furniture'])}")


if __name__ == "__main__":
    main()
