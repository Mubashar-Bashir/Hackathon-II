'use client';

import React, { useState, useRef, useEffect } from 'react';
import { User, Camera, Edit3, Mail, Phone, Settings, LogOut } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';

interface UserProfileDropdownProps {
  user: {
    name?: string;
    email?: string;
    phone?: string;
    avatar?: string;
  } | null;
  onLogout: () => void;
}

const UserProfileDropdown: React.FC<UserProfileDropdownProps> = ({ user, onLogout }) => {
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  const { updateUserProfile } = useAuth();

  const [profileData, setProfileData] = useState({
    name: user?.name || '',
    email: user?.email || '',
    phone: user?.phone || '',
  });

  const [isEditing, setIsEditing] = useState(false);
  const [imagePreview, setImagePreview] = useState<string | null>(null);

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsOpen(false);
        setIsEditing(false);
      }
    };

    if (isOpen) {
      document.addEventListener('mousedown', handleClickOutside);
    }
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [isOpen, setIsOpen]);

  const handleEditToggle = () => {
    setIsEditing(!isEditing);
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setProfileData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSave = () => {
    // Update the user profile in the context
    if (user) {
      updateUserProfile({
        name: profileData.name,
        email: profileData.email,
        phone: profileData.phone
      });
    }
    setIsEditing(false);
  };

  const handleImageChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        const imageUrl = reader.result as string;
        setImagePreview(imageUrl);

        // Update the user profile with the image URL
        if (user) {
          updateUserProfile({
            avatar: imageUrl // Only update the avatar, other fields will be handled separately
          });
        }
      };
      reader.readAsDataURL(file);
    }
  };

  return (
    <div className="relative" ref={dropdownRef}>
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center space-x-2 group"
        aria-label="User profile"
      >
        {user?.avatar ? (
          <div className="w-8 h-8 rounded-lg overflow-hidden">
            <img
              src={user.avatar}
              alt="Profile"
              className="w-full h-full object-cover"
            />
          </div>
        ) : (
          <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-indigo-500 to-pink-500 flex items-center justify-center">
            <User className="w-5 h-5 text-white" />
          </div>
        )}
        <span className="text-sm font-medium hidden sm:inline text-white group-hover:text-indigo-300 transition-colors">
          {user?.name || user?.email || 'User'}
        </span>
      </button>

      {isOpen && (
        <div className="absolute right-0 mt-2 w-64 bg-slate-800/90 backdrop-blur-xl border border-white/10 rounded-lg shadow-xl z-50 overflow-hidden">
          <div className="p-4 border-b border-white/10">
            <div className="flex items-center space-x-3">
              <div className="relative">
                {user?.avatar || imagePreview ? (
                  <div className="w-12 h-12 rounded-full overflow-hidden">
                    <img
                      src={imagePreview || user?.avatar || ''}
                      alt="Profile"
                      className="w-full h-full object-cover"
                    />
                  </div>
                ) : (
                  <div className="w-12 h-12 rounded-full bg-gradient-to-br from-indigo-500 to-pink-500 flex items-center justify-center">
                    <User className="w-6 h-6 text-white" />
                  </div>
                )}
                {isEditing && (
                  <label className="absolute bottom-0 right-0 bg-indigo-600 rounded-full p-1 cursor-pointer">
                    <Camera className="w-3 h-3 text-white" />
                    <input
                      type="file"
                      className="hidden"
                      accept="image/*"
                      onChange={handleImageChange}
                    />
                  </label>
                )}
              </div>
              <div>
                {isEditing ? (
                  <input
                    type="text"
                    name="name"
                    value={profileData.name}
                    onChange={handleInputChange}
                    className="text-white font-medium bg-slate-700 rounded px-2 py-1 text-sm w-full"
                  />
                ) : (
                  <p className="text-white font-medium">{user?.name || 'User'}</p>
                )}
                <p className="text-slate-400 text-xs">{user?.email}</p>
              </div>
            </div>
          </div>

          <div className="p-2">
            <div className="space-y-1">
              <div className="flex items-center space-x-2 px-2 py-2 rounded hover:bg-slate-700/50 transition-colors">
                <Mail className="w-4 h-4 text-slate-400" />
                <span className="text-slate-300 text-sm">Email: {user?.email}</span>
              </div>

              <div className="flex items-center space-x-2 px-2 py-2 rounded hover:bg-slate-700/50 transition-colors">
                <Phone className="w-4 h-4 text-slate-400" />
                {isEditing ? (
                  <input
                    type="text"
                    name="phone"
                    value={profileData.phone}
                    onChange={handleInputChange}
                    placeholder="Add phone number"
                    className="text-slate-300 text-sm bg-slate-700 rounded px-2 py-1 w-full"
                  />
                ) : (
                  <span className="text-slate-300 text-sm">
                    {user?.phone || 'Add phone number'}
                  </span>
                )}
              </div>
            </div>

            <div className="pt-2 mt-2 border-t border-white/10">
              {isEditing ? (
                <button
                  onClick={handleSave}
                  className="w-full flex items-center justify-center space-x-2 px-3 py-2 bg-indigo-600 hover:bg-indigo-700 rounded text-white text-sm transition-colors"
                >
                  <Settings className="w-4 h-4" />
                  <span>Save Changes</span>
                </button>
              ) : (
                <button
                  onClick={handleEditToggle}
                  className="w-full flex items-center justify-center space-x-2 px-3 py-2 bg-slate-700 hover:bg-slate-600 rounded text-slate-200 text-sm transition-colors"
                >
                  <Edit3 className="w-4 h-4" />
                  <span>Edit Profile</span>
                </button>
              )}

              <button
                onClick={onLogout}
                className="w-full flex items-center justify-center space-x-2 px-3 py-2 mt-2 bg-rose-600/20 hover:bg-rose-600/30 rounded text-rose-300 text-sm transition-colors"
              >
                <LogOut className="w-4 h-4" />
                <span>Logout</span>
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default UserProfileDropdown;