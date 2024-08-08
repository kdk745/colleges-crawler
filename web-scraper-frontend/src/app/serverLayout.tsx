import React, { ReactNode } from 'react';
import './globals.css'; // Ensure you have the correct path

interface ServerLayoutProps {
  children: ReactNode;
}


const ServerLayout: React.FC<ServerLayoutProps> = ({ children }) => {
  return (
    <html lang="en">
      <body className="flex flex-col min-h-screen font-sans bg-white text-black">
        {children}
      </body>
    </html>
  );
};

export default ServerLayout;
