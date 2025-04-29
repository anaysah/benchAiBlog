import { X } from "lucide-react";
import { Logo } from "../ui/logo";

export function Footer() {
    return (
      <footer className="p-10 bg-back-2 text-text-3">
        <div className="container mx-auto my-4 flex justify-between items-start">
          <div className="">
            <Logo/>
            <p className="font-light text-sm">
            Did you come here for something in particular or just general Riker
            </p>
          </div>
          <div className="flex  gap-4 flex-column text-sm font-light flex-col">
            <span className="font-bold text-text-4">Blog</span>
            <span>Travel</span>
            <span>Technology</span>
            <span>Lifestyle</span>
            <span>fashion</span>
            <span>Business</span>
          </div>
          <div className="flex  gap-4 flex-column text-sm font-light flex-col">
            <span className="font-bold text-text-4">Quick Links</span>
            <span>FAQ</span>
            <span>Terms and Conditions</span>
            <span>Support</span>
            <span>Privacy Policy</span>
          </div>
          <div >
            <div className="flex flex-col gap-2 mb-4">
              <span className="font-bold text-text-4">Subscribe to our newsletter</span>
              <span className=" rounded overflow-hidden bg-back-3">
                <input type="text" className="mx-2 text-text-5 focus:outline-0"/>
                <button className="bg-text-1 text-white px-4 py-1">Subscribe</button>
              </span>
            </div>
            <div>
              <span className="font-bold text-text-4">Follow on</span>
              <span className="flex gap-4">
                <span className="">
                  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-twitter-icon lucide-twitter"><path d="M22 4s-.7 2.1-2 3.4c1.6 10-9.4 17.3-18 11.6 2.2.1 4.4-.6 6-2C3 15.5.5 9.6 3 5c2.2 2.6 5.6 4.1 9 4-.9-4.2 4-6.6 7-3.8 1.1 0 3-1.2 3-1.2z"/></svg>
                </span>
                <span>
                  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-linkedin-icon lucide-linkedin"><path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z"/><rect width="4" height="12" x="2" y="9"/><circle cx="4" cy="4" r="2"/></svg>
                </span>
                <span>
                  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-facebook-icon lucide-facebook"><path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"/></svg>
                </span>
                <span>
                  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-instagram-icon lucide-instagram"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
                </span>
              </span>
            </div>
          </div>
        </div>

        <hr className="text-[#D1E7E5]"/>

        <p className="text-center text-sm font-light mt-4 ">Designed By Themefisher & Developed By Gethugothemes</p>
      </footer>
    );
  }
  

export default Footer;