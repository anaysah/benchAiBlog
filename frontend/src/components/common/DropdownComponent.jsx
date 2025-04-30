import React, { useState, useRef, useEffect } from 'react';

const Dropdown = ({ isVisible, position, children }) => {
  return (
    isVisible && (
      <div className={`absolute ${position} mt-1 z-10 border border-gray-200 rounded-md shadow-lg bg-white`}>
        {children}
      </div>
    )
  );
};

const DropdownComponent = ({ MainComponent, DropdownContent, position = "right-0" }) => {
  const [isDropdownVisible, setIsDropdownVisible] = useState(false);
  const wrapperRef = useRef(null);

  // Close dropdown on outside click
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (wrapperRef.current && !wrapperRef.current.contains(event.target)) {
        setIsDropdownVisible(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const toggleDropdown = () => {
    setIsDropdownVisible(prev => !prev);
  };

  return (
    <div className="relative" ref={wrapperRef}>
      <MainComponent onClick={toggleDropdown} />
      <Dropdown isVisible={isDropdownVisible} position={position}>
        <DropdownContent />
      </Dropdown>
    </div>
  );
};

export default DropdownComponent;
