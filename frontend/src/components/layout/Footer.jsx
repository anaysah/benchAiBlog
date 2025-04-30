import { Logo } from "../ui/logo";
import { FacebookIcon, InstagramIcon, LinkedInIcon, TwitterIcon } from "../common/icons";

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
                
                <span>
                  <TwitterIcon/>
                </span>

                <span>
                  <LinkedInIcon/>
                </span>

                <span>
                  <FacebookIcon/>
                </span>

                <span>
                  <InstagramIcon/>
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