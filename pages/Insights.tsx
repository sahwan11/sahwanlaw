
import React, { useState } from 'react';
import { ArrowRight, Clock, BookOpen, AlertCircle, CheckCircle, Loader2 } from 'lucide-react';
import { articles } from '../data/articles';
import { ArticleCategory } from '../types';

// Formspree Endpoint for Sahwan Law
const FORMSPREE_ENDPOINT = "https://formspree.io/f/xnjjqove";

const Insights: React.FC = () => {
  const [selectedCategory, setSelectedCategory] = useState<ArticleCategory | 'All'>('All');
  
  // Subscription Form State
  const [email, setEmail] = useState('');
  const [subStatus, setSubStatus] = useState<'idle' | 'submitting' | 'success' | 'error'>('idle');

  const categories: (ArticleCategory | 'All')[] = ['All', 'Legislation', 'Corporate', 'Real Estate', 'Labor', 'Disputes', 'Firm News'];

  // Filter logic
  const filteredArticles = selectedCategory === 'All' 
    ? articles 
    : articles.filter(a => a.category === selectedCategory);

  // Featured Article
  const featuredArticle = filteredArticles.find(a => a.isFeatured) || filteredArticles[0];
  const standardArticles = filteredArticles.filter(a => a.id !== featuredArticle?.id);

  const handleSubscribe = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!email) return;
    
    setSubStatus('submitting');

    const formData = new FormData();
    formData.append('email', email);
    formData.append('_subject', 'New Newsletter Subscription'); // Custom subject line

    try {
        const response = await fetch(FORMSPREE_ENDPOINT, {
            method: 'POST',
            body: formData,
            headers: { 'Accept': 'application/json' }
        });

        if (response.ok) {
            setSubStatus('success');
            setEmail('');
            setTimeout(() => setSubStatus('idle'), 5000);
        } else {
            setSubStatus('error');
        }
    } catch (error) {
        setSubStatus('error');
    }
  };

  return (
    <div className="pt-32 pb-24 min-h-screen bg-white">
        
        {/* Header */}
        <div className="container mx-auto px-6 md:px-12 mb-20 border-b border-gray-100 pb-12">
            <h1 className="font-serif text-5xl md:text-6xl text-charcoal-900 mb-6">Legal Insights</h1>
            <p className="text-slate-500 text-lg max-w-2xl font-light leading-relaxed">
                Navigating the complexities of GCC law. Expert analysis on legislation, market trends, and regulatory changes.
            </p>
        </div>

        <div className="container mx-auto px-6 md:px-12">
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-12">
                
                {/* Sidebar Filters - Sticky */}
                <div className="lg:col-span-3">
                    <div className="sticky top-32">
                        <h3 className="text-xs font-medium uppercase tracking-[0.2em] text-silver mb-6">Topics</h3>
                        <ul className="space-y-3 border-l border-gray-100 pl-4">
                            {categories.map(cat => (
                                <li key={cat}>
                                    <button 
                                        onClick={() => setSelectedCategory(cat)}
                                        className={`text-sm transition-all duration-300 block w-full text-left
                                            ${selectedCategory === cat 
                                                ? 'text-charcoal-900 font-medium translate-x-2' 
                                                : 'text-slate-500 hover:text-accent'}`}
                                    >
                                        {cat}
                                    </button>
                                </li>
                            ))}
                        </ul>

                        {/* Subscription Box */}
                        <div className="mt-16 bg-pearl p-8 border border-gray-100 relative overflow-hidden">
                             <div className="mb-4">
                                <BookOpen size={24} className="text-accent" />
                             </div>
                             
                             {subStatus === 'success' ? (
                                 <div className="animate-fade-in-up">
                                     <h4 className="font-serif text-lg text-charcoal-900 mb-2 flex items-center gap-2">
                                         Subscribed <CheckCircle size={18} className="text-green-600"/>
                                     </h4>
                                     <p className="text-xs text-slate-500">You've been added to our briefing list.</p>
                                 </div>
                             ) : (
                                 <>
                                    <h4 className="font-serif text-lg text-charcoal-900 mb-2">Subscribe to Briefs</h4>
                                    <p className="text-xs text-slate-500 mb-6 leading-relaxed">
                                        Get crucial legislative updates delivered to your inbox.
                                    </p>
                                    <form onSubmit={handleSubscribe} className="flex border-b border-charcoal-900 pb-2 relative">
                                        <input 
                                            type="email" 
                                            value={email}
                                            onChange={(e) => setEmail(e.target.value)}
                                            placeholder="Email Address" 
                                            required
                                            disabled={subStatus === 'submitting'}
                                            className="bg-transparent text-sm w-full focus:outline-none placeholder:text-slate-400 text-charcoal-900" 
                                        />
                                        <button 
                                            type="submit" 
                                            disabled={subStatus === 'submitting'}
                                            className="text-xs font-medium uppercase text-charcoal-900 hover:text-accent transition-colors disabled:opacity-50"
                                        >
                                            {subStatus === 'submitting' ? <Loader2 size={14} className="animate-spin"/> : 'Join'}
                                        </button>
                                    </form>
                                    {subStatus === 'error' && <p className="text-[10px] text-red-500 mt-2">Unable to subscribe. Please try again.</p>}
                                 </>
                             )}
                        </div>
                    </div>
                </div>

                {/* Content Area */}
                <div className="lg:col-span-9">
                    
                    {/* Featured Article */}
                    {featuredArticle && (
                        <div className="mb-16 group cursor-pointer">
                            <div className="aspect-[21/9] bg-gray-100 mb-8 overflow-hidden relative">
                                {featuredArticle.imageUrl ? (
                                    <img 
                                        src={featuredArticle.imageUrl} 
                                        alt={featuredArticle.title} 
                                        className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-105"
                                    />
                                ) : (
                                    <div className="w-full h-full bg-charcoal-900 flex items-center justify-center">
                                        <span className="font-serif text-white/10 text-9xl">SAS</span>
                                    </div>
                                )}
                                {featuredArticle.category === 'Legislation' && (
                                    <div className="absolute top-6 left-6 bg-accent text-white text-[10px] font-bold uppercase tracking-widest px-3 py-1.5 flex items-center gap-2">
                                        <AlertCircle size={12} /> New Regulation
                                    </div>
                                )}
                            </div>

                            <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
                                <div className="md:col-span-1 text-xs text-silver space-y-2 pt-2 border-t border-gray-100">
                                    <div className="flex items-center gap-2">
                                        <span className="w-2 h-2 rounded-full bg-accent"></span>
                                        {featuredArticle.category}
                                    </div>
                                    <div className="block">{featuredArticle.date}</div>
                                    <div className="flex items-center gap-1"><Clock size={12}/> {featuredArticle.readTime}</div>
                                </div>
                                <div className="md:col-span-3">
                                    <h2 className="font-serif text-4xl text-charcoal-900 mb-4 group-hover:text-accent transition-colors">
                                        {featuredArticle.title}
                                    </h2>
                                    <p className="text-slate-500 font-light leading-relaxed mb-6 text-lg">
                                        {featuredArticle.excerpt}
                                    </p>
                                    <div className="flex items-center gap-3 text-charcoal-900 text-sm font-medium uppercase tracking-widest">
                                        Read Full Analysis <ArrowRight size={16} />
                                    </div>
                                </div>
                            </div>
                        </div>
                    )}

                    {/* Standard Articles Grid */}
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-x-12 gap-y-16 border-t border-gray-100 pt-16">
                        {standardArticles.map((article) => (
                            <div key={article.id} className="group cursor-pointer">
                                <div className="flex items-center gap-3 text-xs font-medium uppercase tracking-widest text-silver mb-3">
                                    <span className={`${article.category === 'Legislation' ? 'text-accent' : 'text-slate-400'}`}>
                                        {article.category}
                                    </span>
                                    <span className="text-gray-300">|</span>
                                    <span>{article.date}</span>
                                </div>
                                <h3 className="font-serif text-2xl text-charcoal-900 mb-3 group-hover:text-accent transition-colors leading-tight">
                                    {article.title}
                                </h3>
                                <p className="text-slate-500 text-sm font-light leading-relaxed mb-4 line-clamp-3">
                                    {article.excerpt}
                                </p>
                                <div className="flex items-center justify-between text-xs text-silver border-t border-gray-50 pt-3">
                                    <span>By {article.author}</span>
                                    <span className="flex items-center gap-1"><Clock size={12}/> {article.readTime}</span>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>

            </div>
        </div>
    </div>
  );
};

export default Insights;
