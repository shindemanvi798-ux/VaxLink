const API_BASE = '/api';

export async function fetchChildren() {
  try {
    const res = await fetch(`${API_BASE}/children`);
    if (!res.ok) throw new Error('Failed to fetch children');
    return await res.json();
  } catch (err) {
    console.warn('API connection failed, using local demo fallback:', err.message);
    return [
      { id: 'child_001', name: 'Aarav Sharma', dob: '2025-12-15', family_id: 'fam_demo_001' },
      { id: 'child_002', name: 'Ananya Sharma', dob: '2026-08-15', family_id: 'fam_demo_001' }
    ];
  }
}

export async function createChild(name, dob) {
  const res = await fetch(`${API_BASE}/children`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name, dob })
  });
  if (!res.ok) {
    const errorData = await res.json().catch(() => ({ detail: 'Failed to create child profile' }));
    throw new Error(errorData.detail || 'Failed to create child profile');
  }
  return await res.json();
}

export async function fetchChildSchedule(childId) {
  try {
    const res = await fetch(`${API_BASE}/children/${childId}/schedule`);
    if (!res.ok) throw new Error('Failed to fetch child schedule');
    return await res.json();
  } catch (err) {
    console.warn('API fallback for schedule:', err.message);
    return null;
  }
}

export async function fetchCamps() {
  try {
    const res = await fetch(`${API_BASE}/camps`);
    if (!res.ok) throw new Error('Failed to fetch camps');
    return await res.json();
  } catch (err) {
    console.warn('API fallback for camps:', err.message);
    return [];
  }
}

export async function bookSlot(campId, slotId, childId) {
  const res = await fetch(`${API_BASE}/camps/${campId}/slots/${slotId}/book`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ child_id: childId })
  });
  if (!res.ok) {
    const errorData = await res.json().catch(() => ({ detail: 'Failed to book slot' }));
    throw new Error(errorData.detail || 'Failed to book slot');
  }
  return await res.json();
}
