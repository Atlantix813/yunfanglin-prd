#!/usr/bin/env python3
import base64
import json
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.request
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
import websocket


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "_compare"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"


PAGES = {
    "pc-course-list": {
        "size": (1920, 1080),
        "live": "http://127.0.0.1:8300/course/vod/index",
        "proto": "http://127.0.0.1:8768/prototype/admin-course-embed-source.html",
        "live_key": "meedu-admin-token",
        "live_token": "ADMIN_TOKEN",
    },
    "h5-member": {
        "size": (430, 932),
        "live": "http://127.0.0.1:8200/member",
        "proto": "http://127.0.0.1:8768/prototype/member-center.html",
        "live_key": "meedu-h5-token",
        "live_token": "H5_TOKEN",
    },
    "h5-home": {
        "size": (430, 932),
        "live": "http://127.0.0.1:8200/",
        "proto": "http://127.0.0.1:8768/prototype/training-home.html",
        "live_key": "meedu-h5-token",
        "live_token": "H5_TOKEN",
    },
    "h5-course-detail": {
        "size": (430, 932),
        "live": "http://127.0.0.1:8200/course/19",
        "proto": "http://127.0.0.1:8768/prototype/course-detail.html",
        "live_key": "meedu-h5-token",
        "live_token": "H5_TOKEN",
    },
    "h5-video": {
        "size": (430, 932),
        "live": "http://127.0.0.1:8200/course/video/48",
        "proto": "http://127.0.0.1:8768/prototype/video-learning.html",
        "live_key": "meedu-h5-token",
        "live_token": "H5_TOKEN",
    },
    "h5-study": {
        "size": (430, 932),
        "live": "http://127.0.0.1:8200/study",
        "proto": "http://127.0.0.1:8768/prototype/member-learning.html",
        "live_key": "meedu-h5-token",
        "live_token": "H5_TOKEN",
    },
    "h5-vip": {
        "size": (430, 932),
        "live": "http://127.0.0.1:8200/role",
        "proto": "http://127.0.0.1:8768/prototype/h5-vip-source.html",
        "live_key": "meedu-h5-token",
        "live_token": "H5_TOKEN",
    },
    "h5-cashier": {
        "size": (430, 932),
        "live": "http://127.0.0.1:8200/order?goods_id=19&goods_name=社区矛盾调解沟通技巧&goods_label=录播课程&goods_charge=99&goods_type=vod",
        "proto": "http://127.0.0.1:8768/prototype/h5-cashier-source.html",
        "live_key": "meedu-h5-token",
        "live_token": "H5_TOKEN",
    },
    "h5-pay-success": {
        "size": (430, 932),
        "live": "http://127.0.0.1:8200/order/success",
        "proto": "http://127.0.0.1:8768/prototype/h5-pay-success-source.html",
        "live_key": "meedu-h5-token",
        "live_token": "H5_TOKEN",
    },
    "h5-my-orders": {
        "size": (430, 932),
        "live": "http://127.0.0.1:8200/member/order",
        "proto": "http://127.0.0.1:8768/prototype/h5-my-orders-source.html",
        "live_key": "meedu-h5-token",
        "live_token": "H5_TOKEN",
    },
    "pc-course-students": {
        "size": (1920, 1080),
        "live": "http://127.0.0.1:8300/course/vod/19/view",
        "proto": "http://127.0.0.1:8768/prototype/pc-course-students-source.html",
        "live_key": "meedu-admin-token",
        "live_token": "ADMIN_TOKEN",
    },
    "pc-video-management": {
        "size": (1920, 1080),
        "live": "http://127.0.0.1:8300/course/vod/video/index?course_id=19&title=社区矛盾调解沟通技巧",
        "proto": "http://127.0.0.1:8768/prototype/pc-video-management-source.html",
        "live_key": "meedu-admin-token",
        "live_token": "ADMIN_TOKEN",
    },
    "pc-video-sales": {
        "size": (1920, 1080),
        "live": "http://127.0.0.1:8300/course/vod/video/subscribe?course_id=19&video_id=48",
        "proto": "http://127.0.0.1:8768/prototype/pc-video-sales-source.html",
        "live_key": "meedu-admin-token",
        "live_token": "ADMIN_TOKEN",
    },
    "pc-member-list": {
        "size": (1920, 1080),
        "live": "http://127.0.0.1:8300/member/index",
        "proto": "http://127.0.0.1:8768/prototype/pc-member-list-source.html",
        "live_key": "meedu-admin-token",
        "live_token": "ADMIN_TOKEN",
    },
    "pc-member-detail": {
        "size": (1920, 1080),
        "live": "http://127.0.0.1:8300/member/1",
        "proto": "http://127.0.0.1:8768/prototype/pc-member-detail-source.html",
        "live_key": "meedu-admin-token",
        "live_token": "ADMIN_TOKEN",
    },
    "pc-order-list": {
        "size": (1920, 1080),
        "live": "http://127.0.0.1:8300/order/index",
        "proto": "http://127.0.0.1:8768/prototype/pc-order-list-source.html",
        "live_key": "meedu-admin-token",
        "live_token": "ADMIN_TOKEN",
    },
    "pc-order-refund": {
        "size": (1920, 1080),
        "live": "http://127.0.0.1:8300/order/refund",
        "proto": "http://127.0.0.1:8768/prototype/pc-order-refund-source.html",
        "live_key": "meedu-admin-token",
        "live_token": "ADMIN_TOKEN",
    },
    "pc-order-detail": {
        "size": (1920, 1080),
        "live": "http://127.0.0.1:8300/order/detail?id=1",
        "proto": "http://127.0.0.1:8768/prototype/pc-order-detail-source.html",
        "live_key": "meedu-admin-token",
        "live_token": "ADMIN_TOKEN",
    },
    "pc-transaction-stats": {
        "size": (1920, 1080),
        "live": "http://127.0.0.1:8300/stats/transaction/index",
        "proto": "http://127.0.0.1:8768/prototype/pc-transaction-stats-source.html",
        "live_key": "meedu-admin-token",
        "live_token": "ADMIN_TOKEN",
    },
    "pc-vip": {
        "size": (1920, 1080),
        "live": "http://127.0.0.1:8300/role",
        "proto": "http://127.0.0.1:8768/prototype/pc-vip-source.html",
        "live_key": "meedu-admin-token",
        "live_token": "ADMIN_TOKEN",
    },
    "pc-promocode": {
        "size": (1920, 1080),
        "live": "http://127.0.0.1:8300/promocode",
        "proto": "http://127.0.0.1:8768/prototype/pc-promocode-source.html",
        "live_key": "meedu-admin-token",
        "live_token": "ADMIN_TOKEN",
    },
    "pc-payment-config": {
        "size": (1920, 1080),
        "live": "http://127.0.0.1:8300/system/paymentConfig",
        "proto": "http://127.0.0.1:8768/prototype/pc-payment-config-source.html",
        "live_key": "meedu-admin-token",
        "live_token": "ADMIN_TOKEN",
    },
    "pc-content-stats": {
        "size": (1920, 1080),
        "live": "http://127.0.0.1:8300/stats/content/index",
        "proto": "http://127.0.0.1:8768/prototype/pc-content-stats-source.html",
        "live_key": "meedu-admin-token",
        "live_token": "ADMIN_TOKEN",
    },
    "pc-member-stats": {
        "size": (1920, 1080),
        "live": "http://127.0.0.1:8300/stats/member/index",
        "proto": "http://127.0.0.1:8768/prototype/admin-stats.html",
        "live_key": "meedu-admin-token",
        "live_token": "ADMIN_TOKEN",
    },
    "pc-message-config": {
        "size": (1920, 1080),
        "live": "http://127.0.0.1:8300/system/messageConfig",
        "proto": "http://127.0.0.1:8768/prototype/notification-settings.html",
        "live_key": "meedu-admin-token",
        "live_token": "ADMIN_TOKEN",
    },
}


