
export interface Service {
  id: string;
  number: string;
  title: string;
  description: string;
  tags: string[];
}

export interface NavItem {
  label: string;
  href: string;
}

export interface ChatMessage {
  role: 'user' | 'model';
  text: string;
  isStreaming?: boolean;
}

export type ArticleCategory = 'Legislation' | 'Corporate' | 'Real Estate' | 'Labor' | 'Disputes' | 'Firm News';

export interface Article {
  id: string;
  title: string;
  excerpt: string;
  category: ArticleCategory;
  author: string;
  date: string;
  readTime: string;
  isFeatured?: boolean;
  imageUrl?: string;
}
