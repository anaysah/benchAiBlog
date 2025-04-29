import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { ButtonWithDropDown } from '../ui/ButtonWithDropDown';
import { UserRound } from 'lucide-react';
import { Logo } from '../ui/logo';
// import { useContext } from 'react';
// import { AuthContext } from '../../context/AuthContext';

const LeftHeader = () => {
  return (
    // <div className=''>
    <>
      <ButtonWithDropDown
        text="Categories"
        menuItems={[
          { label: 'Profile', href: '/profile' },
          { label: 'Settings', href: '/settings' },
          { label: 'Logout', href: '/logout' },
        ]}
      />
      <div>About</div>
      <div>Contact</div>
    </>
    // </div>
  )
}

const RightHeader = () => {
  return (
    <>
      <UserRound />
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
