
import React from 'react';
import { ArrowUpRight } from 'lucide-react';
import { Service } from '../types';

// Updated order: Corporate, Litigation, Notary, Owners, Sijilat, Banking, Real Estate
const services: Service[] = [
  {
    id: 'corporate',
    number: '01',
    title: 'Corporate & Commercial',
    description: 'End-to-end corporate services from M&A to complex restructuring. We handle the legal infrastructure so you can focus on growth.',
    tags: ['M&A', 'Contracts', 'Governance']
  },
  {
    id: 'litigation',
    number: '02',
    title: 'Litigation & Disputes',
    description: 'Strategic representation in courts and arbitration tribunals across the GCC. We build compelling cases and protect your interests through resolution.',
    tags: ['Civil', 'Arbitration', 'Enforcement']
  },
  {
    id: 'notary',
    number: '03',
    title: 'Notarization',
    description: 'Official notary services licensed by the Ministry of Justice. Authentication, translation, and certification for legal proceedings.',
    tags: ['Public Notary', 'Certified', 'Apostille']
  },
  {
    id: 'owners',
    number: '04',
    title: 'Owners Associations',
    description: 'Comprehensive legal support for homeowners associations and joint property management. Governance and compliance for shared communities.',
    tags: ['HOA', 'RERA', 'Disputes']
  },
  {
    id: 'sijilat',
    number: '05',
    title: 'Sijilat & Formation',
    description: 'Expert guidance through the Ministry of Industry & Commerce (Sijilat) portal. Swift company incorporation, CR amendments, and regulatory licensing.',
    tags: ['Sijilat', 'CR', 'Licensing']
  },
  {
    id: 'banking',
    number: '06',
    title: 'Banking & Finance',
    description: 'Advisory and transactional support for financial institutions and borrowers. Conventional and Islamic finance structures.',
    tags: ['Islamic Finance', 'Loans', 'CBB']
  },
  {
    id: 'realestate',
    number: '07',
    title: 'Real Estate',
    description: 'Full-spectrum property legal services from acquisition through development. Construction contracts, title matters, and investment structures.',
    tags: ['Construction', 'Development', 'Title']
  },
];

const Services: React.FC = () => {
  return (
    <section id="services" className="py-24 md:py-32 bg-pearl">
      <div className="container mx-auto px-6 md:px-12">
        <div className="flex flex-col md:flex-row md:items-end justify-between mb-16 md:mb-24 gap-6">
          <div>
            <span className="block text-xs font-medium uppercase tracking-[0.2em] text-silver mb-4">Practice Areas</span>
            <h2 className="font-serif text-4xl md:text-6xl text-charcoal-900">What We Do</h2>
          </div>
          <p className="max-w-md text-slate-500 font-light">
            Comprehensive legal expertise tailored to the unique challenges of the GCC market.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-px bg-gray-200 border border-gray-200">
          {services.map((service) => (
            <div 
              key={service.id} 
              className="group relative bg-white p-8 md:p-14 overflow-hidden cursor-pointer h-full flex flex-col justify-between hover:bg-charcoal-900 transition-colors duration-500"
            >
              <div className="relative z-10">
                <span className="block font-serif text-lg text-silver mb-8 group-hover:text-accent transition-colors duration-500">
                  {service.number}
                </span>
                <h3 className="font-serif text-2xl md:text-3xl text-charcoal-900 mb-4 group-hover:text-white transition-colors duration-500">
                  {service.title}
                </h3>
                <p className="text-slate-500 font-light leading-relaxed mb-8 group-hover:text-gray-400 transition-colors duration-500">
                  {service.description}
                </p>
                <div className="flex flex-wrap gap-2">
                  {service.tags.map(tag => (
                    <span key={tag} className="text-[10px] uppercase tracking-wider px-3 py-1.5 bg-pearl text-slate-600 rounded-sm group-hover:bg-white/10 group-hover:text-gray-300 transition-colors duration-500">
                      {tag}
                    </span>
                  ))}
                </div>
              </div>

              <div className="absolute bottom-8 right-8 md:bottom-12 md:right-12 w-12 h-12 rounded-full border border-gray-200 flex items-center justify-center group-hover:bg-white group-hover:border-white transition-all duration-500 z-10">
                <ArrowUpRight size={20} className="text-gray-400 group-hover:text-charcoal-900 transition-colors duration-500" />
              </div>
            </div>
          ))}
          
          {/* Filler for grid symmetry */}
           <div className="hidden lg:block bg-white p-8 md:p-14 relative overflow-hidden group">
                <div className="absolute inset-0 flex items-center justify-center opacity-5 transition-opacity duration-500 group-hover:opacity-10">
                    <span className="font-serif text-9xl text-charcoal-900">SAS</span>
                </div>
                <div className="absolute inset-0 bg-charcoal-900/0 group-hover:bg-charcoal-900/5 transition-colors duration-500"></div>
           </div>
        </div>
      </div>
    </section>
  );
};

export default Services;
