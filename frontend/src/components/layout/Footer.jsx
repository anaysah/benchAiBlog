function Footer() {
    return (
      <footer className="bg-gray-800 text-white p-4">
        <div className="container mx-auto text-center">
          <div className="space-x-4 mb-4">
            <a href="/about" className="hover:underline">
              About
            </a>
            <a href="/contact" className="hover:underline">
              Contact
            </a>
          </div>
          <p>&copy; {new Date().getFullYear()} My Blog. All rights reserved.</p>
        </div>
      </footer>
    );
  }
  

export default Footer;