class CDP:
    def __init__(self, port: int):
        self.port = port
        self.proc = None
        self.ws = None
        self.seq = 0
        self.tmp = None

    def start(self):
        self.tmp = tempfile.mkdtemp(prefix="meedu-capture-")
        self.proc = subprocess.Popen(
            [
                CHROME,
                "--headless=new",
                f"--remote-debugging-port={self.port}",
                f"--user-data-dir={self.tmp}",
                "--no-first-run",
                "--no-default-browser-check",
                "--noerrdialogs",
                "--remote-allow-origins=*",
                "--disable-gpu",
                "--disable-dev-shm-usage",
                "about:blank",
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        for _ in range(120):
            try:
                urllib.request.urlopen(f"http://127.0.0.1:{self.port}/json/version", timeout=0.5).read()
                return
            except Exception:
                if self.proc.poll() is not None:
                    raise RuntimeError("Chrome 进程提前退出")
                time.sleep(0.25)
        raise RuntimeError("Chrome 启动失败")

    def open_tab(self):
        req = urllib.request.Request(f"http://127.0.0.1:{self.port}/json/new?about:blank", method="PUT")
        data = json.loads(urllib.request.urlopen(req, timeout=2).read())
        self.ws = websocket.create_connection(data["webSocketDebuggerUrl"], timeout=5)
        self.call("Page.enable")
        self.call("Runtime.enable")
        self.call("Network.enable")

    def call(self, method, params=None):
        self.seq += 1
        self.ws.send(json.dumps({"id": self.seq, "method": method, "params": params or {}}))
        while True:
            raw = self.ws.recv()
            msg = json.loads(raw)
            if msg.get("id") == self.seq:
                if "error" in msg:
                    raise RuntimeError(msg["error"])
                return msg.get("result", {})

    def navigate(self, url, wait=2.5):
        self.call("Page.navigate", {"url": url})
        time.sleep(wait)
        for _ in range(20):
            state = self.call("Runtime.evaluate", {"expression": "document.readyState", "returnByValue": True})
            if state.get("result", {}).get("value") == "complete":
                break
            time.sleep(0.2)
        time.sleep(wait)

    def set_viewport(self, width, height):
        self.call("Emulation.setDeviceMetricsOverride", {
            "width": width,
            "height": height,
            "deviceScaleFactor": 1,
            "mobile": width < 700,
        })

    def set_token(self, origin, key, token):
        if not key or not token:
            return
        self.navigate(origin, wait=0.5)
        expr = f"localStorage.setItem({json.dumps(key)}, {json.dumps(token)})"
        self.call("Runtime.evaluate", {"expression": expr, "returnByValue": True})

    def screenshot(self, url, path, width, height, token_key=None, token=None):
        self.set_viewport(width, height)
        origin = url.split("/", 3)[:3]
        origin = "/".join(origin) + "/"
        self.set_token(origin, token_key, token)
        self.navigate(url, wait=2.8)
        png = self.call("Page.captureScreenshot", {"format": "png", "fromSurface": True})["data"]
        Path(path).write_bytes(base64.b64decode(png))

    def close(self):
        try:
            if self.ws:
                self.ws.close()
        finally:
            if self.proc:
                self.proc.terminate()
            if self.tmp:
                shutil.rmtree(self.tmp, ignore_errors=True)


def make_side_by_side(name):
    live = OUT / f"{name}-live.png"
    proto = OUT / f"{name}-proto.png"
    combo = OUT / f"{name}-compare.png"
    a = Image.open(live).convert("RGB")
    b = Image.open(proto).convert("RGB")
    height = max(a.height, b.height)
    width = a.width + b.width + 24
    canvas = Image.new("RGB", (width, height + 42), "#f4f6fb")
    draw = ImageDraw.Draw(canvas)
    draw.rectangle([0, 0, width, 42], fill="#111827")
    draw.text((16, 13), "LIVE Docker", fill="#ffffff")
    draw.text((a.width + 40, 13), "Prototype", fill="#ffffff")
    canvas.paste(a, (0, 42))
    canvas.paste(b, (a.width + 24, 42))
    canvas.save(combo)
    return combo


def main():
    if len(sys.argv) < 4:
        raise SystemExit("usage: capture_compare.py ADMIN_TOKEN H5_TOKEN page [page...]")
    admin_token, h5_token = sys.argv[1], sys.argv[2]
    selected = sys.argv[3:]
    OUT.mkdir(exist_ok=True)
    cdp = CDP(9333)
    cdp.start()
    cdp.open_tab()
    try:
        made = []
        for name in selected:
            item = PAGES[name]
            w, h = item["size"]
            token = admin_token if item["live_token"] == "ADMIN_TOKEN" else h5_token
            cdp.screenshot(item["live"], OUT / f"{name}-live.png", w, h, item["live_key"], token)
            cdp.screenshot(item["proto"], OUT / f"{name}-proto.png", w, h)
            made.append(str(make_side_by_side(name)))
        print("\n".join(made))
    finally:
        cdp.close()


if __name__ == "__main__":
    main()
