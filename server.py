import os
import json
import secrets
import subprocess
from functools import wraps
from flask import Flask, jsonify, request, send_from_directory

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "data", "products.json")
SECRETS_FILE = os.path.join(BASE_DIR, "data", "admin_secrets.json")
IMG_DIR = os.path.join(BASE_DIR, "images")

app = Flask(__name__)
ACTIVE_TOKENS = set()

def load_public():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_public(data):
    clean = {
        "shopName": data.get("shopName", "Squishy Store"),
        "phone": data.get("phone", "0374860580"),
        "zalo": data.get("zalo", "0374860580"),
        "facebook": data.get("facebook", "https://www.facebook.com/anhduc.ng.121"),
        "products": [
            {k: v for k, v in p.items() if k not in ("sourcePrice", "costPrice")}
            for p in data.get("products", [])
        ]
    }
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(clean, f, ensure_ascii=False, indent=2)

def load_secrets():
    if not os.path.exists(SECRETS_FILE):
        return {"adminPin": "0580", "discountRules": {"under50": 14000, "from50": 16000, "packCost": 0}, "sourcePrices": {}}
    with open(SECRETS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_secrets(sec):
    with open(SECRETS_FILE, "w", encoding="utf-8") as f:
        json.dump(sec, f, ensure_ascii=False, indent=2)

def require_admin(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        token = request.headers.get("X-Admin-Token", "")
        if not token or token not in ACTIVE_TOKENS:
            return jsonify({"error": "Chưa đăng nhập quản trị"}), 401
        return fn(*args, **kwargs)
    return wrapper

@app.route("/")
@app.route("/index.html")
def customer_page():
    return send_from_directory(BASE_DIR, "index.html")

@app.route("/admin")
@app.route("/admin.html")
def admin_page():
    return send_from_directory(BASE_DIR, "admin.html")

@app.route("/images/<path:filename>")
def serve_image(filename):
    return send_from_directory(IMG_DIR, filename)

@app.route("/data/products.json")
def serve_public_data():
    return send_from_directory(os.path.join(BASE_DIR, "data"), "products.json")

@app.route("/api/products", methods=["GET"])
def get_public_products():
    return jsonify(load_public())

@app.route("/api/admin/login", methods=["POST"])
def admin_login():
    body = request.get_json(silent=True) or {}
    pin = str(body.get("pin", "")).strip()
    sec = load_secrets()
    if pin == str(sec.get("adminPin", "0580")):
        token = secrets.token_hex(24)
        ACTIVE_TOKENS.add(token)
        return jsonify({"ok": True, "token": token})
    return jsonify({"ok": False, "error": "Sai mã PIN quản trị!"}), 403

@app.route("/api/admin/logout", methods=["POST"])
def admin_logout():
    token = request.headers.get("X-Admin-Token", "")
    ACTIVE_TOKENS.discard(token)
    return jsonify({"ok": True})

@app.route("/api/admin/products", methods=["GET"])
@require_admin
def admin_get_products():
    pub = load_public()
    sec = load_secrets()
    sp_map = sec.get("sourcePrices", {})
    merged = []
    for p in pub.get("products", []):
        item = dict(p)
        item["sourcePrice"] = sp_map.get(str(p["id"]), 0)
        merged.append(item)
    return jsonify({
        "shopName": pub.get("shopName", "Squishy Store"),
        "phone": pub.get("phone", "0374860580"),
        "zalo": pub.get("zalo", "0374860580"),
        "facebook": pub.get("facebook", "https://www.facebook.com/anhduc.ng.121"),
        "discountRules": sec.get("discountRules", {"under50": 14000, "from50": 16000, "packCost": 0}),
        "products": merged
    })

@app.route("/api/admin/products", methods=["POST"])
@require_admin
def admin_save_products():
    body = request.get_json(silent=True) or {}
    pub = load_public()
    sec = load_secrets()
    if "shopName" in body:
        pub["shopName"] = str(body["shopName"]).strip() or pub["shopName"]
    if "phone" in body:
        pub["phone"] = str(body["phone"]).strip() or pub["phone"]
    if "zalo" in body:
        pub["zalo"] = str(body["zalo"]).strip() or pub["zalo"]
    if "discountRules" in body and isinstance(body["discountRules"], dict):
        sec["discountRules"] = body["discountRules"]
    if "newPin" in body and str(body["newPin"]).strip():
        sec["adminPin"] = str(body["newPin"]).strip()
    if "products" in body and isinstance(body["products"], list):
        sp_map = sec.get("sourcePrices", {})
        for p in body["products"]:
            if "sourcePrice" in p:
                sp_map[str(p["id"])] = p["sourcePrice"]
        sec["sourcePrices"] = sp_map
        pub["products"] = body["products"]
    save_public(pub)
    save_secrets(sec)
    return jsonify({"ok": True, "count": len(pub["products"])})

@app.route("/api/admin/upload/<int:pid>", methods=["POST"])
@require_admin
def admin_upload_image(pid):
    if "file" not in request.files:
        return jsonify({"error": "Không có file ảnh"}), 400
    f = request.files["file"]
    if not f.filename:
        return jsonify({"error": "File rỗng"}), 400
    ext = os.path.splitext(f.filename)[1].lower()
    if ext not in (".jpg", ".jpeg", ".png", ".webp"):
        return jsonify({"error": "Chỉ hỗ trợ JPG/PNG/WEBP"}), 400
    fname = f"product_{pid:02d}{ext}"
    f.save(os.path.join(IMG_DIR, fname))
    pub = load_public()
    for p in pub["products"]:
        if p["id"] == pid:
            p["image"] = f"images/{fname}"
            break
    save_public(pub)
    return jsonify({"ok": True, "image": f"images/{fname}"})

@app.route("/api/admin/publish", methods=["POST"])
@require_admin
def admin_publish():
    try:
        subprocess.run(["git", "add", "data/products.json", "images/"], cwd=BASE_DIR, check=True, capture_output=True, text=True)
        st = subprocess.run(["git", "status", "--porcelain"], cwd=BASE_DIR, check=True, capture_output=True, text=True)
        if st.stdout.strip():
            subprocess.run(["git", "commit", "-m", "Update public product prices"], cwd=BASE_DIR, check=True, capture_output=True, text=True)
        subprocess.run(["git", "push"], cwd=BASE_DIR, check=True, capture_output=True, text=True)
        return jsonify({"ok": True, "message": "Đã đẩy giá bán mới lên web công khai (giá gốc & biên lãi được giữ bí mật tuyệt đối trên máy bạn)!"})
    except subprocess.CalledProcessError as e:
        return jsonify({"ok": False, "error": (e.stderr or e.stdout or str(e)).strip()}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
