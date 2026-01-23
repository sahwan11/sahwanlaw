import React from 'react';

const Careers: React.FC = () => {
  return (
    <div className="pt-32 pb-24 min-h-screen">
        <div className="container mx-auto px-6 md:px-12">
            <div className="max-w-4xl mx-auto text-center mb-24">
                <span className="block text-xs font-medium uppercase tracking-[0.2em] text-accent mb-6">Join Our Team</span>
                <h1 className="font-serif text-5xl md:text-6xl text-charcoal-900 mb-8">Build Your Legacy with Us</h1>
                <p className="text-slate-500 text-lg font-light leading-relaxed">
                    We are always looking for exceptional legal talent. At Sahwan Law, we foster a culture of excellence, mentorship, and professional growth.
                </p>
            </div>

            <div className="max-w-5xl mx-auto">
                <div className="bg-pearl p-12 border border-gray-100 mb-8">
                    <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-6">
                        <div>
                            <h3 className="font-serif text-2xl text-charcoal-900 mb-2">Corporate Associate</h3>
                            <p className="text-sm text-slate-500">Manama, Bahrain · Full-time</p>
                        </div>
                        <a href="mailto:careers@sahwanlaw.com" className="px-8 py-3 bg-charcoal-900 text-white text-xs font-medium uppercase tracking-widest hover:bg-accent transition-colors">
                            Apply Now
                        </a>
                    </div>
                </div>

                <div className="bg-pearl p-12 border border-gray-100 mb-8">
                    <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-6">
                        <div>
                            <h3 className="font-serif text-2xl text-charcoal-900 mb-2">Legal Secretary</h3>
                            <p className="text-sm text-slate-500">Manama, Bahrain · Full-time</p>
                        </div>
                        <a href="mailto:careers@sahwanlaw.com" className="px-8 py-3 bg-charcoal-900 text-white text-xs font-medium uppercase tracking-widest hover:bg-accent transition-colors">
                            Apply Now
                        </a>
                    </div>
                </div>

                <div className="text-center mt-16">
                     <p className="text-slate-500 font-light mb-4">Don't see a relevant opening?</p>
                     <p className="text-charcoal-900 font-medium">Send your CV to <a href="mailto:careers@sahwanlaw.com" className="text-accent hover:underline">careers@sahwanlaw.com</a></p>
                </div>
            </div>
        </div>
    </div>
  );
};

export default Careers;