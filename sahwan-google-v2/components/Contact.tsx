import React, { useState } from 'react';

const Contact: React.FC = () => {
  const [formStatus, setFormStatus] = useState<'idle' | 'submitting' | 'success'>('idle');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setFormStatus('submitting');
    // Simulate network request
    setTimeout(() => {
      setFormStatus('success');
      alert('Thank you. We have received your inquiry.');
      setFormStatus('idle');
    }, 1500);
  };

  return (
    <section id="contact" className="py-24 md:py-32 bg-white border-t border-gray-100">
      <div className="container mx-auto px-6 md:px-12">
        <div className="grid grid-cols-1 lg:grid-cols-5 gap-16 lg:gap-24">
          
          {/* Info */}
          <div className="lg:col-span-2">
            <span className="block text-xs font-medium uppercase tracking-[0.2em] text-silver mb-6">Get in Touch</span>
            <h2 className="font-serif text-4xl text-charcoal-900 mb-8">Let's Discuss Your Legal Needs</h2>
            <p className="text-slate-500 font-light leading-relaxed mb-12">
              Whether you're launching a venture, navigating a dispute, or seeking ongoing counsel, we're here to help you move forward with confidence.
            </p>

            <div className="space-y-8">
              <div>
                <span className="block text-xs font-medium uppercase tracking-widest text-silver mb-1">Phone</span>
                <p className="text-lg text-charcoal-900">+973 17 531 566</p>
              </div>
              <div>
                <span className="block text-xs font-medium uppercase tracking-widest text-silver mb-1">Email</span>
                <p className="text-lg text-charcoal-900">info@sahwanlaw.com</p>
              </div>
              <div>
                <span className="block text-xs font-medium uppercase tracking-widest text-silver mb-1">Location</span>
                <p className="text-lg text-charcoal-900">Wind Tower, Diplomatic Area<br/>Manama, Kingdom of Bahrain</p>
              </div>
            </div>
          </div>

          {/* Form */}
          <div className="lg:col-span-3 bg-pearl p-8 md:p-12 lg:p-16">
            <div className="mb-10">
              <h3 className="font-serif text-2xl text-charcoal-900 mb-2">Request a Consultation</h3>
              <p className="text-slate-500 text-sm">We'll respond within one business day.</p>
            </div>

            <form onSubmit={handleSubmit} className="space-y-8">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                <div className="group relative">
                  <input type="text" id="name" required className="peer w-full bg-transparent border-b border-gray-300 py-3 text-charcoal-900 focus:outline-none focus:border-charcoal-900 transition-colors" placeholder=" " />
                  <label htmlFor="name" className="absolute left-0 top-3 text-gray-400 text-sm transition-all duration-300 peer-focus:-top-4 peer-focus:text-xs peer-focus:text-charcoal-900 peer-focus:uppercase peer-focus:tracking-widest peer-not-placeholder-shown:-top-4 peer-not-placeholder-shown:text-xs peer-not-placeholder-shown:text-charcoal-900 peer-not-placeholder-shown:uppercase peer-not-placeholder-shown:tracking-widest">Full Name</label>
                </div>
                <div className="group relative">
                  <input type="tel" id="phone" className="peer w-full bg-transparent border-b border-gray-300 py-3 text-charcoal-900 focus:outline-none focus:border-charcoal-900 transition-colors" placeholder=" " />
                  <label htmlFor="phone" className="absolute left-0 top-3 text-gray-400 text-sm transition-all duration-300 peer-focus:-top-4 peer-focus:text-xs peer-focus:text-charcoal-900 peer-focus:uppercase peer-focus:tracking-widest peer-not-placeholder-shown:-top-4 peer-not-placeholder-shown:text-xs peer-not-placeholder-shown:text-charcoal-900 peer-not-placeholder-shown:uppercase peer-not-placeholder-shown:tracking-widest">Phone</label>
                </div>
              </div>

              <div className="group relative">
                <input type="email" id="email" required className="peer w-full bg-transparent border-b border-gray-300 py-3 text-charcoal-900 focus:outline-none focus:border-charcoal-900 transition-colors" placeholder=" " />
                <label htmlFor="email" className="absolute left-0 top-3 text-gray-400 text-sm transition-all duration-300 peer-focus:-top-4 peer-focus:text-xs peer-focus:text-charcoal-900 peer-focus:uppercase peer-focus:tracking-widest peer-not-placeholder-shown:-top-4 peer-not-placeholder-shown:text-xs peer-not-placeholder-shown:text-charcoal-900 peer-not-placeholder-shown:uppercase peer-not-placeholder-shown:tracking-widest">Email Address</label>
              </div>

              <div className="group relative">
                <select id="service" className="w-full bg-transparent border-b border-gray-300 py-3 text-charcoal-900 focus:outline-none focus:border-charcoal-900 transition-colors appearance-none cursor-pointer">
                  <option value="" disabled selected>Select a Service</option>
                  <option value="corporate">Corporate & Commercial</option>
                  <option value="litigation">Litigation & Disputes</option>
                  <option value="notarization">Notarization & Documentation</option>
                  <option value="associations">Owners Associations</option>
                  <option value="banking">Banking & Finance</option>
                  <option value="real-estate">Real Estate & Construction</option>
                  <option value="other">Other</option>
                </select>
              </div>

              <div className="group relative">
                <textarea id="message" rows={4} className="peer w-full bg-transparent border-b border-gray-300 py-3 text-charcoal-900 focus:outline-none focus:border-charcoal-900 transition-colors resize-none" placeholder=" "></textarea>
                <label htmlFor="message" className="absolute left-0 top-3 text-gray-400 text-sm transition-all duration-300 peer-focus:-top-4 peer-focus:text-xs peer-focus:text-charcoal-900 peer-focus:uppercase peer-focus:tracking-widest peer-not-placeholder-shown:-top-4 peer-not-placeholder-shown:text-xs peer-not-placeholder-shown:text-charcoal-900 peer-not-placeholder-shown:uppercase peer-not-placeholder-shown:tracking-widest">How can we help?</label>
              </div>

              <button 
                type="submit" 
                disabled={formStatus === 'submitting'}
                className="w-full bg-charcoal-900 text-white text-xs font-medium uppercase tracking-widest py-5 hover:bg-black transition-colors disabled:opacity-70"
              >
                {formStatus === 'submitting' ? 'Sending...' : 'Send Inquiry'}
              </button>
            </form>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Contact;