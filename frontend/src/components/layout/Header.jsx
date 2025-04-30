import React from 'react';
import { Logo } from '../ui/logo';
import DropdownComponent from '../common/DropdownComponent';
import { ChevronDown, UserRound } from 'lucide-react';
// import { useContext } from 'react';
// import { AuthContext } from '../../context/AuthContext';

const CategoryDropdownButton = ({ onClick }) => {
  return (
    <button onClick={onClick} className='inline-flex justify-center items-center gap-1'>
      Categories
      <ChevronDown className="w-4 h-4" />      
    </button>
  );
};

const CategoryDropdownMenu = () => {
  return (
    <div className='w-48'>
      <span className='block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100'>Profile</span>
      <span className='block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100'>Settings</span>
      <span className='block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100'>Logout</span>
    </div>
  );
};

const LeftHeader = () => {
  return (
    // <div className=''>
    <>
      {/* <ButtonWithDropDown
        text="Categories"
        menuItems={[
          { label: 'Profile', href: '/profile' },
          { label: 'Settings', href: '/settings' },
          { label: 'Logout', href: '/logout' },
        ]}
      /> */}
      <DropdownComponent
        MainComponent={CategoryDropdownButton} 
        DropdownContent={CategoryDropdownMenu} 
        position='left-0'
      />
      <div>About</div>
      <div>Contact</div>
    </>
    // </div>
  )
}

const UserIconButton = ({ onClick }) => {
  return (
    <button onClick={onClick} className='inline-flex justify-center items-center gap-1'>
      <UserRound />
      <ChevronDown className="w-4 h-4" />      
    </button>
  );
};

const UserIconDropdownMenu = () => {
  return (
    <div className='w-48'>
      <span className='block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100'>Profile</span>
      <span className='block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100'>Settings</span>
      <span className='block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100'>Logout</span>
    </div>
  );
};

const RightHeader = () => {
  return (
    <>
      {/* <UserButtonDropdown/> */}
      <DropdownComponent
        MainComponent={UserIconButton} 
        DropdownContent={UserIconDropdownMenu}
        position='right-0'
      />
    </>
  )
}

const MidHeader = () => {
  return(
    <>
      <Logo/>
    </>
  )
}

function Header() {
  return (
    <header className="p-4 bg-back-1">
      <div className="container mx-auto flex justify-between items-center">
        <div className="flex-1 flex justify-start gap-4 text-base font-light">
          <LeftHeader />
        </div>
        <div className="flex-1 flex justify-center">
          <MidHeader />
        </div>
        <div className="flex-1 flex justify-end">
          <RightHeader />
        </div>
      </div>
    </header>
  );
}

export default Header;
