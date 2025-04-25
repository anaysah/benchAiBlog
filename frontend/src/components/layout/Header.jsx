import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { ButtonWithDropDown } from '../ui/ButtonWithDropDown';
// import { useContext } from 'react';
// import { AuthContext } from '../../context/AuthContext';

const LeftHeader = () => {
  return (
    <div>
      <ButtonWithDropDown
        text="Menu"
        menuItems={[
          { label: 'Profile', href: '/profile' },
          { label: 'Settings', href: '/settings' },
          { label: 'Logout', href: '/logout' },
        ]}
      />
    </div>
  )
}


function Header() {
//   const { token, setToken } = useContext(AuthContext);
//   const navigate = useNavigate();

//   const handleLogout = () => {
//     localStorage.removeItem('accessToken');
//     localStorage.removeItem('refreshToken');
//     setToken(null);
//     navigate('/login');
//   };

  return (
    <header className="bg-blue-600 text-white p-4">
      <div className="container mx-auto flex justify-between items-center">
        <LeftHeader/>
        <Link to="/" className="text-2xl font-bold">
          My Blog
        </Link>
      </div>
    </header>
  );
}

export default Header;