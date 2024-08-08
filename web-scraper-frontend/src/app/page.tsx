"use client";

import { useState } from 'react';
import { useAppDispatch, useAppSelector } from './store/hooks';
import { setColleges } from './store/slices/collegesSlice';
import Pagination from './components/Pagination';

interface College {
  school_name: string;
  school_city: string;
  school_state: string;
}

const Home: React.FC = () => {
  const [loading, setLoading] = useState<boolean>(false);
  const [currentPage, setCurrentPage] = useState<number>(1);
  const itemsPerPage = 10;
  const dispatch = useAppDispatch();
  const data = useAppSelector((state) => state.colleges.data);
  const totalPages = Math.ceil(data.length / itemsPerPage);

  const startCrawl = async () => {
    setLoading(true);
    dispatch(setColleges([]));  // Clear the data to reflect the reset state
    const response = await fetch('/api/start-crawl', {
      method: 'POST',
    });
    const result = await response.json();
    setLoading(false);
    if (result) {
      dispatch(setColleges(result));  // Set the data returned from the API
      setCurrentPage(1); // Reset to first page
    } else {
      console.error('Failed to start crawl job');
    }
  };

  const handlePageChange = (page: number) => {
    setCurrentPage(page);
  };

  const paginatedData = data.slice((currentPage - 1) * itemsPerPage, currentPage * itemsPerPage);

  return (
    <div className="flex flex-col items-center justify-center p-8 bg-white rounded shadow-lg">
      <div className="text-center max-w-3xl">
        <h2 className="text-2xl font-bold mb-4">About This App</h2>
        <p className="mb-4">
          This application is a web crawler designed to scrape data from The College Board&apos;s BigFuture college search tool. The goal is to build a database containing information about American colleges and universities.
        </p>
        <p className="mb-4">
          The crawler scrapes and stores the following fields for each college:
        </p>
        <ul className="list-disc list-inside mb-4 text-left">
          <li>The school name</li>
          <li>The school city</li>
          <li>The school state</li>
          <li>&quot;The college board code&quot; (if it exists)</li>
        </ul>
        <p className="mb-4">
          The data is persisted into an SQLite database. The app respects web scraping constraints to avoid IP blocking by including delays between requests.
        </p>
      </div>
      <button
        onClick={startCrawl}
        disabled={loading}
        className={`px-6 py-3 text-lg font-semibold text-white rounded ${
          loading ? 'bg-gray-400 cursor-not-allowed' : 'bg-blue-600 hover:bg-blue-700'
        }`}
      >
        {loading ? 'Crawling...' : 'Start Crawl'}
      </button>
      <div className="mt-8 w-full">
        <h2 className="text-xl font-semibold mb-4">Results</h2>
        <ul className="space-y-4">
          {paginatedData.map((item, index) => (
            <li key={index} className="p-4 bg-gray-100 rounded border border-gray-300">
              {item.school_name} - {item.school_city}, {item.school_state}
            </li>
          ))}
        </ul>
        <Pagination currentPage={currentPage} totalPages={totalPages} onPageChange={handlePageChange} />
      </div>
    </div>
  );
};

export default Home;
