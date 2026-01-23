
import { Article } from '../types';

/**
 * HOW TO ADD A NEW ARTICLE:
 * 1. Copy the structure of one of the objects below (from { to },).
 * 2. Paste it at the TOP of the 'articles' array to make it the newest.
 * 3. Update the fields:
 *    - id: unique string (e.g., '5')
 *    - title: Headline
 *    - excerpt: A short summary (2-3 lines)
 *    - category: Choose from 'Legislation', 'Corporate', 'Real Estate', etc.
 *    - isFeatured: Set to true if you want it big at the top of the Insights page.
 */

export const articles: Article[] = [
  {
    id: '1',
    title: "Bahrain's New Sijilat Portal 3.0: A Guide for Investors",
    excerpt: "The Ministry of Industry & Commerce has unveiled significant upgrades to the Sijilat portal. We analyze the new streamlined beneficial ownership registration process and what it means for foreign compliance.",
    category: 'Legislation',
    author: 'Corporate Team',
    date: 'Oct 12, 2024',
    readTime: '5 min read',
    isFeatured: true,
    imageUrl: 'https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?q=80&w=2070&auto=format&fit=crop'
  },
  {
    id: '2',
    title: "Labor Law Amendment: Remote Work Regulations",
    excerpt: "New amendments to the Private Sector Labor Law now formally recognize 'remote work' arrangements. Employers must update their standard employment contracts to mitigate liability regarding working hours and confidentiality.",
    category: 'Labor',
    author: 'Sarah Al-Mahmood',
    date: 'Sep 28, 2024',
    readTime: '4 min read',
    imageUrl: 'https://images.unsplash.com/photo-1593642632823-8f78536709c6?q=80&w=2070&auto=format&fit=crop'
  },
  {
    id: '3',
    title: "RERA: Stricter Governance for Owners Associations",
    excerpt: "The Real Estate Regulatory Authority has issued Circular No. 4/2024. Joint property managers face tighter scrutiny on service charge collections and reserve fund audits.",
    category: 'Real Estate',
    author: 'Abdulla Sahwan',
    date: 'Aug 15, 2024',
    readTime: '6 min read'
  },
  {
    id: '4',
    title: "Enforcing Foreign Arbitral Awards in GCC Courts",
    excerpt: "Despite the New York Convention, practical hurdles remain. We discuss a recent precedent-setting case regarding the ratification of a UK arbitration award in Bahraini courts.",
    category: 'Disputes',
    author: 'Litigation Department',
    date: 'July 10, 2024',
    readTime: '8 min read'
  },
  {
    id: '5',
    title: "Sahwan Law Named 'Boutique Firm of the Year'",
    excerpt: "We are honored to be recognized by the Gulf Legal Awards for our dedication to excellence in corporate restructuring and family business advisory.",
    category: 'Firm News',
    author: 'Press Office',
    date: 'June 01, 2024',
    readTime: '2 min read'
  }
];
