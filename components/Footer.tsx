import React from 'react';
import { Link } from 'react-router-dom';

const Footer: React.FC = () => {
  return (
    <footer className="bg-charcoal-900 text-white pt-24 pb-12 mt-auto">
      <div className="container mx-auto px-6 md:px-12">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-12 lg:gap-8 pb-16 border-b border-white/10">
          <div className="lg:col-span-1">
            <Link to="/" className="font-serif text-2xl mb-6 block text-white hover:text-accent transition-colors">Sahwan Law</Link>
            <p className="text-gray-400 text-sm leading-relaxed max-w-xs">
              A full-service law firm providing corporate, litigation, and advisory services across the GCC since 1975.
            </p>
          </div>
          
          <div>
            <h4 className="text-xs font-medium uppercase tracking-widest text-gray-500 mb-6">Services</h4>
            <ul className="space-y-4">
              <li><Link to="/services" className="text-sm text-gray-300 hover:text-white transition-colors">Sijilat & Formation</Link></li>
              <li><Link to="/services" className="text-sm text-gray-300 hover:text-white transition-colors">Corporate & Commercial</Link></li>
              <li><Link to="/services" className="text-sm text-gray-300 hover:text-white transition-colors">Litigation & Disputes</Link></li>
              <li><Link to="/services" className="text-sm text-gray-300 hover:text-white transition-colors">Real Estate</Link></li>
            </ul>
          </div>
          
          <div>
            <h4 className="text-xs font-medium uppercase tracking-widest text-gray-500 mb-6">Company</h4>
            <ul className="space-y-4">
              <li><Link to="/about" className="text-sm text-gray-300 hover:text-white transition-colors">Our Story</Link></li>
              <li><Link to="/about" className="text-sm text-gray-300 hover:text-white transition-colors">Leadership</Link></li>
              <li><Link to="/insights" className="text-sm text-gray-300 hover:text-white transition-colors">Insights</Link></li>
              <li><Link to="/careers" className="text-sm text-gray-300 hover:text-white transition-colors">Careers</Link></li>
            </ul>
          </div>
          
          <div>
            <h4 className="text-xs font-medium uppercase tracking-widest text-gray-500 mb-6">Connect</h4>
            <ul className="space-y-4">
              <li className="text-sm text-gray-300 flex items-start gap-2">
                <span className="text-accent">T:</span> +973 17 531 566
              </li>
              <li className="text-sm text-gray-300 flex items-start gap-2">
                <span className="text-accent">E:</span> info@sahwanlaw.com
              </li>
              <li className="text-sm text-gray-300 flex items-start gap-2">
                <span className="text-accent">A:</span> Wind Tower, Diplomatic Area, Bahrain
              </li>
            </ul>
          </div>
        </div>
        
        <div className="pt-12 flex flex-col md:flex-row justify-between items-center gap-6">
          <p className="text-xs text-gray-500">&copy; 2025 Sahwan Law. All rights reserved.</p>
          <div className="flex gap-6">
            <Link to="#" className="text-xs text-gray-500 hover:text-white transition-colors">Privacy Policy</Link>
            <Link to="#" className="text-xs text-gray-500 hover:text-white transition-colors">Terms of Service</Link>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;