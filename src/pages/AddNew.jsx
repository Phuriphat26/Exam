import React, { useState } from 'react';
import axios from 'axios';
import Sidebar from "../components/Sidebar";
// A placeholder for the Sidebar component to make this file self-contained and runnable.

export default function ExamPlannerAddNew() {
  const [formData, setFormData] = useState({
    title: '',
    subject: '',
    dueDate: '',
    time: '',
    spareTime: '',
    detail: '',
    level: '', // Kept as string for the select input
    reminder: false,
    email: '',
  });

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Simple client-side validation
    if (!formData.title || !formData.subject || !formData.dueDate) {
      alert('Please fill in required fields: Title, Subject, and Due Date');
      return;
    }
    if (formData.reminder && !formData.email) {
      alert('Please enter your email address for the reminder.');
      return;
    }

    // Map form's string level to a number for the API
    const levelMap = { Easy: 1, Medium: 2, Hard: 3 };
    const numericLevel = levelMap[formData.level] || 1; // Default to 1 if not set

    try {
      const res = await axios.post(
        "http://localhost:5000/api/courses/",
        { ...formData, level: numericLevel },
        { withCredentials: true }
      );
      alert(res.data.message);
      // Reset form on successful submission
      handleCancel(); 
    } catch (err) {
      if (err.response && err.response.status === 401) {
        alert("กรุณา login ก่อน"); // "Please login first"
      } else {
        console.error(err);
        alert("เกิดข้อผิดพลาด"); // "An error occurred"
      }
    }
  };

  const handleCancel = () => {
    setFormData({
      title: '',
      subject: '',
      dueDate: '',
      time: '',
      spareTime: '',
      detail: '',
      level: '',
      reminder: false,
      email: '',
    });
  };

  return (
    <div className="flex min-h-screen bg-gray-100 font-sans">
      <Sidebar />

      <div className="flex-1 p-4 sm:p-8">
        <div className="max-w-5xl mx-auto">
          <h1 className="text-3xl font-bold mb-6 text-gray-800">เพิ่มรายการสอบ</h1>
          
          <form onSubmit={handleSubmit} className="bg-white rounded-2xl shadow-lg p-6 sm:p-10">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-x-8 gap-y-6">
              {/* Title */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Title</label>
                <input
                  type="text"
                  name="title"
                  value={formData.title}
                  onChange={handleChange}
                  className="w-full px-4 py-3 rounded-lg border border-gray-300 bg-gray-50 focus:ring-2 focus:ring-blue-500 focus:outline-none transition"
                />
              </div>

              {/* Subject */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Subject</label>
                <input
                  type="text"
                  name="subject"
                  value={formData.subject}
                  onChange={handleChange}
                  className="w-full px-4 py-3 rounded-lg border border-gray-300 bg-gray-50 focus:ring-2 focus:ring-blue-500 focus:outline-none transition"
                />
              </div>

              {/* Due Date */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Due Date</label>
                <input
                  type="date"
                  name="dueDate"
                  value={formData.dueDate}
                  onChange={handleChange}
                  className="w-full px-4 py-3 rounded-lg border border-gray-300 bg-gray-50 focus:ring-2 focus:ring-blue-500 focus:outline-none transition"
                />
              </div>

              {/* Time */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Time</label>
                <input
                  type="time"
                  name="time"
                  value={formData.time}
                  onChange={handleChange}
                  className="w-full px-4 py-3 rounded-lg border border-gray-300 bg-gray-50 focus:ring-2 focus:ring-blue-500 focus:outline-none transition"
                />
              </div>

              {/* Spare Time */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Spare Time</label>
                <input
                  type="date"
                  name="spareTime"
                  value={formData.spareTime}
                  onChange={handleChange}
                  className="w-full px-4 py-3 rounded-lg border border-gray-300 bg-gray-50 focus:ring-2 focus:ring-blue-500 focus:outline-none transition"
                />
              </div>

              {/* Level */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Level</label>
                <select
                  name="level"
                  value={formData.level}
                  onChange={handleChange}
                  className="w-full px-4 py-3 rounded-lg border border-gray-300 bg-gray-50 text-gray-600 focus:ring-2 focus:ring-blue-500 focus:outline-none transition"
                >
                  <option value="">Select Level</option>
                  <option value="Easy">Easy</option>
                  <option value="Medium">Medium</option>
                  <option value="Hard">Hard</option>
                </select>
              </div>

              {/* Detail */}
              <div className="md:col-span-2">
                <label className="block text-sm font-medium text-gray-700 mb-2">Detail</label>
                <textarea
                  name="detail"
                  value={formData.detail}
                  onChange={handleChange}
                  rows="4"
                  className="w-full px-4 py-3 rounded-lg border border-gray-300 bg-gray-50 focus:ring-2 focus:ring-blue-500 focus:outline-none resize-none transition"
                />
              </div>

              {/* Reminder */}
              <div className="md:col-span-2 flex items-center">
                <label className="flex items-center gap-3 cursor-pointer">
                  <input
                    type="checkbox"
                    name="reminder"
                    checked={formData.reminder}
                    onChange={handleChange}
                    className="w-5 h-5 text-blue-600 rounded-md border-gray-300 focus:ring-blue-500 cursor-pointer"
                  />
                  <span className="font-medium text-gray-700">Set Reminder</span>
                </label>
              </div>
            </div>

            {/* Conditional Email Input */}
            <div className={`mt-6 overflow-hidden transition-all duration-500 ease-in-out ${formData.reminder ? 'max-h-40 opacity-100' : 'max-h-0 opacity-0'}`}>
              <label className="block text-sm font-medium text-gray-700 mb-2">Email Address</label>
              <input
                type="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                placeholder="Enter your email for the reminder"
                className="w-full md:w-1/2 px-4 py-3 rounded-lg border border-gray-300 bg-gray-50 focus:ring-2 focus:ring-blue-500 focus:outline-none transition"
              />
            </div>

            {/* Action Buttons */}
            <div className="flex gap-4 mt-10 justify-end">
              <button
                type="button"
                onClick={handleCancel}
                className="px-8 py-3 rounded-full bg-gray-200 text-gray-800 font-semibold hover:bg-gray-300 transition text-base"
              >
                ยกเลิก
              </button>
              <button
                type="submit"
                className="px-8 py-3 rounded-full bg-blue-600 text-white font-semibold hover:bg-blue-700 transition text-base"
              >
                บันทึก
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}
