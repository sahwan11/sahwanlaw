import React from 'react';
import Contact from '../components/Contact';

const ContactPage: React.FC = () => {
  return (
    <div className="pt-20">
        <Contact />
        
        {/* Full Map Placeholder */}
        <div className="h-[500px] w-full bg-gray-200 relative">
             <iframe 
                src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3578.966453696515!2d50.5855!3d26.2361!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0x0!2zMjbCsDE0JzEwLjAiTiA1MMKwMzUnMDcuOCJF!5e0!3m2!1sen!2sbh!4v1625680000000!5m2!1sen!2sbh" 
                width="100%" 
                height="100%" 
                style={{border:0}} 
                allowFullScreen={true} 
                loading="lazy" 
                className="grayscale opacity-80 hover:grayscale-0 transition-all duration-500"
             ></iframe>
             
             <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-white p-6 shadow-xl text-center">
                 <span className="font-serif text-xl text-charcoal-900 block mb-1">Wind Tower</span>
                 <span className="text-xs text-slate-500 uppercase tracking-widest">Diplomatic Area</span>
             </div>
        </div>
    </div>
  );
};

export default ContactPage;