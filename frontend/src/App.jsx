import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Header from './components/layout/Header';
import Footer from './components/layout/Footer';
import Home from './pages/Home';
import Categories from './pages/Categories'
import Auth from './pages/Auth';
import { AuthProvider } from './auth/AuthProvider';
import Dashboard from './pages/Dashboard';
import ProtectedRoute from './auth/ProtectedRoute';

function App() {
  return (
    <BrowserRouter>
      <div className="flex flex-col min-h-screen">
        <Header />
        <main className="flex-grow">
          <AuthProvider>
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/Categories" element={<Categories />} />
              <Route path="/Auth" element={<Auth />} />


              <Route path="/dashboard" element={
                <ProtectedRoute>
                  <Dashboard />
                </ProtectedRoute>
              } />
            </Routes>
          </AuthProvider>
        </main>
        <Footer />
      </div>
    </BrowserRouter>
  );
}

export default App;