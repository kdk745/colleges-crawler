"use client"; // Add this directive at the top

import React, { ReactNode, useEffect, useState } from 'react';
import { Provider } from 'react-redux';
import store from './store'; // Adjust the import based on your actual file structure

interface ClientLayoutProps {
  children: ReactNode;
}

const ClientLayout: React.FC<ClientLayoutProps> = ({ children }) => {

  return (
    <html lang="en">
      <body className="flex flex-col min-h-screen font-sans">
        <Provider store={store}>
          <header className="bg-blue-600 text-white p-4 text-center">
            <h1 className="text-1xl font-bold">College Scraper</h1>
          </header>
          <main className="flex-1 p-8 bg-gray-100">{children}</main>
          <footer className="bg-blue-600 text-white text-center p-4">
            <p>&copy; Built by Kayne Khoury</p>
          </footer>
        </Provider>
      </body>
    </html>
  );
};

export default ClientLayout;
