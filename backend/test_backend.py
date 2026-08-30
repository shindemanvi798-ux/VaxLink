from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health():
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"
    print("[PASS] Health check passed")

def test_list_children():
    res = client.get("/api/children")
    assert res.status_code == 200
    data = res.json()
    assert len(data) >= 2
    assert data[0]["name"] == "Aarav Sharma"
    print("[PASS] Children list passed")

def test_child_schedule():
    res = client.get("/api/children/child_001/schedule")
    assert res.status_code == 200
    data = res.json()
    assert data["child_name"] == "Aarav Sharma"
    assert "doses" in data
    assert len(data["doses"]) > 0
    assert data["progress_percentage"] > 0
    print("[PASS] Child schedule engine passed")

def test_camps_and_crowd():
    res = client.get("/api/camps")
    assert res.status_code == 200
    camps = res.json()
    assert len(camps) >= 3
    crowd_levels = [c["crowd_status"] for c in camps]
    assert "LOW" in crowd_levels
    assert "MEDIUM" in crowd_levels
    assert "HIGH" in crowd_levels
    print("[PASS] Camps and Crowd Indicators passed")

def test_booking_flow():
    # Book a slot in Shivaji Nagar PHC (camp_001, slot_c1_1)
    payload = {"child_id": "child_001", "family_id": "fam_demo_001"}
    res = client.post("/api/camps/camp_001/slots/slot_c1_1/book", json=payload)
    assert res.status_code == 201
    data = res.json()
    assert data["status"] == "CONFIRMED"
    assert data["child_name"] == "Aarav Sharma"
    assert data["camp_name"] == "Shivaji Nagar Primary Health Center (PHC)"
    assert "reference_code" in data
    print("[PASS] Booking flow and confirmation passed")

def test_chatbot():
    # 1. Test English greeting
    payload_en = {
        "messages": [
            {"role": "user", "content": "Hello Saathi, tell me about OPV vaccine."}
        ],
        "language": "en"
    }
    res_en = client.post("/api/chat/", json=payload_en)
    assert res_en.status_code == 200
    data_en = res_en.json()
    assert "reply" in data_en
    assert "Oral Polio Vaccine" in data_en["reply"] or "OPV" in data_en["reply"]
    print("[PASS] Chatbot EN passed")

    # 2. Test Hindi greeting
    payload_hi = {
        "messages": [
            {"role": "user", "content": "नमस्ते साथी, ओपीवी टीका क्या है?"}
        ],
        "language": "hi"
    }
    res_hi = client.post("/api/chat/", json=payload_hi)
    assert res_hi.status_code == 200
    data_hi = res_hi.json()
    assert "reply" in data_hi
    assert "ओरल पोलियो" in data_hi["reply"] or "नमस्ते" in data_hi["reply"]
    print("[PASS] Chatbot HI passed")

    # 3. Test Marathi greeting
    payload_mr = {
        "messages": [
            {"role": "user", "content": "नमस्कार, ताप बद्दल सांगा"}
        ],
        "language": "mr"
    }
    res_mr = client.post("/api/chat/", json=payload_mr)
    assert res_mr.status_code == 200
    data_mr = res_mr.json()
    assert "reply" in data_mr
    assert "ताप" in data_mr["reply"] or "नमस्कार" in data_mr["reply"]
    print("[PASS] Chatbot MR passed")

if __name__ == "__main__":
    test_health()
    test_list_children()
    test_child_schedule()
    test_camps_and_crowd()
    test_booking_flow()
    test_chatbot()
    print("\nALL BACKEND VERIFICATION TESTS PASSED SUCCESSFULLY!")
