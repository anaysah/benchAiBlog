import { useState } from 'react';
import { ChevronDown } from 'lucide-react';
import React from 'react';

export const ButtonWithDropDown = ({ text, menuItems }) => {
  const [open, setOpen] = useState(false);

  return (
    <div className="relative inline-block text-left">
      <button
        onClick={() => setOpen(!open)}
        className="inline-flex justify-center items-center"
      >
        {text}
        <ChevronDown className="ml-2 w-4 h-4" />
      </button>

      {open && (
        <div className="absolute z-10 mt-2 w-48 bg-white border border-gray-200 rounded-md shadow-lg">
          {menuItems.map((item, index) => (
            <a
              key={index}
              href={item.href}
              className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
            >
              {item.label}
            </a>
          ))}
        </div>
      )}
    </div>
  );
};
