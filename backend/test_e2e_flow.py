from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def run_e2e_hackathon_demo_flow():
    print("=== STARTING E2E HACKATHON DEMO FLOW VERIFICATION ===")

    # Step 1: Create a new child
    new_child_payload = {
        "name": "Pooja Sharma",
        "dob": "2026-01-15",
        "family_id": "fam_demo_001"
    }
    create_res = client.post("/api/children", json=new_child_payload)
    assert create_res.status_code == 201, f"Failed to create child: {create_res.text}"
    child_data = create_res.json()
    child_id = child_data["id"]
    print(f"[PASS] Created child '{child_data['name']}' with ID: {child_id}")

    # Step 2: Fetch calculated schedule for new child
    sched_res = client.get(f"/api/children/{child_id}/schedule")
    assert sched_res.status_code == 200
    sched = sched_res.json()
    assert sched["child_name"] == "Pooja Sharma"
    assert len(sched["doses"]) > 0
    print(f"[PASS] Calculated schedule contains {len(sched['doses'])} UIP doses. Progress: {sched['progress_percentage']}%")

    # Step 3: Fetch camp listing & verify crowd density metrics
    camps_res = client.get("/api/camps")
    assert camps_res.status_code == 200
    camps = camps_res.json()
    target_camp = camps[0] # Shivaji Nagar PHC
    target_slot = target_camp["slots"][0] # 09:00 - 10:30 AM
    initial_available = target_slot["available_slots"]
    print(f"[PASS] Target Camp: {target_camp['name']} | Initial Crowd: {target_camp['crowd_status']} | Slot Available: {initial_available}")

    # Step 4: Book slot for Pooja
    booking_payload = {"child_id": child_id, "family_id": "fam_demo_001"}
    book_res = client.post(
        f"/api/camps/{target_camp['id']}/slots/{target_slot['id']}/book",
        json=booking_payload
    )
    assert book_res.status_code == 201
    booking_info = book_res.json()
    assert booking_info["status"] == "CONFIRMED"
    assert booking_info["reference_code"].startswith("VX-")
    print(f"[PASS] Slot Booked! Token Reference: {booking_info['reference_code']}")

    # Step 5: Verify capacity and crowd status mutation
    updated_camps_res = client.get("/api/camps")
    updated_camps = updated_camps_res.json()
    updated_camp = [c for c in updated_camps if c["id"] == target_camp["id"]][0]
    updated_slot = [s for s in updated_camp["slots"] if s["id"] == target_slot["id"]][0]
    
    assert updated_slot["available_slots"] == initial_available - 1
    print(f"[PASS] Verified slot availability updated from {initial_available} -> {updated_slot['available_slots']}")
    print("=== E2E DEMO FLOW VERIFIED SUCCESSFULLY! ===")

if __name__ == "__main__":
    run_e2e_hackathon_demo_flow()
