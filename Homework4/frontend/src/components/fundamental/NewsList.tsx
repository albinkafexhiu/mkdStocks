import React from 'react';
import { NewsArticle } from '../../types/fundamental';

interface NewsListProps {
  articles: NewsArticle[];
}

export const NewsList: React.FC<NewsListProps> = ({ articles }) => (
  <div className="bg-white rounded-lg shadow">
    <h3 className="text-lg font-semibold p-4 border-b">Recent News</h3>
    <div className="divide-y">
      {articles.map((article, index) => (
        <div key={index} className="p-4">
          <div className="flex items-start justify-between">
            <div className="flex-1">
              <p className="text-sm text-gray-600">{article.date}</p>
              <h4 className="font-medium mt-1">{article.title.translated}</h4>
              <p className="text-gray-600 mt-2 text-sm">
                {article.content.translated.slice(0, 200)}...
              </p>
              <a 
                href={article.url} 
                target="_blank" 
                rel="noopener noreferrer"
                className="text-blue-600 hover:text-blue-800 text-sm mt-2 inline-block"
              >
                Read more →
              </a>
            </div>
          </div>
        </div>
      ))}
    </div>
  </div>
);
