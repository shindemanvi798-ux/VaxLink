import React, { useState, useEffect } from 'react';
import Header from './components/Header.jsx';
import Navigation from './components/Navigation.jsx';
import HomeDashboard from './components/HomeDashboard.jsx';
import ChildProfile from './components/ChildProfile.jsx';
import CampDiscovery from './components/CampDiscovery.jsx';
import AddChildModal from './components/AddChildModal.jsx';
import SlotBookingModal from './components/SlotBookingModal.jsx';
import BookingConfirmation from './components/BookingConfirmation.jsx';
import TeammateSeams from './components/TeammateSeams.jsx';

import {
  fetchChildren,
  createChild,
  fetchChildSchedule,
  fetchCamps,
  bookSlot
} from './api.js';

export default function App() {
  const [activeTab, setActiveTab] = useState('home');
  const [childrenList, setChildrenList] = useState([]);
  const [selectedChildId, setSelectedChildId] = useState(null);
  const [scheduleData, setScheduleData] = useState(null);
  const [camps, setCamps] = useState([]);
  
  // Modals & Booking flow
  const [isAddModalOpen, setIsAddModalOpen] = useState(false);
  const [bookingTarget, setBookingTarget] = useState(null); // { camp, slot }
  const [activeBookingResult, setActiveBookingResult] = useState(null);

  // Initial load
  useEffect(() => {
    loadInitialData();
  }, []);

  // Reload schedule when selected child changes
  useEffect(() => {
    if (selectedChildId) {
      loadSchedule(selectedChildId);
    }
  }, [selectedChildId]);

  const loadInitialData = async () => {
    try {
      const kids = await fetchChildren();
      setChildrenList(kids);
      if (kids && kids.length > 0) {
        setSelectedChildId(kids[0].id);
      }
      const campData = await fetchCamps();
      setCamps(campData);
    } catch (err) {
      console.error('Failed to load initial data:', err);
    }
  };

  const loadSchedule = async (childId) => {
    try {
      const schedule = await fetchChildSchedule(childId);
      setScheduleData(schedule);
    } catch (err) {
      console.error('Failed to load schedule:', err);
    }
  };

  const handleAddChild = async (name, dob) => {
    const newChild = await createChild(name, dob);
    const updatedKids = await fetchChildren();
    setChildrenList(updatedKids);
    setSelectedChildId(newChild.id);
    setActiveTab('schedule');
  };

  const handleBookVaccineClick = (vaccine) => {
    setActiveTab('camps');
  };

  const handleSelectSlot = (camp, slot) => {
    const activeChild = childrenList.find((c) => c.id === selectedChildId);
    setBookingTarget({ camp, slot, child: activeChild });
  };

  const handleConfirmBooking = async (campId, slotId, childId) => {
    const result = await bookSlot(campId, slotId, childId);
    setActiveBookingResult(result);
    setBookingTarget(null);
    // Refresh camps to reflect updated booked_count and crowd status
    const updatedCamps = await fetchCamps();
    setCamps(updatedCamps);
  };

  const selectedChild = childrenList.find((c) => c.id === selectedChildId);

  return (
    <div className="min-h-screen bg-slate-100 font-sans text-slate-900 pb-12">
      <Header
        childrenList={childrenList}
        selectedChildId={selectedChildId}
        onSelectChild={setSelectedChildId}
        onOpenAddModal={() => setIsAddModalOpen(true)}
      />

      <Navigation activeTab={activeTab} setActiveTab={setActiveTab} />

      <main className="max-w-4xl mx-auto px-4 py-6">
        {/* Booking Confirmation View */}
        {activeBookingResult ? (
          <BookingConfirmation
            booking={activeBookingResult}
            onBackToHome={() => {
              setActiveBookingResult(null);
              setActiveTab('home');
            }}
          />
        ) : (
          <>
            {activeTab === 'home' && (
              <HomeDashboard
                selectedChild={selectedChild}
                scheduleData={scheduleData}
                camps={camps}
                onNavigate={setActiveTab}
                onBookVaccine={handleBookVaccineClick}
              />
            )}

            {activeTab === 'schedule' && (
              <ChildProfile
                scheduleData={scheduleData}
                onBookVaccine={handleBookVaccineClick}
              />
            )}

            {activeTab === 'camps' && (
              <CampDiscovery
                camps={camps}
                onSelectSlot={handleSelectSlot}
              />
            )}

            {activeTab === 'assist' && <TeammateSeams />}
          </>
        )}
      </main>

      {/* Add Child Modal */}
      <AddChildModal
        isOpen={isAddModalOpen}
        onClose={() => setIsAddModalOpen(false)}
        onAddSuccess={handleAddChild}
      />

      {/* Slot Booking Modal */}
      {bookingTarget && (
        <SlotBookingModal
          isOpen={!!bookingTarget}
          onClose={() => setBookingTarget(null)}
          camp={bookingTarget.camp}
          slot={bookingTarget.slot}
          child={bookingTarget.child}
          onConfirmBooking={handleConfirmBooking}
        />
      )}
    </div>
  );
}
